import os
from copy import copy
import numpy as np
import torch
import torch.nn as nn
import torchvision.models as models

class ModelHandler:
    def __init__(self):
        # Setup device
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        torch.backends.cudnn.benchmark = True
        self.model = models.mobilenet_v2(pretrained=True).to(self.device)

    def infer(self, input):
        output = self.model(input.to(self.device))
        return {"model": "mobilenet_v2", "input size": output.shape[0], "device": self.device.type}

