
from PyQt5.QtCore import QThread, pyqtSignal
from PIL import Image, ImageDraw, ImageFont

class BatchProgram(QThread):
    msg = pyqtSignal(str)
    finish = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)
        self.flag = True

    def set_arguments(self,imagePath,ListStr,color,text_size,position,output):
        self.imagePath = imagePath
        self.ListStr = ListStr
        self.color = color
        self.text_size = text_size
        self.position = position
        self.output=output
        self.FontPosition = {"右上角": "right", "右下角": "right", "左上角": "left", "左下角": "left"}

    def run(self):
        success=0
        fail=[]
        for i in range(len(self.imagePath)):
            if self.flag == False:
                self.msg.emit('停止成功')
                break
            print(self.output + "/" + str(i) + ".jpg")
            print(self.imagePath[i],
                              self.ListStr[i],
                              self.color,
                              self.text_size,
                              self.position)
            try:
                img = self.ImageAddText(self.imagePath[i],
                              self.ListStr[i],
                              self.color,
                              self.text_size,
                              self.position)

                img.save(self.output+"/"+str(i+1)+".jpg")
                success+=1
            except:
                fail.append(self.ListStr[i])
            if i % 10 == 0:
                self.msg.emit("任务进度： "+str(i)+"/"+str(len(self.imagePath)))
        self.msg.emit("处理完成,一共："+str(len(self.imagePath))+" 张图片")
        self.finish.emit("成功处理：" + str(success) + " 张图片")
        if len(fail)!=0:
            self.msg.emit("其中第 " + str(fail) + " 张图片处理失败，请检查图片")



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