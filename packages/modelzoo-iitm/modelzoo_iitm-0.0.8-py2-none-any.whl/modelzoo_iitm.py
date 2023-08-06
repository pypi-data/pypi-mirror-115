import torch
import torch.nn as nn
import torchvision
import numpy as np
import torch.nn.functional as F
import math
from torch.autograd import Variable
import torch.utils.model_zoo as model_zoo
from UNet import *
from UNetPP import *
from PointNet import *
from StackGAN import *
from CharCNN import *
from PSPNet import *
from Inpainting import *
from AdapAttnIC import *
import requests

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# model_weights = {UNet : }
def models(name = None):
    if name is None:
        return "No Models loaded"
    else:
        return f"{name} model loaded successfully"

def UNet(num_channels = 1, pretrained = False):        # num_channels = 1 if grayscale image else num_channels = 3 if color image
    if pretrained == True:
        model = U_Net(num_channels)
        url = 'https://github.com/Vinayak-VG/ModelZoo_PyPi/releases/download/Weights/U-Net_Image_Seg_Norm.pt'
        r = requests.get(url, allow_redirects=True)
        open('unet.pt', 'wb').write(r.content)
        model.load_state_dict(torch.load('unet.pt'))
        # model.load_state_dict(model_zoo.load_url(url))
        print("Pre-Trained Model Loaded Succesfully")
    else:
        model = U_Net(num_channels)
        print("Model Loaded Succesfully") 
    return model

def UNetPP(num_channels = 1, pretrained = False):      # num_channels = 1 if grayscale image else num_channels = 3 if color image
    if pretrained == True:
        model = UNet_PP(num_channels, DenseBlock, BasicDownBlock, BasicUpBlock)
        url = "https://github.com/Vinayak-VG/ModelZoo_PyPi/releases/download/Weights/U-Net++.pt"
        r = requests.get(url, allow_redirects=True)
        open('unetpp.pt', 'wb').write(r.content)
        model.load_state_dict(torch.load('unetpp.pt'))
        # model.load_state_dict(model_zoo.load_url(url))
        print("Pre-Trained Model Loaded Succesfully")
    else:    
        model = UNet_PP(num_channels, DenseBlock, BasicDownBlock, BasicUpBlock)
        print("Model Loaded Succesfully") 
    return model

def PointNet(pretrained = False):
    if pretrained == True:
        model = Point_Net(T_Net)
        url = "https://github.com/Vinayak-VG/ModelZoo_PyPi/releases/download/Weights/PointNet_Best.pt"
        model.load_state_dict(model_zoo.load_url(url))
        print("Pre-Trained Model Loaded Succesfully")
    else:
        model = Point_Net(T_Net)
        model = model.apply(weights_init)
        print("Model Loaded Succesfully") 
    return model

def CharCNN(pretrained = False):
    if pretrained == True:
        model = Char_CNN()
        print("Pre-Trained Model Loaded Succesfully") 
        return model
    else:
        model = Char_CNN()
        print("Model Loaded Succesfully") 
        return model

# def KimCNN(vocab_size = 20000, embedding_dim = 300, n_filters = 100, filter_sizes = [3, 4, 5], output_dim = 1, dropout = 0.2, pad_idx = 0):
#     model = Kim_CNN(vocab_size, embedding_dim, n_filters, filter_sizes, output_dim, dropout, pad_idx)
#     return model

