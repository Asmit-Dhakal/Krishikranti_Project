import torch
import torch.nn as nn
import torch.nn.functional as F

class ImageClassificationBase(nn.Module):
    def training_step(self, batch):
        images, labels = batch
        out = self(images)  # Generate predictions
        loss = F.cross_entropy(out, labels)  # Calculate loss
        return loss

def conv_block(in_channels, out_channels, pool=False):
    layers = [nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
              nn.BatchNorm2d(out_channels),
              nn.ReLU(inplace=True)]
    if pool:
        layers.append(nn.MaxPool2d(2))
    return nn.Sequential(*layers)

class mymodel(ImageClassificationBase):
    def __init__(self, in_channels, num_classes):
        super().__init__()
        # Input : 3 * 256 * 256
        self.conv1 = conv_block(in_channels, 64, pool=True) # 64 * 128 * 128
        self.conv2 = conv_block(64, 128, pool=True) # 128 * 64 * 64
        self.res1 = nn.Sequential(conv_block(128, 128),
                                  conv_block(128, 128)) # 128 * 64 * 64

        self.conv3 = conv_block(128, 256, pool=True) # 256 * 32 * 32
        self.res2 = nn.Sequential(conv_block(256, 256),
                                  conv_block(256, 256)) # 256 * 32 * 32

        self.conv4 = conv_block(256, 512, pool=True) # 512 * 16 * 16
        self.res3 = nn.Sequential(conv_block(512, 512),
                                  conv_block(512, 512)) # 512 * 16 * 16

        self.conv5 = conv_block(512, 1024, pool=True) # 1024 * 8 * 8
        self.res4 = nn.Sequential(conv_block(1024, 1024),
                                  conv_block(1024, 1024)) # 1024 * 8 * 8

        self.classifier = nn.Sequential(nn.MaxPool2d(8),  # 1024 * 1 * 1
                                        nn.Flatten(),     # 1024
                                        nn.Dropout(0.5),
                                        nn.Linear(1024, num_classes))

    def forward(self, xb):
        out = self.conv1(xb)
        out = self.conv2(out)
        out = self.res1(out) + out
        out = self.conv3(out)
        out = self.res2(out) + out
        out = self.conv4(out)
        out = self.res3(out) + out
        out = self.conv5(out)
        out = self.res4(out) + out
        out = self.classifier(out)
        return out

from django.db import models

class Disease(models.Model):
    name = models.CharField(max_length=100, unique=True)
    solution = models.TextField()

    def __str__(self):
        return self.name