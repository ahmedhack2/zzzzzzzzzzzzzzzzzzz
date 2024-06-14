import numpy as np
import random
import json
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
#from other classes
from nltk_utils import bag_of_words, tokenize, stem
from model import NeuralNet

with open('intents.json', 'r') as f:
    intents = json.load(f)

all_words = []
tags = []
xy = []
# loop through each sentence in our intents patterns
for intent in intents['intents']:
    tag = intent['tag']
    # add to tag list
    tags.append(tag)
    for pattern in intent['patterns']:
        # tokenize each word in the sentence
        w = tokenize(pattern)
        # add to our words list
        all_words.extend(w)
        # add to xy pair
        xy.append((w, tag))

print(xy)        

# stem and lower each word
ignore_words = ['?', '.', '!']
all_words = [stem(w) for w in all_words if w not in ignore_words]
# remove duplicates and sort
all_words = sorted(set(all_words))
tags = sorted(set(tags))

print(len(xy), "patterns")
print(len(tags), "tags:", tags)
print(len(all_words), "unique stemmed words:", all_words)

# create training data
X_train = []
y_train = []
for (pattern_sentence, tag) in xy:
    # X: bag of words for each pattern_sentence
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)
    # y: PyTorch CrossEntropyLoss needs only class labels, not one-hot
    label = tags.index(tag)
    y_train.append(label)

X_train = np.array(X_train)
y_train = np.array(y_train)

# Hyper-parameters 
num_epochs = 1000
batch_size = 8
learning_rate = 0.001
input_size = len(X_train[0])
hidden_size = 8
output_size = len(tags)
print(input_size, output_size)

class ChatDataset(Dataset):

    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    # support indexing such that dataset[i] can be used to get i-th sample
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    # we can call len(dataset) to return the size
    def __len__(self):
        return self.n_samples

dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset,
                          batch_size=batch_size,
                          shuffle=True,
                          num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# cuda => GPU
model = NeuralNet(input_size, hidden_size, output_size).to(device) #push our model to device



# Loss and optimizer
#shoud found when we training our model
criterion = nn.CrossEntropyLoss() # used to calculate the loss in classification problem
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
# adam : id activiation function to training Neural Network
# Adam optimizer from the torch.optim module takes two arguments: model.parameters() and lr (learning rate).
#model.parameters() returns an iterator over all the learnable parameters of the model,

# Train the model
# an epoch represent a complete iteration
for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)
        
        # Forward pass
        outputs = model(words)
        # if y would be one-hot, we must apply
        # labels = torch.max(labels, 1)[1]
        loss = criterion(outputs, labels)
        
        # Backward and optimize
        optimizer.zero_grad()
        #optimizer.zero_grad() - This line clears (zeros) the gradients of all the parameters optimized by the optimizer. Gradients are accumulated when performing backpropagation during training, and calling zero_grad() ensures that the gradients are reset to zero before the next iteration.
        #In summary, these two lines of code set up and prepare the optimizer for gradient updates during training. The optimizer is initialized with the model parameters and learning rate, and zero_grad() is called to reset the gradients to zero before computing the gradients for the next batch of data.
        loss.backward() # to calculate the backpropagation
        optimizer.step()
        
    if (epoch+1) % 100 == 0:
        print (f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# Epoch [100/1000], Loss: 1.4827
# Epoch [200/1000], Loss: 0.0388
# Epoch [300/1000], Loss: 0.0704
# Epoch [400/1000], Loss: 0.0208
# Epoch [500/1000], Loss: 0.0078
# Epoch [600/1000], Loss: 0.0043
# Epoch [700/1000], Loss: 0.0012
# Epoch [800/1000], Loss: 0.0015
# Epoch [900/1000], Loss: 0.0015
# Epoch [1000/1000], Loss: 0.0003
#every time loss decresses this means the module in training well


print(f'final loss: {loss.item():.4f}')

data = {
"model_state": model.state_dict(),
"input_size": input_size,
"hidden_size": hidden_size,
"output_size": output_size,
"all_words": all_words,
"tags": tags
}

FILE = "data.pth"
torch.save(data, FILE)

print(f'training complete. file saved to {FILE}')
