# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 12:35:32 2019

@author: iamav
"""

import torch.nn as nn
import torchvision.models as models
import torch.nn.functional as F
import torch

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        resnet_firstlayer = models.resnet50(pretrained = True).conv1 #load just the first conv layer
        resnet = models.resnet50(pretrained = True) #load upto the classification layers except first conv layer
        modules = list(resnet.children())[1:9]  # not include the first conv layer.
        
        
        w1 = resnet_firstlayer.state_dict()['weight'][:,0,:,:]
        w2 = resnet_firstlayer.state_dict()['weight'][:,1,:,:]
        w3 = resnet_firstlayer.state_dict()['weight'][:,2,:,:]
        w4 = w1+w2+w3 # add the three weigths of the channels
        w4 = w4.unsqueeze(1)# make it 4 dimensional
    
        first_conv = nn.Conv2d(1, 64, 3, padding = (1,1)) #create a new conv layer
        first_conv.weight = torch.nn.Parameter(w4, requires_grad=True) #initialize  the conv layer's weigths with w4
#        first_conv.bias = torch.nn.Parameter(resnet_firstlayer.state_dict()['bias'], requires_grad=True) #initialize  the conv layer's weigths with vgg's first conv bias
    
    
        self.first_convlayer = first_conv #the first layer is 1 channel (Grayscale) conv layer
        self.resnet = nn.Sequential(*modules)

        self.fc1 = nn.Linear(2048, 1000)
        self.fc2 = nn.Linear(1002, 2)

    def forward(self, x, y):
        x=self.first_convlayer(x)
        x=self.resnet(x)
        x = F.relu(self.fc1(x.view(x.size(0), -1)), inplace=True) #flatten        
        x = torch.cat([x, y], dim=1)
        x = self.fc2(x)

        return x

m = Model()
print(m)