import scipy
from scipy.signal import argrelextrema
from skimage.color import rgb2gray
from skimage.filters import sobel
from skimage.filters import threshold_adaptive
from skimage.filters import threshold_otsu
from skimage.io import imread
import matplotlib.pyplot as plt
import numpy as np

from utils import smooth, find_nearest_value_index


class ImageParser:
    def __init__(self):
        self._matrix = None  # type: list[list[int]]
        self.img = None  # type: np.ndarray
        self._threshold_range = 0.3

    @property
    def _smooth_param(self):
        if self.img is None:
            raise AttributeError('Initialize self.img before using _smooth_param')
        return self.img.shape[0] // 115
        
    def _get_rows(self, grayscale_img, draw_plots=False):
        gradient_magnitude = sobel(grayscale_img)
        # sum up rows of gradients, so that local maximas
        # of resulting arrays are equal cell rows coordinates
        gradient_y_projection = np.sum(gradient_magnitude, axis=1)
        # smooth the array to get nice local maximas
        gradient_y_projection = smooth(gradient_y_projection, self._smooth_param)

        local_max_indices = argrelextrema(gradient_y_projection, np.greater)[0]
        height_middle = gradient_magnitude.shape[0] // 2
        index = find_nearest_value_index(local_max_indices, height_middle)
        diff = np.roll(local_max_indices, -1) - local_max_indices

        start_i, end_i = index, index
        threshold = diff[index] * self._threshold_range
        while np.abs(diff[start_i] - diff[index]) < threshold:
            start_i -= 1
        while np.abs(diff[end_i] - diff[index]) < threshold:
            end_i += 1

        local_max_indices = local_max_indices[start_i + 1:end_i + 1]

        if draw_plots:
            plt.plot(gradient_y_projection)
            plt.scatter(local_max_indices, np.ones(len(local_max_indices)), c='r')

        return local_max_indices

    def parse(self, filename):
        self.img = imread(filename)
        grayscale_img = rgb2gray(self.img)

        plt.figure(figsize=(12, 8))
        plt.subplot(131)
        rows = self._get_rows(grayscale_img, True)

        cropped_grayscale = grayscale_img[rows[0]:rows[-1], :]

        plt.subplot(132)
        plt.imshow(cropped_grayscale, cmap='gray')

        plt.subplot(133)
        plt.imshow(self.img)

        plt.show()

    @property
    def matrix(self):
        if self._matrix is None:
            raise AttributeError('Call parse function before using the matrix')
        return self._matrix
