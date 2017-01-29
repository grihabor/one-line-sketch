from sketch_model import SketchModel


def main():
    model = SketchModel.from_textfile('data/beginner/apple.txt')
    #model.draw()
    model.solve()


if __name__ == '__main__':
    main()
