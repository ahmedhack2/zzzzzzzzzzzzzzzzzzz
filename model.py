import torch
import torch.nn as nn


#  this Neural Network of type feedForword NN
# class NeuralNet(nn.Module) => class NeuralNet inhert from nn.Module class that provided from torch 
class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size) 
        self.l2 = nn.Linear(hidden_size, hidden_size) 
        self.l3 = nn.Linear(hidden_size, num_classes)
        self.relu = nn.ReLU()
        # relu is activiation function
    
    def forward(self, x):
        out = self.l1(x) #pass the input to layer one
        out = self.relu(out) # apply the activiation function tp layer 1
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        # no activation and no softmax at the end
        return out
