"""
Pruning a MLP by weights with one shot
"""

import torch
import torch.nn as nn
import torchvision.datasets as datasets
import torchvision.transforms as transforms

from pruning.methods import weight_prune
from pruning.utils import to_var, train, test, check_nonzero
from models import MLP


# Hyper Parameters
param = {
    'pruning_perc': 90.,
    'batch_size': 128, 
    'test_batch_size': 100,
    'num_epochs': 10,
    'learning_rate': 0.001,
    'weight_decay': 5e-4,
}


# Data loaders
train_dataset = datasets.MNIST(root='../data/',train=True, download=True, 
    transform=transforms.ToTensor())
loader_train = torch.utils.data.DataLoader(train_dataset, 
    batch_size=param['batch_size'], shuffle=True)

test_dataset = datasets.MNIST(root='../data/', train=False, download=True, 
    transform=transforms.ToTensor())
loader_test = torch.utils.data.DataLoader(test_dataset, 
    batch_size=param['test_batch_size'], shuffle=True)


# Load the pretrained model
net = MLP()
# net.load_state_dict(torch.load('mlp_pretrained.pkl'))
if torch.cuda.is_available():
    print('CUDA ensabled.')
    net.cuda()

# prune the weights
# masks = weight_prune(net, param['pruning_perc'])
# net.set_masks(masks)


# Retraining
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.RMSprop(net.parameters(), lr=param['learning_rate'], 
                                weight_decay=param['weight_decay'])

train(net, criterion, optimizer, param, loader_train)


# Check accuracy and nonzeros weights in each layer
test(net, loader_test)
prune_rate(net)


# Save and load the entire model
torch.save(net.state_dict(), 'mlp_pretrained.pkl')