import scipy
from skimage.color import rgb2gray
from skimage.filters import sobel
from skimage.filters import threshold_adaptive
from skimage.filters import threshold_otsu
from skimage.io import imread
import matplotlib.pyplot as plt
import numpy as np

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
        print(len(row_sum), row_sum)

        plt.subplot(121)
        plt.plot(row_sum)



        plt.subplot(122)
        plt.imshow(img)
        print(img)
        plt.show()

    @property
    def matrix(self):
        if self._matrix is None:
            raise AttributeError('Call parse function before using the matrix')
        return self._matrix
