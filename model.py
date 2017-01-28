

class Cell:
    def __init__(self, left, top, right, bottom, status=0):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.status = status


class Model:
    def __init__(self, cell_list):
        self.cell_list = cell_list

    @classmethod
    def from_matrix(cls, matrix):
        pass

    @classmethod
    def from_textfile(cls, filename):
        matrix = []
        for line in filename:
            matrix.append([int(item) for item in line.split()])
        return Model.from_matrix(matrix)

    @classmethod
    def from_image(cls, filename):
        pass
