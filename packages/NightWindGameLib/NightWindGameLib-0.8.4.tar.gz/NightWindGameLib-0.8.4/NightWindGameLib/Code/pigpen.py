from arcade import *
from arcade import color, key
import string

WIDTH = 1000
HEIGHT = 400
TITLE = "信件加密器"


class Pigpen(Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        set_background_color(color.WHITE)
        self.words = string.ascii_lowercase + " "
        self.img = Sprite("images_pigpen/space.png")
        self.wordlist = SpriteList()
        self.x = 0
        self.y = HEIGHT
        self.current = 1

    def on_draw(self):
        start_render()
        self.img.draw()
        self.wordlist.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        try:
            word = chr(symbol)

            if len(self.wordlist) == 40:
                print("输入字符已达上限！")

            else:
                if word in self.words:
                    if symbol == key.SPACE:
                        img = Sprite("images_pigpen/space.png")
                    else:
                        img = Sprite(f"images_pigpen/{word}.png")

                    img.center_x = WIDTH // 2
                    img.center_y = HEIGHT // 2
                    img.left = self.x
                    img.top = self.y
                    self.wordlist.append(img)

                    if self.current == 10:
                        self.x = 0
                        self.y -= 100
                        self.current = 1
                    else:
                        self.x += 100
                        self.current += 1

            if symbol == key.BACKSPACE:
                if self.wordlist:
                    self.wordlist.pop()

                    if self.current == 1:
                        self.x = 900
                        self.y += 100
                        self.current = 10
                    else:
                        self.x -= 100
                        self.current -= 1

            if symbol == key.RETURN:
                picture = get_image(0, 0, WIDTH, HEIGHT)
                picture.save("images_pigpen/screenshot.png", "PNG")
                print("密信生成完毕!")

        except OverflowError:
            pass


if __name__ == '__main__':
    game = Pigpen(WIDTH, HEIGHT, TITLE)
    run()
