from PIL import Image
import numpy as np
import random


class ImageCipher:
    def __init__(self):
        self.keys = []
        self.picList = []
        self.width = 0
        self.height = 0

    def PicToList(self, path):
        pic = Image.open(path).convert("RGB")
        self.width, self.height = pic.size
        pic_array = np.array(pic)
        self.picList = pic_array.tolist()
        return self.picList

    def ListToPic(self, picList):
        en_array = np.array(picList)
        EnPic = Image.fromarray(np.uint8(en_array))
        return EnPic

    def getKey(self, row, col):
        for i in range(row):
            self.keys.append(random.randint(1, col))

        return self.keys

    def Encryption(self, picture, width, height):
        self.keys = self.getKey(width, height)

        for i in range(height):
            key = self.keys[i]
            listA = picture[i][:key]
            listB = picture[i][key:]

            picture[i][:width - key] = listB
            picture[i][width - key:] = listA

        return picture, self.keys

    def Decryption(self, pic_list, width, height, keyList):
        for i in range(height):
            key = keyList[i]
            listA = pic_list[i][:width - key]
            listB = pic_list[i][width - key:]

            pic_list[i][:key] = listB
            pic_list[i][key:] = listA

        return pic_list


if __name__ == "__main__":
    img = ImageCipher()

    # 加密
    pic_list = img.PicToList("图片.png")
    en_list, key = img.Encryption(pic_list, img.width, img.height)
    en_pic = img.ListToPic(en_list)
    en_pic.save("加密.png")

    # 解密
    de_pic = img.PicToList("加密.png")
    DePicList = img.Decryption(de_pic, img.width, img.height, key)
    decrypted_pic = img.ListToPic(DePicList)
    decrypted_pic.save("解密后.png")
