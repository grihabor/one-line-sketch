

class Cell:
    def __init__(self, left, top, right, bottom, active=False):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.active = active


class Model:
    def __init__(self, cell_list):
        self.cell_list = cell_list

    @classmethod
    def from_matrix(cls, matrix):
        pass

    @classmethod
    def from_textfile(cls, filename):
        pass

    @classmethod
    def from_image(cls, filename):
        pass
