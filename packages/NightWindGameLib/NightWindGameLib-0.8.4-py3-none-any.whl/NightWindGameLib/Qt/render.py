from PIL import Image, ImageOps, ImageEnhance
import sys
from PySide2.QtWidgets import*

from NightWindGameLib.Qt.UIRender import Ui_MainWindow
from NightWindGameLib.Qt.fixQt import FixPySide2
fix = FixPySide2()
fix.start_fix()


class RenderPicture(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup()
        self.show()
        self.data_file = None
        self.save_file = None
        self.pic = None

    def setup(self):
        self.Open_BTN.clicked.connect(self.open_pic)
        self.Render_BTN.clicked.connect(self.render_pic)
        self.Save_BTN.clicked.connect(self.save_pic)

    def open_pic(self):
        self.data_file, _ = QFileDialog.getOpenFileName(caption="选择图片文件",
                                                        filter="(*.jpg *.png *.jpeg)")
        if self.data_file:
            self.if_open.setText("获取成功!")
        else:
            QMessageBox.warning(self, "注意", "没有打开图片!")

    def save_pic(self):
        self.save_file, _ = QFileDialog.getSaveFileName(caption="保存图片文件",
                                                        filter="(*.png *.jpg *.jpeg)")
        if self.pic:
            self.pic.save(self.save_file)
        else:
            QMessageBox.warning(self, "注意", "没有图片可保存!")

    def render_pic(self):
        if self.data_file:
            self.pic = Image.open(self.data_file).convert("RGB")
            if self.checkBox.isChecked():
                self.pic = ImageOps.invert(self.pic)

            r = self.R_Slider.value()
            g = self.G_Slider.value()
            b = self.B_Slider.value()
            old = 0
            width, height = self.pic.size
            for y in range(height):
                for x in range(width):
                    value = list(self.pic.getpixel((x, y)))
                    value[0] += r
                    value[1] += g
                    value[2] += b
                    self.pic.putpixel((x, y), tuple(value))
                process = int((y+1)*100 / height)
                if process != old:
                    self.progressBar.setValue(process)
                    old = process
            Con = self.Contrast_Slider.value()
            self.pic = ImageEnhance.Contrast(self.pic).enhance(Con / 1000)
            Bri = self.Brightness_Slider.value()
            self.pic = ImageEnhance.Brightness(self.pic).enhance(Bri / 1000)
            self.pic.show()


def main():
    app = QApplication(sys.argv)
    window = RenderPicture()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

