from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.Open_BTN = QPushButton(self.centralwidget)
        self.Open_BTN.setObjectName(u"Open_BTN")
        self.Open_BTN.setGeometry(QRect(100, 130, 92, 28))
        self.if_open = QLabel(self.centralwidget)
        self.if_open.setObjectName(u"if_open")
        self.if_open.setGeometry(QRect(330, 170, 91, 21))
        self.if_open.setAlignment(Qt.AlignCenter)
        self.R_Slider = QSlider(self.centralwidget)
        self.R_Slider.setObjectName(u"R_Slider")
        self.R_Slider.setGeometry(QRect(220, 210, 391, 21))
        self.R_Slider.setMinimum(-255)
        self.R_Slider.setMaximum(255)
        self.R_Slider.setOrientation(Qt.Horizontal)
        self.G_Slider = QSlider(self.centralwidget)
        self.G_Slider.setObjectName(u"G_Slider")
        self.G_Slider.setGeometry(QRect(220, 250, 391, 21))
        self.G_Slider.setMinimum(-255)
        self.G_Slider.setMaximum(255)
        self.G_Slider.setOrientation(Qt.Horizontal)
        self.B_Slider = QSlider(self.centralwidget)
        self.B_Slider.setObjectName(u"B_Slider")
        self.B_Slider.setGeometry(QRect(220, 290, 391, 21))
        self.B_Slider.setMinimum(-255)
        self.B_Slider.setMaximum(255)
        self.B_Slider.setOrientation(Qt.Horizontal)
        self.R_label = QLabel(self.centralwidget)
        self.R_label.setObjectName(u"R_label")
        self.R_label.setGeometry(QRect(120, 210, 72, 15))
        self.G_label = QLabel(self.centralwidget)
        self.G_label.setObjectName(u"G_label")
        self.G_label.setGeometry(QRect(120, 250, 72, 15))
        self.B_label = QLabel(self.centralwidget)
        self.B_label.setObjectName(u"B_label")
        self.B_label.setGeometry(QRect(120, 290, 72, 15))
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(110, 490, 561, 23))
        self.progressBar.setValue(0)
        self.Render_BTN = QPushButton(self.centralwidget)
        self.Render_BTN.setObjectName(u"Render_BTN")
        self.Render_BTN.setGeometry(QRect(190, 430, 91, 31))
        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(570, 130, 181, 31))
        self.Contrast_Slider = QSlider(self.centralwidget)
        self.Contrast_Slider.setObjectName(u"Contrast_Slider")
        self.Contrast_Slider.setGeometry(QRect(220, 330, 391, 21))
        self.Contrast_Slider.setMinimum(0)
        self.Contrast_Slider.setMaximum(3000)
        self.Contrast_Slider.setValue(1000)
        self.Contrast_Slider.setOrientation(Qt.Horizontal)
        self.Contrast = QLabel(self.centralwidget)
        self.Contrast.setObjectName(u"Contrast")
        self.Contrast.setGeometry(QRect(120, 330, 72, 15))
        self.Brightness_Slider = QSlider(self.centralwidget)
        self.Brightness_Slider.setObjectName(u"Brightness_Slider")
        self.Brightness_Slider.setGeometry(QRect(220, 370, 391, 21))
        self.Brightness_Slider.setMinimum(0)
        self.Brightness_Slider.setMaximum(3000)
        self.Brightness_Slider.setValue(1000)
        self.Brightness_Slider.setOrientation(Qt.Horizontal)
        self.Brightness = QLabel(self.centralwidget)
        self.Brightness.setObjectName(u"Brightness")
        self.Brightness.setGeometry(QRect(120, 370, 81, 16))
        self.Save_BTN = QPushButton(self.centralwidget)
        self.Save_BTN.setObjectName(u"Save_BTN")
        self.Save_BTN.setGeometry(QRect(450, 430, 91, 31))
        self.title_label = QLabel(self.centralwidget)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setGeometry(QRect(240, 120, 301, 41))
        font = QFont()
        font.setPointSize(16)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignCenter)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow",
                                                             u"MainWindow", None))
        self.Open_BTN.setText(QCoreApplication.translate("MainWindow",
                                                         u"\u6253\u5f00\u56fe\u7247", None))
        self.if_open.setText("")
        self.R_label.setText(QCoreApplication.translate("MainWindow",
                                                        u"\u7ea2\u8272(R)", None))
        self.G_label.setText(QCoreApplication.translate("MainWindow",
                                                        u"\u7eff\u8272(G)", None))
        self.B_label.setText(
            QCoreApplication.translate("MainWindow",
                                       u"\u84dd\u8272(B)", None))
        self.Render_BTN.setText(
            QCoreApplication.translate("MainWindow",
                                       u"\u5f00\u59cb\u6e32\u67d3", None))
        self.checkBox.setText(
            QCoreApplication.translate("MainWindow",
                                       u"\u80f6\u5377\u6a21\u5f0f", None))
        self.Contrast.setText(QCoreApplication.translate("MainWindow",
                                                         u"\u5bf9\u6bd4\u5ea6", None))
        self.Brightness.setText(QCoreApplication.translate("MainWindow",
                                                           u"\u660e\u4eae\u5ea6", None))
        self.Save_BTN.setText(QCoreApplication.translate("MainWindow",
                                                         u"\u4fdd\u5b58\u56fe\u7247", None))
        self.title_label.setText(
            QCoreApplication.translate("MainWindow",
                                       u"\u56fe\u7247\u6e32\u67d3\u5c0f\u5de5\u5177", None))
    # retranslateUi
