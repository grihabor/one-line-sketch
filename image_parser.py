import scipy
from scipy.signal import argrelextrema
from skimage.color import rgb2gray
from skimage.filters import sobel
from skimage.filters import threshold_adaptive
from skimage.filters import threshold_otsu
from skimage.io import imread
import matplotlib.pyplot as plt
import numpy as np

from utils import smooth, find_nearest_index


class ImageParser:
    def __init__(self):
        self._matrix = None

    def parse(self, filename):
        img = imread(filename)
        img = rgb2gray(img)
        #print(img.shape)
        #img = threshold_adaptive(img, 51)
        img = sobel(img)
        row_sum = np.sum(img, axis=1)
        #print(len(row_sum), row_sum)

        plt.subplot(121)
        row_sum = smooth(row_sum, 11)


        plt.plot(row_sum)



        max_indices = argrelextrema(row_sum, np.greater)[0]


        middle_point = img.shape[0] // 2
        index = find_nearest_index(max_indices, middle_point)
        print(max_indices)
        print(index)
        diff = np.roll(max_indices, -1) - max_indices
        print(diff)
        print(diff[index])

        start_i, end_i = index, index
        threshold = diff[index] * 0.3
        while np.abs(diff[start_i] - diff[index]) < threshold:
            start_i -= 1
        while np.abs(diff[end_i] - diff[index]) < threshold:
            end_i += 1

        max_indices = max_indices[start_i+1:end_i+1]

        plt.scatter(max_indices, np.ones(len(max_indices)), c='r')

        plt.subplot(122)
        plt.imshow(img)
        #print(img)
        plt.show()

    @property
    def matrix(self):
        if self._matrix is None:
            raise AttributeError('Call parse function before using the matrix')
        return self._matrix
