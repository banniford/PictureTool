from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QMainWindow, QFileDialog
import ui.picturetoolUI as UI


class PictureTool(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = UI.Ui_MainWindow()
        self.main_ui.setupUi(self)

        self.main_ui.lineEdit.setValidator(QIntValidator(0, 100))
        self.main_ui.lineEdit.setText("50")

        self.FontColor={"红色":"red","黑色":"black"}
        self.FontPosition={"右上角":0,"右下角":1,"左上角":2,"左下角":3}

        self.main_ui.pushButton.clicked.connect(self.LoadDir)
        self.main_ui.pushButton_2.clicked.connect(self.LoadFile)
        self.main_ui.start.clicked.connect(self.start)

    def LoadDir(self):
        directory = QFileDialog.getExistingDirectory(self, "选取文件夹")  # 起始路径
        self.main_ui.label_3.setText(directory)

    def LoadFile(self):
        openfile_name = QFileDialog.getOpenFileName(self, '选择文件', '', 'Excel files(*.xlsx , *.xls)')
        print(openfile_name)
        self.main_ui.label_4.setText(openfile_name[0])

    def start(self):
        print(self.main_ui.lineEdit.text())
