import os, glob, re, shutil
import subprocess
from sys import platform

import tifffile
import numpy as np
from skimage import morphology, transform
from barbar import Bar
from tqdm import tqdm as tqdm

import torch
from torch import nn as nn, flatten
from torch.utils.data import Dataset, DataLoader, random_split
import torch.nn.functional as F
import torch.optim as optim

from .losses import *
from .predict import Predict
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


class Trainer:
    def __init__(self, network, dataset, num_epochs, batch_size=4, lr=1e-3, momentum=1e-1, n_filter=64, val_split=0.2,
                 save_dir='./', save_name='model.pth', save_iter=False, load_weights=False, bce_dice=(1, 1)):
        """Class for training of neural network"""
        self.network = network
        self.model = network(n_filter=n_filter).to(device)
        self.data = dataset
        self.num_epochs = num_epochs
        self.batch_size = batch_size
        self.lr = lr
        self.momentum = momentum
        self.best_loss = torch.tensor(float('inf'))
        self.save_iter = save_iter
        self.bce_dice = bce_dice
        self.n_filter = n_filter
        # split training and validation data
        num_val = int(len(dataset) * val_split)
        num_train = len(dataset) - num_val
        self.dim = dataset.dim_out
        train_data, val_data = random_split(dataset, [num_train, num_val])
        self.train_loader = DataLoader(train_data, batch_size=self.batch_size, pin_memory=True, drop_last=True)
        self.val_loader = DataLoader(val_data, batch_size=self.batch_size, pin_memory=True, drop_last=True)
        self.criterion = BCEDiceLoss(bce_dice[0], bce_dice[1])
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(self.optimizer, 'min', patience=4, factor=0.1)
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)
        self.save_name = save_name
        if load_weights:
            self.state = torch.load(self.save_dir + '/' + self.save_name)
            self.model.load_state_dict(self.state['state_dict'])

    def iterate(self, epoch, mode):
        if mode == 'train':
            print('\nStarting training epoch %s ...' % epoch)
            for i, batch_i in enumerate(Bar(self.train_loader)):
                x_i = batch_i['image'].view(self.batch_size, 1, self.dim[0], self.dim[1]).to(device)
                y_i = batch_i['mask'].view(self.batch_size, 1, self.dim[0], self.dim[0]).to(device)
                # Forward pass: Compute predicted y by passing x to the model
                y_pred, y_logits = self.model(x_i)

                # Compute and print loss
                loss = self.criterion(y_logits, y_i)

                # Zero gradients, perform a backward pass, and update the weights.
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

        elif mode == 'val':
            loss_list = []
            print('\nStarting validation epoch %s ...' % epoch)
            with torch.no_grad():
                for i, batch_i in enumerate(Bar(self.val_loader)):
                    x_i = batch_i['image'].view(self.batch_size, 1, self.dim[0], self.dim[1]).to(device)
                    y_i = batch_i['mask'].view(self.batch_size, 1, self.dim[0], self.dim[1]).to(device)
                    # Forward pass: Compute predicted y by passing x to the model
                    y_pred, y_logits = self.model(x_i)
                    loss = self.criterion(y_logits, y_i)
                    loss_list.append(loss.detach())
            val_loss = torch.stack(loss_list).mean()
            return val_loss

        torch.cuda.empty_cache()

    def start(self, test_data_path=None, result_path=None):
        for epoch in range(self.num_epochs):
            self.iterate(epoch, 'train')
            self.state = {
                'epoch': epoch,
                'best_loss': self.best_loss,
                'state_dict': self.model.state_dict(),
                'optimizer': self.optimizer.state_dict(),
                'lr': self.lr,
                'bce_dice': self.bce_dice,
                'n_filter': self.n_filter,
                'augmentation': self.data.aug_factor,
                'clip_thres': self.data.clip_thres,
                'noise_amp': self.data.noise_amp,
                'brightness_contrast': self.data.brightness_contrast,
                'shiftscalerotate': self.data.shiftscalerotate,
            }
            with torch.no_grad():
                val_loss = self.iterate(epoch, 'val')
                self.scheduler.step(val_loss)
            if val_loss < self.best_loss:
                print('\nValidation loss improved from %s to %s - saving model state' % (
                    round(self.best_loss.item(), 5), round(val_loss.item(), 5)))
                self.state['best_loss'] = self.best_loss = val_loss
                torch.save(self.state, self.save_dir + '/' + self.save_name)
            if self.save_iter:
                torch.save(self.state, self.save_dir + '/' + f'model_epoch_{epoch}.pth')

            if test_data_path is not None:
                files = glob.glob(test_data_path + '*.tif')
                for i, file in enumerate(files):
                    Predict(file, result_path + os.path.basename(file) + f'epoch_{epoch}.tif', self.network,
                            self.save_dir + '/' + f'model_epoch_{epoch}.pth', resize_dim=(512, 512), invert=False,
                            n_filter=self.n_filter)

