import torch
import torch.nn as nn
import torchvision
import numpy as np
import torch.nn.functional as F
import math
from torch.autograd import Variable
import torch.utils.model_zoo as model_zoo

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

''' Character CNN for Text Classification'''

class Char_CNN(nn.Module):
    def __init__(self):
        super().__init__()

        self.conv1 = nn.Conv1d(in_channels = 70, out_channels = 256, kernel_size = 7, stride = 1)
        self.maxpool = nn.MaxPool1d(kernel_size = 2, stride = 2)
        self.conv2 = nn.Conv1d(in_channels = 256, out_channels = 256, kernel_size = 7, stride = 1)
        self.conv3 = nn.Conv1d(in_channels = 256, out_channels = 256, kernel_size = 3, stride = 1)
        self.fc1 = nn.Linear(7936, 1024)
        self.fc2 = nn.Linear(1024, 1024)
        self.fc3 = nn.Linear(1024,1)
        self.sigmoid = nn.Sigmoid()
        self.relu = nn.ReLU()

    def forward(self, text):
        
        x = self.conv1(text)
        x = self.relu(x)
        x = self.maxpool(x)
        x = self.conv2(x)
        x = self.relu(x)
        x = self.maxpool(x)
        x = self.conv3(x)
        x = self.relu(x)
        x = self.conv3(x)
        x = self.relu(x)
        x = self.conv3(x)
        x = self.relu(x)
        x = self.conv3(x)
        x = self.relu(x)
        x = self.maxpool(x)
        x = torch.reshape(x, (-1, 1, 7936))
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)
        x = self.sigmoid(x)

        return x