def StackGAN(name = "None", pretrained = False):
    if pretrained == True:
        if name == "None":
            return "Please specify the name of Model"
        elif name == 'StageI_Gen':
            model = StageI_GAN_Gen(Conditioning_Augmentation_StageI)
            url = "https://github.com/Vinayak-VG/ModelZoo_PyPi/releases/download/Weights/StageI_Gen_GAN_GPT2-3.pt"
            model.load_state_dict(model_zoo.load_url(url))
            print("Pre-Trained Model Loaded Succesfully")
            return model
        elif name == 'StageI_Dis':
            model = StageI_GAN_Dis(DownSample1)
            url = "https://github.com/Vinayak-VG/ModelZoo_PyPi/releases/download/Weights/StageI_Dis_GAN_GPT2.pt"
            model.load_state_dict(model_zoo.load_url(url))
            print("Pre-Trained Model Loaded Succesfully")
            return model
        elif name == 'StageII_Gen':
            model = StageII_GAN_Gen(DownSample2, ResidualBlock, UpSampling2, Conditioning_Augmentation_StageII)
            url = "https://github.com/Vinayak-VG/ModelZoo_PyPi/releases/download/Weights/StageII_Gen_GAN_GPT2.pt"
            model.load_state_dict(model_zoo.load_url(url))
            print("Pre-Trained Model Loaded Succesfully")
            return model
        elif name == 'StageII_Dis':
            model = StageII_GAN_Dis(DownSample3)
            url = "https://github.com/Vinayak-VG/ModelZoo_PyPi/releases/download/Weights/StageII_Dis_GAN_GPT2.pt"
            model.load_state_dict(model_zoo.load_url(url))
            print("Pre-Trained Model Loaded Succesfully")
            return model
    else:
        if name == "None":
            return "Please specify the name of Model"
        elif name == 'StageI_Gen':
            model = StageI_GAN_Gen(Conditioning_Augmentation_StageI)
            model = model.apply(weights_init)
            print("Model Loaded Succesfully") 
            return model
        elif name == 'StageI_Dis':
            model = StageI_GAN_Dis(DownSample1)
            model = model.apply(weights_init)
            print("Model Loaded Succesfully") 
            return model
        elif name == 'StageII_Gen':
            model = StageII_GAN_Gen(DownSample2, ResidualBlock, UpSampling2, Conditioning_Augmentation_StageII)
            model = model.apply(weights_init)
            print("Model Loaded Succesfully") 
            return model
        elif name == 'StageII_Dis':
            model = StageII_GAN_Dis(DownSample3)
            model = model.apply(weights_init)
            print("Model Loaded Succesfully") 
            return model

def Inpainting(name = "None", pretrained = False):
    if pretrained == True:
        if name == "None":
            return "Please specify the name of Model"
        elif name == 'Generator':
            model = Generator(use_cuda=True)
            print("Pre-Trained Model Loaded Succesfully")
            return model
        elif name == 'LocalDis':
            model = LocalDis()
            print("Pre-Trained Model Loaded Succesfully")
            return model
        elif name == 'GlobalDis':
            model = GlobalDis()
            print("Pre-Trained Model Loaded Succesfully")
            return model
    else:
        if name == "None":
            return "Please specify the name of Model"
        elif name == 'Generator':
            model = Generator(use_cuda=True)
            print("Model Loaded Succesfully") 
            return model
        elif name == 'LocalDis':
            model = LocalDis()
            print("Model Loaded Succesfully") 
            return model
        elif name == 'GlobalDis':
            model = GlobalDis()
            print("Model Loaded Succesfully") 
            return model

def PSPNet(pretrained = False):
    if pretrained == True:
        model = PSP_Net()
        print("Pre-Trained Model Loaded Succesfully") 
        return model
    else: 
        model = PSP_Net()
        print("Model Loaded Succesfully") 
        return model
      
def AdapAttnIC(embed_dim, hidden_dim, feature_dim, vocab_size, weights_matrix, name = 'None',pretrained = False):
    if pretrained == True:
        if name == "None":
            return "Please specify the name of Model"
        elif name == 'Encoder':
            model = Encoder()
            print("Pre-Trained Model Loaded Succesfully")
            return model
        elif name == 'Decoder':
            model = Decoder(embed_dim, hidden_dim, feature_dim, vocab_size, weights_matrix, device)
            print("Pre-Trained Model Loaded Succesfully")
            return model
    if pretrained == False:
        if name == "None":
            return "Please specify the name of Model"
        elif name == 'Encoder':
            model = Encoder()
            print("Model Loaded Succesfully") 
            return model
        elif name == 'Decoder':
            model = Decoder(embed_dim, hidden_dim, feature_dim, vocab_size, weights_matrix, device)
            print("Model Loaded Succesfully") 
            return model



