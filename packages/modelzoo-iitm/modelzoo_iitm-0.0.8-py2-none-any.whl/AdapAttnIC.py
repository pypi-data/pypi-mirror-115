## Adaptive Attention for Image Captioning

import torch
import torchvision
import torch.nn as  nn
import torch.nn.functional as F


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class Encoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = torchvision.models.resnet50(pretrained=True)
        for param in self.model.parameters():
            param.requires_grad = False
        self.model = torch.nn.Sequential(*(list(self.model.children())[:-2]))
    def forward(self, x):
        return self.model(x)


class Attention(nn.Module):
  def __init__(self, feature_dim, hidden_dim, embed_dim, num_vecs):
    super().__init__()
    
    self.feature_transform_fc = nn.Linear(feature_dim, hidden_dim)
    self.features_fc = nn.Linear(hidden_dim, num_vecs)
    self.hidden_fc = nn.Linear(hidden_dim, num_vecs)
    self.context_fc = nn.Linear(num_vecs, 1)
    self.input_fc = nn.Linear(hidden_dim+embed_dim, hidden_dim)
    self.hidden_gate_fc = nn.Linear(hidden_dim, hidden_dim)
    self.s_fc = nn.Linear(hidden_dim, num_vecs)
    self.ones = torch.ones(num_vecs,1).to(device) #[49,1]
    self.tanh = torch.tanh
    self.sigma = torch.sigmoid
    self.relu = nn.ReLU()
  def forward(self, features, hidden, inputs, memory, s):

    c1 = []
    #c1 = c1.to(device)
    for i in range(features.shape[0]):
      
      # features[i] size = [49,2048]
      
      features_transform = self.relu((self.feature_transform_fc(features[i,:,:]))) # [49,512] 
      
      f = self.features_fc(features_transform)                       # [49,49]
      h = self.hidden_fc(hidden[i,:].unsqueeze(0))                   # [1,49]
      h1 = self.ones @ h                                             # [49,49]
      z = self.context_fc(self.tanh(f+h1)).permute((1,0))            # [1,49]
      a = F.softmax(z, dim = 1)                                      # [1,49]
      c = a @ features_transform                                     # [1,512]

    
      #gate = self.sigma( self.input_fc(inputs[i,:]) + self.hidden_gate_fc(hidden[i,:]) )   # [512]
      #s = gate * self.tanh(memory[i,:])                                                    # [512]
      
      si = s[i].float()
      ws = self.s_fc(si.unsqueeze(0))                   # [1,49]
      
      w = self.tanh(ws+h)                              # [1,49]
      i = self.context_fc(w)                           # [1,1]
      
      concat = F.softmax(torch.cat((z,i), dim = 1), dim = 1).squeeze(0)  # [50]
      b = concat[-1]                                                     # [1]
  
      c1b = b*si + (1-b)*(c.squeeze(0))         #[512]
    
      c1.append(c1b)


    c1 = torch.stack(c1)                       #[80,1,512]

    

    return  c1.squeeze(1)                      #[80,512]


class Decoder(nn.Module):
    def __init__(self, embed_size, hidden_size, feature_dim, vocab_size, weights_matrix, device,num_layers=1):
        super(Decoder, self).__init__()
        
        # define the properties
        self.feature_dim = feature_dim
        self.embed_size = embed_size
        self.hidden_size = hidden_size
        self.vocab_size = vocab_size
        
        # lstm cell
        #self.lstm_cell = nn.LSTMCell(input_size = embed_size + hidden_size, hidden_size=hidden_size)
        self.lstm_cell = nn.LSTMCell(input_size = self.hidden_size + embed_size, hidden_size=hidden_size)
        # output fully connected layer
        self.fc_out = nn.Linear(in_features = self.hidden_size*2, out_features = self.vocab_size)
        self.globalf_fc = nn.Linear(feature_dim, self.hidden_size)
    
        # embedding layer
        self.embed = nn.Embedding(num_embeddings = self.vocab_size, embedding_dim = self.embed_size)
        self.embed.weight.requires_grad = False
        self.embed.load_state_dict({'weight': weights_matrix})
        self.relu = nn.ReLU()
        self.sigma = torch.sigmoid
        
        self.gate_x_fc = nn.Linear(in_features = hidden_size + embed_size, out_features = hidden_size )
        self.gate_h_fc = nn.Linear(in_features = hidden_size, out_features = hidden_size )

        self.attention = Attention(self.feature_dim, self.hidden_size, self.embed_size, 49)
        self.attention.to(device)
         
    def forward(self, features, captions):


        # features = [80,49,2048], captions = [80,num_words]
        
        # batch size
        batch_size = features.size(0)    # 80
        
        # calculating vg
        mean_features = torch.mean(features, dim = 1)   #[80,2048]
        vg = self.relu((self.globalf_fc(mean_features))) #[80,512]
        
        # initialising hidden and cell state
        hidden_state = vg
        cell_state = vg     
        
        # empty tensor which will contain the predicted words
        outputs = torch.empty((batch_size, captions.size(1), self.vocab_size)).to(device) #captions.size(1) is the number of words 
        # outputs = [80,num_words,vocab_size]
        
        # embed the captions
        captions_embed = self.embed(captions)    #[80,num_words,300]
        
        
        # pass the caption word by word
        for t in range(captions.size(1)):

            x = torch.cat((captions_embed[:,t,:],vg), dim = 1)    #[80,812] 
            
            gate = self.sigma(self.gate_x_fc(x) + self.gate_h_fc(hidden_state))  #80,512
            
            hidden_state, cell_state = self.lstm_cell(x, (hidden_state, cell_state))
            
            s = gate * cell_state      #[80,512]
            context = self.attention(features, hidden_state, x, cell_state, s)              #[80,512]
            
            
            out = torch.cat((context, hidden_state), dim = 1)                  #[80,1024]
            # output of the attention mechanism
            out = self.fc_out(out)                                             #[80, vocab_size]
            
            # build the output tensor
            outputs[:, t, :] = out      
    
        return F.log_softmax(outputs, dim = 2)