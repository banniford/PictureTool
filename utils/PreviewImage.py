import random

from utils.ImageAddText import ImageAddText
from PyQt5.QtCore import QThread


class PreviewImage(QThread):
    def __init__(self):
        QThread.__init__(self)
    def set_arguments(self, imagePath, ListStr,select, color, text_size, position):
        self.imagePath = imagePath
        self.ListStr = ListStr
        self.color = color
        self.text_size = text_size
        self.position = position
        self.select = select

    def get_key(self,dict, value):
        for k, v in dict.items():
            if v == value:
                return k
    def run(self):
        if self.select=="随机":
            index = random.randint(1, len(self.ListStr)-1)
            img = ImageAddText(self.imagePath[index],
                               self.ListStr[index],
                               self.color,
                               self.text_size,
                               self.position)
            img.show()
        else:
            img = ImageAddText(self.imagePath[self.get_key(self.ListStr,self.select)],
                               self.ListStr[self.get_key(self.ListStr,self.select)],
                               self.color,
                               self.text_size,
                               self.position)
            img.show()

