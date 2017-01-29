from sketch_model import SketchModel


def main():
    model = SketchModel.from_textfile('data/expert/headset.txt')
    #model.draw()
    model.solve()


if __name__ == '__main__':
    main()
