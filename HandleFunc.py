import xlrd
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QMainWindow, QFileDialog
import ui.picturetoolUI as UI
from PIL import Image, ImageDraw, ImageFont
import warnings
warnings.filterwarnings("ignore")

class PictureTool(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = UI.Ui_MainWindow()
        self.main_ui.setupUi(self)

        self.main_ui.lineEdit.setValidator(QIntValidator(0, 100))
        self.main_ui.lineEdit.setText("80")

        self.FontColor={"红色": (255, 0, 0),"黑色":(0,0,0)}
        self.FontPosition={"右上角": "right","右下角": "right","左上角": "left","左下角":"left"}

        self.xlsx = None

        self.main_ui.pushButton.clicked.connect(self.LoadDir)
        self.main_ui.pushButton_2.clicked.connect(self.LoadFile)
        self.main_ui.start.clicked.connect(self.start)

    def LoadDir(self):
        directory = QFileDialog.getExistingDirectory(self, "选取文件夹")  # 起始路径
        print(directory)
        self.main_ui.label_3.setText(directory)

    def LoadFile(self):
        self.xlsx = None
        openfile_name = QFileDialog.getOpenFileName(self, '选择文件', '', 'Excel files(*.xlsx , *.xls)')
        print(openfile_name)
        try:
            self.xlsx = xlrd.open_workbook(openfile_name[0]).sheet_by_name("信息录入")
            self.main_ui.label_4.setText(openfile_name[0])
        except:
            self.xlsx = None
            print("请检查表格是否损坏，该表格中 “信息录入”表 是否存在")



    def start(self):
        print(self.main_ui.lineEdit.text())

    def LoadXlsx(self):
        pass

    def image_add_text(self,img_path, text, text_color, text_size, position):
        img = Image.open(img_path)
        # 创建一个可以在给定图像上绘图的对象
        draw = ImageDraw.Draw(img)
        # 字体的格式 这里的SimHei.ttf需要有这个字体
        fontStyle = ImageFont.truetype("./assets/font/simhei.ttf", text_size, encoding="utf-8")
        # 计算坐标
        if position=="右下角":
            left = img.size[0]-draw.textsize(text,font=fontStyle)[0]-30
            top = img.size[1]-draw.textsize(text,font=fontStyle)[1]-30
        elif position=="左下角":
            left = 30
            top = img.size[1]-draw.textsize(text,font=fontStyle)[1]-30
        elif position=="左上角":
            left = 30
            top = 30
        else:
            # 默认"右上角"
            left = img.size[0] - draw.textsize(text, font=fontStyle)[0] - 30
            top = 30
        # 绘制文本
        draw.text((left, top), text, text_color, font=fontStyle,align=self.FontPosition[position])
        return img

