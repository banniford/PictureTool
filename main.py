
import sys
from ui import picturetoolUI as UI
from PyQt5.QtWidgets import QApplication, QMainWindow

items = ['Python', 'R', 'Java', 'C++', 'CSS']
items1 = ["序号","考生姓名 拼音（注意统一大小写）","证件类型（身份证、护照、港澳通行证、台胞证）","证件号码（注意""X""大写，不能有空格或特殊字符）","性别（无需填写，录入身份证号自动生成）","生日（无需填写，录入身份证号自动生成）",
         "考级时间（年、月、日，例：2019-08-08）","报考专业（请参考填表说明中第七条，核对后填写）","报考级别（以数列形式排序统一填写阿拉伯数字，例如“1”）","民族（一定要全称，例如”汉族、回族、蒙古族等）"	,
         "国籍","考级结果"]
# comboBox1.loadItems(items)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = UI.Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.MycomboBox.loadItems(items)
    MainWindow.show()
    sys.exit(app.exec_())
