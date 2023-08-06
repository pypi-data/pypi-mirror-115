import os, re
import subprocess
from sys import platform

import tifffile
import numpy as np
from tqdm import tqdm as tqdm
from .unet import Unet

import torch

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


class Predict:
    """
    Class for prediction of tif-movies.
    1) Loading file and preprocess (normalization)
    2) Resizing of images into patches with resize_dim
    3) Prediction with U-Net
    4) Stitching of predicted patches and averaging of overlapping regions
    """

    def __init__(self, tif_file, result_name, model_params, n_filter=64, resize_dim=(512, 512), invert=False,
                 frame_lim=None, clip_thres=(0., 99.8), add_tile=0, bias=1, normalize_result=False):
        self.tif_file = tif_file
        self.resize_dim = resize_dim
        self.add_tile = add_tile
        self.n_filter = n_filter
        self.bias = bias
        self.normalize_result = normalize_result
        self.invert = invert
        self.clip_thres = clip_thres
        self.frame_lim = frame_lim
        self.result_name = result_name
        if self.result_name == 'nodes':
            self.folder = os.path.dirname(self.tif_file)
        else:
            self.folder = re.split('.tif', self.tif_file)[0] + '/'

        # read, preprocess and split data
        imgs = self.read_data()
        imgs = self.preprocess(imgs)
        patches = self.split(imgs)
        del imgs

        # load model and predict data
        self.model = Unet(n_filter=self.n_filter).to(device)
        self.model.load_state_dict(torch.load(model_params)['state_dict'])
        self.model.eval()
        result_patches = self.predict(patches)
        del patches
        # stitch patches (mean of overlapped regions)
        imgs_result = self.stitch(result_patches)
        del result_patches

        # save as .tif file
        self.save_as_tif(imgs_result, self.result_name, normalize=normalize_result)

    def open_folder(self):
        if platform.system() == "Windows":
            os.startfile(self.folder)
        elif platform.system() == "Linux":
            subprocess.Popen(["xdg-open", self.folder])

    def read_data(self):
        imgs = tifffile.imread(self.tif_file)
        if self.frame_lim is not None:
            imgs = imgs[self.frame_lim[0]:self.frame_lim[1]]
        self.imgs_shape = imgs.shape
        if len(self.imgs_shape) == 2:  # if single image
            self.imgs_shape = [1, self.imgs_shape[0], self.imgs_shape[1]]
        return imgs

    def preprocess(self, imgs):
        if len(imgs.shape) == 3:
            for i, img in enumerate(imgs):
                img = np.clip(img, a_min=np.nanpercentile(img, self.clip_thres[0]),
                              a_max=np.percentile(img, self.clip_thres[1]))
                img = img - np.min(img)
                img = img / np.max(img) * 255
                if self.invert:
                    img = 255 - img
                imgs[i] = img
        if len(imgs.shape) == 2:
            imgs = np.clip(imgs, a_min=np.nanpercentile(imgs, self.clip_thres[0]),
                           a_max=np.percentile(imgs, self.clip_thres[1]))
            imgs = imgs - np.min(imgs)
            imgs = imgs / np.max(imgs) * 255
            if self.invert:
                imgs = 255 - imgs
        imgs = imgs.astype('uint8')
        return imgs

    def split(self, imgs):
        # number of patches in x and y
        self.N_x = int(np.ceil(self.imgs_shape[1] / self.resize_dim[0])) + self.add_tile
        self.N_y = int(np.ceil(self.imgs_shape[2] / self.resize_dim[1])) + self.add_tile
        self.N_per_img = self.N_x * self.N_y
        self.N = self.N_x * self.N_y * self.imgs_shape[0]  # total number of patches
        print('Resizing into each %s patches ...' % self.N_per_img)

        # define array for prediction
        patches = np.zeros((self.N, 1, self.resize_dim[0], self.resize_dim[1]), dtype='uint8')

        # zero padding of image if imgs_shape < resize_dim
        if self.imgs_shape[0] > 1:
            if self.imgs_shape[1] < self.resize_dim[0]:  # for x
                imgs = np.pad(imgs, ((0, 0), (0, self.resize_dim[0] - self.imgs_shape[1]), (0, 0)),
                              'constant')
            if self.imgs_shape[2] < self.resize_dim[1]:  # for y
                imgs = np.pad(imgs, ((0, 0), (0, 0), (0, self.resize_dim[1] - self.imgs_shape[2])),
                              'constant')
        elif self.imgs_shape[0] == 1:
            if self.imgs_shape[1] < self.resize_dim[0]:  # for x
                imgs = np.pad(imgs, ((0, self.resize_dim[0] - self.imgs_shape[1]), (0, 0)), 'reflect')
            if self.imgs_shape[2] < self.resize_dim[1]:  # for y
                imgs = np.pad(imgs, ((0, 0), (0, self.resize_dim[1] - self.imgs_shape[2])), 'reflect')

        # starting indices of patches
        self.X_start = np.linspace(0, self.imgs_shape[1] - self.resize_dim[0], self.N_x).astype('uint16')
        self.Y_start = np.linspace(0, self.imgs_shape[2] - self.resize_dim[1], self.N_y).astype('uint16')

        # split in resize_dim
        n = 0
        if self.imgs_shape[0] > 1:
            for i, img in enumerate(imgs):
                for j in range(self.N_x):
                    for k in range(self.N_y):
                        patches[n, 0, :, :] = img[self.X_start[j]:self.X_start[j] + self.resize_dim[0],
                                              self.Y_start[k]:self.Y_start[k] + self.resize_dim[1]]
                        n += 1
        elif self.imgs_shape[0] == 1:
            for j in range(self.N_x):
                for k in range(self.N_y):
                    patches[n, 0, :, :] = imgs[self.X_start[j]:self.X_start[j] + self.resize_dim[0],
                                          self.Y_start[k]:self.Y_start[k] + self.resize_dim[1]]
                    n += 1
        return patches

    def predict(self, patches):
        result_patches = np.zeros(patches.shape, dtype='uint8')
        print('Predicting data ...')
        with torch.no_grad():
            for i, patch_i in enumerate(tqdm(patches)):
                patch_i = torch.from_numpy(patch_i.astype('float32') / 255).to(device).view((1, 1, self.resize_dim[0],
                                                                                             self.resize_dim[1]))
                res_i, logits_i = self.model(patch_i)
                res_i = res_i.view((1, self.resize_dim[0], self.resize_dim[1])).cpu().numpy() * 255
                result_patches[i] = res_i.astype('uint8')
                del patch_i, res_i
        return result_patches

    def stitch(self, result_patches):
        print('Stitching patches back together ...')
        # create array
        imgs_result = np.zeros((self.imgs_shape[0], np.max((self.resize_dim[0], self.imgs_shape[1]))
                                , np.max((self.resize_dim[1], self.imgs_shape[2]))), dtype='uint8')
        for i in range(self.imgs_shape[0]):
            if self.imgs_shape[0] > 1:  # if stack
                stack_result_i = np.zeros((self.N_per_img, np.max((self.resize_dim[0], self.imgs_shape[1])),
                                           np.max((self.resize_dim[1], self.imgs_shape[2]))), dtype='uint8') * np.nan
            elif self.imgs_shape[0] == 1:  # if only one image
                stack_result_i = np.zeros((self.N_per_img, np.max((self.resize_dim[0], self.imgs_shape[1])),
                                           np.max((self.resize_dim[1], self.imgs_shape[2]))), dtype='uint8') * np.nan
            n = 0
            for j in range(self.N_x):
                for k in range(self.N_y):
                    stack_result_i[n, self.X_start[j]:self.X_start[j] + self.resize_dim[0],
                    self.Y_start[k]:self.Y_start[k] + self.resize_dim[1]] = result_patches[i * self.N_per_img + n, 0, :,
                                                                            :]
                    # average overlapping regions
                    if self.imgs_shape[0] > 1:  # if stack
                        imgs_result[i] = np.nanmean(stack_result_i, axis=0)
                    elif self.imgs_shape[0] == 1:  # if only one image
                        imgs_result = np.nanmean(stack_result_i, axis=0)
                    n += 1
            del stack_result_i

        # change to input size (if zero padding)
        if self.imgs_shape[0] > 1:  # if stack
            imgs_result = imgs_result[:, :self.imgs_shape[1], :self.imgs_shape[2]]
        elif self.imgs_shape[0] == 1:  # if only one image
            imgs_result = imgs_result[:self.imgs_shape[1], :self.imgs_shape[2]]

        return imgs_result

    def save_as_tif(self, imgs, filename, normalize=False):
        if normalize:
            imgs = imgs.astype('float32')
            imgs = imgs - np.nanmin(imgs)
            imgs /= np.nanmax(imgs)
            imgs *= 255
        imgs = imgs.astype('uint8')
        tifffile.imsave(filename, imgs)
        print('Saving prediction results as %s' % filename)

