from sketch_model import SketchModel

DATA_PATH = 'data'
TXT_DATA_PATH = DATA_PATH + '/txt'
IMG_DATA_PATH = DATA_PATH + '/img'


def main():
    #model = SketchModel.from_textfile(TXT_DATA_PATH + '/expert/rose.txt')
    model = SketchModel.from_image(IMG_DATA_PATH + '/lesser_panda.jpg')
    #model.draw()
    model.solve()
    model.draw()

if __name__ == '__main__':
    main()
