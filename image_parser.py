import scipy
from scipy.signal import argrelextrema
from skimage.color import rgb2gray
from skimage.filters import sobel
from skimage.filters import threshold_adaptive
from skimage.filters import threshold_otsu
from skimage.io import imread
import matplotlib.pyplot as plt
import numpy as np

from utils import smooth, find_nearest_value_index, lax_compare, get_local_maximas


class ImageParser:
    def __init__(self):
        self._matrix = None  # type: list[list[int]]
        self.img = None  # type: np.ndarray
        self._threshold = None
        self._threshold_range = 0.3

    def _smooth_param(self, img_size):
        return img_size // 65

    def threshold(self, cell_size=None):
        if cell_size is None:
            if self._threshold is None:
                raise AttributeError('Pass to threshold() a cell_size before using it without one')
        else:
            self._threshold = cell_size * self._threshold_range
        return self._threshold

    def _get_rows(self, grayscale_img, draw_plots=False):
        gradient_magnitude = sobel(grayscale_img)
        # sum up rows of gradients, so that local maximas
        # of resulting arrays are equal cell rows coordinates
        gradient_y_projection = np.sum(gradient_magnitude, axis=1)


        local_max_indices = get_local_maximas(gradient_y_projection,
                                              self._smooth_param(grayscale_img.shape[1]))

        height_middle = gradient_magnitude.shape[0] // 2
        index = find_nearest_value_index(local_max_indices, height_middle)
        diff = np.roll(local_max_indices, -1) - local_max_indices

        def rows_range():
            start_i, end_i = 0, 0
            threshold = self.threshold(diff[index])

            gen = reversed(list(enumerate(diff[:index])))
            for i, diff_item in gen:
                if np.abs(diff_item - diff[index]) > threshold:
                    start_i = i + 1
                    break

            gen = enumerate(diff[index+1:], start=index+1)
            for i, diff_item in gen:
                if np.abs(diff_item - diff[index]) > threshold:
                    end_i = i
                    break

            return start_i, end_i

        start_i, end_i = rows_range()

        rows = local_max_indices[start_i:end_i+1]

        if draw_plots:
            plt.plot(gradient_y_projection)
            plt.scatter(rows, np.ones(len(rows)), c='r')
            plt.scatter(local_max_indices, 4*np.ones(len(local_max_indices)), c='g')

        return rows

    def _get_columns(self, grayscale, draw_plots=False):
        return self._get_rows(np.transpose(grayscale), draw_plots)

    def parse(self, filename):
        self.img = imread(filename)
        grayscale_img = rgb2gray(self.img)

        plt.figure(figsize=(12, 8))
        plt.subplot(221)
        rows = self._get_rows(grayscale_img, True)

        cropped_grayscale = grayscale_img[rows[0] - self.threshold() : rows[-1] + self.threshold(), :]

        plt.subplot(222)
        plt.imshow(cropped_grayscale, cmap='gray')

        plt.subplot(223)
        columns = self._get_columns(cropped_grayscale, True)

        plt.subplot(224)
        plt.imshow(self.img)

        plt.show()

    @property
    def matrix(self):
        if self._matrix is None:
            raise AttributeError('Call parse function before using the matrix')
        return self._matrix
