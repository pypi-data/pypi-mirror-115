from PySide2.QtCore import *
from PySide2.QtWidgets import *



class Ui_Cards(object):
    def setupUi(self, Cards):
        if not Cards.objectName():
            Cards.setObjectName(u"Cards")
        Cards.resize(1040, 793)
        self.centralwidget = QWidget(Cards)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 110, 1011, 621))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.pbtn07 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img = QButtonGroup(Cards)
        self.pbtn_img.setObjectName(u"pbtn_img")
        self.pbtn_img.addButton(self.pbtn07)
        self.pbtn07.setObjectName(u"pbtn07")

        self.gridLayout.addWidget(self.pbtn07, 1, 2, 1, 1)

        self.pbtn11 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn11)
        self.pbtn11.setObjectName(u"pbtn11")

        self.gridLayout.addWidget(self.pbtn11, 2, 2, 1, 1)

        self.pbtn13 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn13)
        self.pbtn13.setObjectName(u"pbtn13")

        self.gridLayout.addWidget(self.pbtn13, 0, 4, 1, 1)

        self.pbtn03 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn03)
        self.pbtn03.setObjectName(u"pbtn03")

        self.gridLayout.addWidget(self.pbtn03, 0, 2, 1, 1)

        self.pbtn18 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn18)
        self.pbtn18.setObjectName(u"pbtn18")

        self.gridLayout.addWidget(self.pbtn18, 3, 0, 1, 1)

        self.pbtn17 = QPushButton(self.gridLayoutWidget)
        self.pbtn17.setObjectName(u"pbtn17")
        self.pbtn_img.addButton(self.pbtn17)

        self.gridLayout.addWidget(self.pbtn17, 2, 4, 1, 1)

        self.pbtn08 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn08)
        self.pbtn08.setObjectName(u"pbtn08")

        self.gridLayout.addWidget(self.pbtn08, 1, 3, 1, 1)

        self.pbtn10 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn10)
        self.pbtn10.setObjectName(u"pbtn10")

        self.gridLayout.addWidget(self.pbtn10, 2, 1, 1, 1)

        self.pbtn12 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn12)
        self.pbtn12.setObjectName(u"pbtn12")

        self.gridLayout.addWidget(self.pbtn12, 2, 3, 1, 1)

        self.pbtn19 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn19)
        self.pbtn19.setObjectName(u"pbtn19")

        self.gridLayout.addWidget(self.pbtn19, 3, 1, 1, 1)

        self.pbtn02 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn02)
        self.pbtn02.setObjectName(u"pbtn02")

        self.gridLayout.addWidget(self.pbtn02, 0, 1, 1, 1)

        self.pbtn05 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn05)
        self.pbtn05.setObjectName(u"pbtn05")

        self.gridLayout.addWidget(self.pbtn05, 1, 0, 1, 1)

        self.pbtn21 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn21)
        self.pbtn21.setObjectName(u"pbtn21")

        self.gridLayout.addWidget(self.pbtn21, 3, 3, 1, 1)

        self.pbtn20 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn20)
        self.pbtn20.setObjectName(u"pbtn20")

        self.gridLayout.addWidget(self.pbtn20, 3, 2, 1, 1)

        self.pbtn09 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn09)
        self.pbtn09.setObjectName(u"pbtn09")

        self.gridLayout.addWidget(self.pbtn09, 2, 0, 1, 1)

        self.pbtn06 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn06)
        self.pbtn06.setObjectName(u"pbtn06")

        self.gridLayout.addWidget(self.pbtn06, 1, 1, 1, 1)

        self.pbtn24 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn24)
        self.pbtn24.setObjectName(u"pbtn24")

        self.gridLayout.addWidget(self.pbtn24, 1, 4, 1, 1)

        self.pbtn04 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn04)
        self.pbtn04.setObjectName(u"pbtn04")

        self.gridLayout.addWidget(self.pbtn04, 0, 3, 1, 1)

        self.pbtn22 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn22)
        self.pbtn22.setObjectName(u"pbtn22")

        self.gridLayout.addWidget(self.pbtn22, 3, 4, 1, 1)

        self.pbtn01 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn01)
        self.pbtn01.setObjectName(u"pbtn01")

        self.gridLayout.addWidget(self.pbtn01, 0, 0, 1, 1)

        self.pbtn23 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn23)
        self.pbtn23.setObjectName(u"pbtn23")

        self.gridLayout.addWidget(self.pbtn23, 0, 5, 1, 1)

        self.pbtn14 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn14)
        self.pbtn14.setObjectName(u"pbtn14")

        self.gridLayout.addWidget(self.pbtn14, 1, 5, 1, 1)

        self.pbtn15 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn15)
        self.pbtn15.setObjectName(u"pbtn15")

        self.gridLayout.addWidget(self.pbtn15, 2, 5, 1, 1)

        self.pbtn16 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn16)
        self.pbtn16.setObjectName(u"pbtn16")

        self.gridLayout.addWidget(self.pbtn16, 3, 5, 1, 1)

        self.lcd_time = QLCDNumber(self.centralwidget)
        self.lcd_time.setObjectName(u"lcd_time")
        self.lcd_time.setGeometry(QRect(390, 10, 221, 91))
        Cards.setCentralWidget(self.centralwidget)

        self.retranslateUi(Cards)

        QMetaObject.connectSlotsByName(Cards)
    # setupUi

    def retranslateUi(self, Cards):
        Cards.setWindowTitle(
            QCoreApplication.translate("Cards", u"\u8bb0\u5fc6\u7ffb\u724c", None))
        self.pbtn07.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn11.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn13.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn03.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn18.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn17.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn08.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn10.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn12.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn19.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn02.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn05.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn21.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn20.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn09.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn06.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn24.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn04.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn22.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn01.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn23.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn14.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn15.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn16.setText(QCoreApplication.translate("Cards", u"PushButton", None))
    # retranslateUi
