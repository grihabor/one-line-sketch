from sketch_model import SketchModel

DATA_PATH = 'data'
TXT_DATA_PATH = DATA_PATH + '/txt'
IMG_DATA_PATH = DATA_PATH + '/img'


def main():
    model = SketchModel.from_textfile(IMG_DATA_PATH + '/expert/rose.txt')
    #model.draw()
    model.solve()


if __name__ == '__main__':
    main()
