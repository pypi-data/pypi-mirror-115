import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from sympy import *
from sympy.abc import*

from NightWindGameLib.Qt.fixQt import FixPySide2
from NightWindGameLib.Qt.UICalculator import Ui_Calculator

fix = FixPySide2()
fix.start_fix()


def get_prime_factor(num):
    number = num
    List = []
    if num >= 2:
        while number > 1:
            for i in range(2, number + 1):
                while number % i == 0:
                    number = number // i
                    List.append(str(i))
    return List


# 多功能数学计算器
class Calculator(QMainWindow, Ui_Calculator):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.expressions = []
        self.expression = None
        self.mode = None
        self.pbtn_start.clicked.connect(self.get_expression)
        self.show()

    # 获取输入的式子
    def get_expression(self):
        try:
            if self.le_input.text() != "":
                self.expressions = str(self.le_input.text()).split(",")
                self.start_calculate()
            else:
                QMessageBox.warning(self, "注意", "你没有输入数学式，请重新输入")
        except TypeError:
            # print(self.expressions)
            if self.le_input.text() != "":
                QMessageBox.warning(self, "注意", "输入有误")

    # 开始运算
    def start_calculate(self):
        QApplication.processEvents()
        self.expression = eval(str(self.expressions[0]))
        self.mode = self.cb_mode.currentText()
        if self.mode == "分解质因数":
            lst_prime = "*".join(get_prime_factor(self.expression))
            string = ""
            for i in lst_prime:
                string += i
            self.tb_result.setText(str(self.expression) + " = " + string)

        elif self.mode == "多项式展开":
            self.tb_result.setText(str(self.expression) + " = " +
                                   str(expand(self.expression)))

        elif self.mode == "多项式因式分解":
            self.tb_result.setText(str(self.expression) + " = " +
                                   str(factor(self.expression)))

        elif self.mode == "分式通分":
            self.tb_result.setText(str(self.expression) + " = " +
                                   str(together(self.expression)))

        elif self.mode == "绘制函数图像":
            pass

        elif self.mode == "求解方程/方程组":
            pass

        elif self.mode == "整式大除法":
            pass

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.get_expression()


# 开始运行
def main():
    app = QApplication(sys.argv)
    window = Calculator()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
