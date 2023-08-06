import torch
from torch import nn


class AddBias(nn.Module):
    """Add scalar to tensor"""

    def __init__(self, bias=0):
        super(AddBias, self).__init__()
        self.bias = bias

    def forward(self, logits):
        return torch.add(logits, self.bias)
