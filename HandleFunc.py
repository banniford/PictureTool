import os
import shutil
from os import listdir
from os.path import join
import random
import xlrd
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QMainWindow, QFileDialog
import ui.picturetoolUI as UI
from PIL import Image, ImageDraw, ImageFont
import warnings

from BatchProgram import BatchProgram

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
        # 需要读取的列
        self.xlsxPoistion=[0,1,8,9]
        # 起始行
        self.startNrows=2

        self.xlsx = None
        self.imagePath=[]
        self.ListStr=[]
        self.output=""

        self.BatchProgram=BatchProgram()
        self.BatchProgram.msg.connect(self.BatchProgram_msg)
        self.BatchProgram.finish.connect(self.Finish)
        self.main_ui.stopbutton.setEnabled(False)
        self.main_ui.pushButton.clicked.connect(self.LoadDir)
        self.main_ui.pushButton_2.clicked.connect(self.LoadXlsxFile)
        self.main_ui.startbutton.clicked.connect(self.Start)
        self.main_ui.previewbutton.clicked.connect(self.PreviewImage)
        self.main_ui.stopbutton.clicked.connect(self.Stop)
        self.main_ui.deletebutton.clicked.connect(self.DeleteDir)

        # 判断文件是否是图片

    def IsImageFile(self, filename):
        return any(filename.endswith(extension) for extension in ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG'])

    def LoadDir(self):
        directory = QFileDialog.getExistingDirectory(self, "选取文件夹")  # 起始路径
        self.main_ui.label_3.setText(directory)
        if  directory!="":
            self.imagePath = [join(directory, x) for x in listdir(directory) if self.IsImageFile(x)]
            if len(self.imagePath)==0:
                self.main_ui.textEdit.append("请检查文件夹中是否有图片")
            else:
                self.output = directory+"(带水印)"

    def Mkdir(self):
        if os.path.exists(self.output):
            return self.output
        else:
            try:
                os.mkdir(self.output)
            except:
                self.main_ui.textEdit.append("创建 "+self.output+" 文件夹失败，请手动创建")
                return ""
            return self.output

    def LoadXlsxFile(self):
        self.xlsx = None
        openfile_name = QFileDialog.getOpenFileName(self, '选择文件', '', 'Excel files(*.xlsx , *.xls)')
        if openfile_name[0]=="":
            self.ClearXlsxinfo()
            return
        try:
            self.xlsx = xlrd.open_workbook(openfile_name[0]).sheet_by_name("信息录入")
            self.main_ui.label_4.setText(openfile_name[0])
            self.Xlsx2list()
        except:
            self.ClearXlsxinfo()
            self.main_ui.textEdit.append("请检查表格是否损坏，该表格中 “信息录入”表 是否存在")


    def ClearXlsxinfo(self):
        self.main_ui.label_4.setText("")
        self.xlsx = None
        self.ListStr = []

    def Xlsx2list(self):
        self.ListStr=[]
        for i in range(self.startNrows, self.xlsx.nrows):
            tmp = ""
            if self.xlsx.cell(i, 0).value == "":
                break
            for j in self.xlsxPoistion:
                if type(self.xlsx.cell(i, j).value)==float:
                    tmp+=str(int(self.xlsx.cell(i, j).value))
                else:
                    tmp+= " "+str(self.xlsx.cell(i, j).value)
            self.ListStr.append(tmp)
        print(len(self.ListStr))
        print(len(self.imagePath))
    def ImageAddText(self,img_path, text, text_color, text_size, position):
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
        draw.text((left, top), text, text_color, font=fontStyle, align=self.FontPosition[position])
        return img

    def PreviewImage(self):
        if self.main_ui.label_3.text() == "" or self.main_ui.label_4.text() == "":
            self.main_ui.textEdit.append("请先选择 考生作品文件夹 和 考生信息表 ")
            return
        if len(self.ListStr)!=len(self.imagePath):
            self.main_ui.textEdit.append("表格数据内容与文件夹内容图片数量不匹配，请修改表格或重选文件夹")
            return
        index = random.randint(0, len(self.ListStr))
        img = self.ImageAddText(self.imagePath[index],
                           self.ListStr[index],
                           self.FontColor[self.main_ui.comboBox2.currentText()],
                           int(self.main_ui.lineEdit.text()),
                           self.main_ui.comboBox3.currentText())
        img.show()

    def BatchProgram_msg(self,msg):
        self.main_ui.textEdit.append(msg)


    def Start(self):
        if self.main_ui.label_3.text() == "" or self.main_ui.label_4.text() == "":
            self.main_ui.textEdit.append("请先选择 考生作品文件夹 和 考生信息表 ")
            return
        if len(self.ListStr) != len(self.imagePath):
            self.main_ui.textEdit.append("表格数据内容与文件夹内容图片数量不匹配，请修改表格或重选文件夹")
            return
        self.main_ui.startbutton.setEnabled(False)
        self.main_ui.deletebutton.setEnabled(False)
        self.main_ui.stopbutton.setEnabled(True)
        self.main_ui.textEdit.append("开始处理......")
        self.BatchProgram.flag = True
        dir = self.Mkdir()
        if dir!="":
            self.main_ui.textEdit.append("创建 " + dir +" 文件夹成功")
            try:
                self.BatchProgram.set_arguments(self.imagePath,
                               self.ListStr,
                               self.FontColor[self.main_ui.comboBox2.currentText()],
                               int(self.main_ui.lineEdit.text()),
                               self.main_ui.comboBox3.currentText(),self.output)
                self.BatchProgram.start()
            except:
                self.main_ui.startbutton.setEnabled(True)
                self.main_ui.deletebutton.setEnabled(True)
                self.main_ui.stopbutton.setEnabled(False)
                self.BatchProgram.flag = False
                self.main_ui.textEdit.append("处理失败，请检查文件夹和表格")

    def Stop(self):
        self.main_ui.startbutton.setEnabled(True)
        self.main_ui.deletebutton.setEnabled(True)
        self.main_ui.stopbutton.setEnabled(False)
        self.main_ui.textEdit.append("正在停止处理")
        self.BatchProgram.flag = False


    def Finish(self,msg):
        self.main_ui.startbutton.setEnabled(True)
        self.main_ui.deletebutton.setEnabled(True)
        self.main_ui.stopbutton.setEnabled(False)
        self.main_ui.textEdit.append(msg)
        self.BatchProgram.flag = False

    def DeleteDir(self):
        print(self.output)
        if self.output!="":
            if os.path.exists(self.output):
                shutil.rmtree(self.output)
                self.main_ui.textEdit.append("删除 "+self.output+" 文件夹成功")

