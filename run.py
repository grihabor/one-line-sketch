from solver import Solver
from model import Model


def main():
    model = Model.from_textfile('data/data.txt')
    model.draw()
    solver = Solver()


if __name__ == '__main__':
    main()
