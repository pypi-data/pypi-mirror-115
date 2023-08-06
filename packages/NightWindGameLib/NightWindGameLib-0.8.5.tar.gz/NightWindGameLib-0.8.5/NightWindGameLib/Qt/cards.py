import sys
import os
import random
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from NightWindGameLib.Qt.UICards import Ui_Cards
from NightWindGameLib.Qt.fixQt import FixPySide2
fix = FixPySide2()
fix.start_fix()


class Cards(QMainWindow, Ui_Cards):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_button()
        self.init_img()
        self.show()
        self.clicked_num = 0
        self.match_img = {
            1: {
                "pbtn": None,
                "pbtn_img": None
            },
            2: {
                "pbtn": None,
                "pbtn_img": None
            },
        }
        self.first_clicked = True
        self.time = 0
        self.right_count = 0
        self.pbtn_img.buttonClicked.connect(self.pbtn_func)

    def init_button(self):
        pbtn_list = self.pbtn_img.buttons()
        for btn in pbtn_list:
            btn.setText("")
            btn.setIcon(QIcon("images_cards/bg.png"))
            btn.setIconSize(QSize(150, 150))
            btn.setCheckable(True)

    def init_img(self):
        image_type = ['.png', '.jpg', '.bmp', '.jpeg']
        files = os.listdir("images_cards")
        all_imgs = []
        for file in files:
            ext = os.path.splitext(file)[-1]
            if ext in image_type:
                all_imgs.append("images_cards" + os.sep + file)

        random_imgs = random.sample(all_imgs, 12)
        grid_imgs = random_imgs + random_imgs
        random.shuffle(grid_imgs)
        pbtn_list = self.pbtn_img.buttons()
        self.grids = dict(zip(pbtn_list, grid_imgs))

    def pbtn_func(self):
        if self.first_clicked:
            self.first_clicked = False
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_time)
            self.timer.start(1000)

        if self.clicked_num < 2:
            QApplication.processEvents()
            pbtn = self.pbtn_img.checkedButton()
            if pbtn != self.match_img[1]["pbtn"] and pbtn in self.pbtn_img.buttons():
                self.clicked_num += 1
                pbtn.setIcon(QIcon(self.grids[pbtn]))
                self.match_img[self.clicked_num]["pbtn"] = pbtn
                self.match_img[self.clicked_num]["pbtn_img"] = self.grids[pbtn]
                timer = QTimer()
                timer.singleShot(300, self.judge)

    def judge(self):
        if self.clicked_num == 2:
            self.clicked_num = 0
            if self.match_img[1]["pbtn_img"] != self.match_img[2]["pbtn_img"]:
                self.match_img[1]["pbtn"].setIcon(QIcon("images_cards/bg.png"))
                self.match_img[2]["pbtn"].setIcon(QIcon("images_cards/bg.png"))
            else:
                self.pbtn_img.removeButton(self.match_img[1]["pbtn"])
                self.pbtn_img.removeButton(self.match_img[2]["pbtn"])
                self.right_count += 1
                if self.right_count == 12:
                    self.timer.stop()

            self.match_img[1]["pbtn"] = self.match_img[2]["pbtn"] = None

    def update_time(self):
        self.time += 1
        self.lcd_time.display(self.time)


def main():
    app = QApplication(sys.argv)
    window = Cards()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
