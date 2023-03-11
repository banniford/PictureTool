import random

from utils.ImageAddText import ImageAddText
from PyQt5.QtCore import QThread


class PreviewImage(QThread):
    def __init__(self):
        QThread.__init__(self)
    def set_arguments(self, imagePath, ListStr, color, text_size, position):
        self.imagePath = imagePath
        self.ListStr = ListStr
        self.color = color
        self.text_size = text_size
        self.position = position


    def run(self):
        index = random.randint(0, len(self.ListStr))
        img = ImageAddText(self.imagePath[index],
                           self.ListStr[index],
                           self.color,
                           self.text_size,
                           self.position)
        img.show()