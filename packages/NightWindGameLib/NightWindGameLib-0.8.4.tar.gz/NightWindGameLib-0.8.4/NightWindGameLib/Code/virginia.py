import turtle
import string
import time


class Window:
    def __init__(self):
        self.sc = turtle.Screen()
        self.rowPen = turtle.Pen()
        self.colPen = turtle.Pen()
        self.width, self.height = 864, 864
        self.letter = self.height / 27
        self.setupScreen()
        self.setupPen()
        self.letterList = list(string.ascii_lowercase + " ")

        # 创建密码变量
        self.cipherText = ""
        self.password = []

        # 输入明文
        self.plaintext = self.sc.textinput("明文", "输入你要加密的文字:")
        self.plaintextLen = len(self.plaintext)

        # 输入密钥
        self.key = self.sc.textinput("密钥", "输入你的密钥:")
        self.keyLen = len(self.key)
        self.realKey = (self.key * (self.plaintextLen // self.keyLen) +
                        self.key[:self.plaintextLen % self.keyLen])

        self.drawLine()
        self.showCipher()

    def setupScreen(self):
        self.sc.setup(self.width, self.height)
        self.sc.bgpic("images_virginia/bg.gif")

    def setupPen(self):
        self.rowPen.color("yellow")
        self.colPen.color("yellow")
        self.rowPen.speed(5)
        self.colPen.speed(5)
        self.rowPen.pensize(3)
        self.colPen.pensize(3)
        self.colPen.setheading(-90)

    def go(self, t, x, y):
        t.pu()
        t.goto(x, y)
        t.pd()

    def letterPos(self, row, col):
        self.go(t=self.rowPen, x=-self.width / 2,
                y=self.height / 2 - (1.5 + row) * self.letter)
        self.go(t=self.colPen, x=-self.width / 2 + (1.5 + col) * self.letter,
                y=self.height / 2)
        self.rowPen.fd(self.width)
        self.colPen.fd(self.height)

    def drawLine(self):
        for i in range(26):
            lst = list(self.letterList[i:] + self.letterList[:i])
            self.password.append(lst)

        for i in range(self.plaintextLen):
            if self.plaintext[i] != " ":
                rowIndex = self.letterList.index(self.plaintext[i])
                colIndex = self.letterList.index(self.realKey[i])
                self.letterPos(rowIndex, colIndex)
                text = self.password[rowIndex][colIndex]
                self.cipherText += text
            else:
                self.cipherText += " "

    def showCipher(self):
        time.sleep(3)
        self.sc.clear()
        p = turtle.Pen()
        p.ht()
        self.go(p, 0, 0)
        p.pencolor("green")
        p.write(self.cipherText, align="center", font=("Arial", 40, "bold"))


if __name__ == '__main__':
    Window()
    turtle.done()
