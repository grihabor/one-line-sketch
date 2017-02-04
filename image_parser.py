from skimage.io import imread
import matplotlib.pyplot as plt


class ImageParser:
    def __init__(self):
        self._matrix = None

    def parse(self, filename):
        img = imread(filename)
        plt.imshow(img)

    @property
    def matrix(self):
        if self._matrix is None:
            raise AttributeError('Call parse function before using the matrix')
        return self._matrix
