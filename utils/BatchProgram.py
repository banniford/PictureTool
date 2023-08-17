
from PyQt5.QtCore import QThread, pyqtSignal

from utils.ImageAddText import ImageAddText


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

    def run(self):
        success=0
        fail=[]
        for k in self.imagePath:
            if self.flag == False:
                self.msg.emit('停止成功')
                break
            try:
                img = ImageAddText(self.imagePath[k],
                              self.ListStr[k],
                              self.color,
                              self.text_size,
                              self.position)

                img.save(self.output+"/"+str(self.ListStr[k])+".jpg")
                success+=1
            except:
                fail.append(self.ListStr[k])
            if success % 10 == 0:
                self.msg.emit("任务进度： "+str(k)+"/"+str(len(self.imagePath)))
        self.msg.emit("处理完成,一共："+str(len(self.imagePath))+" 张图片")
        self.finish.emit("成功处理：" + str(success) + " 张图片")
        if len(fail)!=0:
            self.msg.emit("其中第 " + str(fail) + " 张图片处理失败，请检查图片")


