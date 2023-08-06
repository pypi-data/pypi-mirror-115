import sys
from PySide2.QtWidgets import*
from PySide2.QtGui import*
from PIL import Image, ImageQt

from NightWindGameLib.Qt.UIRGB import Ui_RGB
from NightWindGameLib.Qt.fixQt import FixPySide2
fix = FixPySide2()
fix.start_fix()


class RGB(QMainWindow, Ui_RGB):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup()
        self.show()

    def setup(self):
        self.slider_b.valueChanged.connect(self.process)
        self.slider_r.valueChanged.connect(self.process)
        self.slider_g.valueChanged.connect(self.process)
        self.label.setScaledContents(True)

    def process(self):
        value_r = self.slider_r.value()
        value_g = self.slider_g.value()
        value_b = self.slider_b.value()
        self.label_b.setText(str(value_b))
        self.label_g.setText(str(value_g))
        self.label_r.setText(str(value_r))
        rgb = (value_r, value_g, value_b)
        self.lineEdit.setText(str(rgb))
        img = Image.new("RGBA", (100, 100), rgb)
        img = ImageQt.ImageQt(img)
        img = QPixmap.fromImage(img)
        self.label.setPixmap(img)


def main():
    app = QApplication(sys.argv)
    window = RGB()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
