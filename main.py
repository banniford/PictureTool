
import sys

from HandleFunc import PictureTool
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = PictureTool()
    Window.show()
    sys.exit(app.exec_())