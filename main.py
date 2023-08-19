
import sys

from HandleFunc import PictureTool
from PyQt5.QtWidgets import QApplication

# 注意修改./ui/picturetoolUI.py 文件中.ico的路径为 ./ 以main文件为起始地址
if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = PictureTool()
    Window.show()
    sys.exit(app.exec_())