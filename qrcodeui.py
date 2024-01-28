
import segno
import os
from datetime import datetime
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from PyQt5 import QtCore, QtGui, QtWidgets
import shutil

COUNT_PER_PAGE = 40
COUNT_PER_LINE = 5

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(861, 535)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 380, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(480, 470, 359, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.generateQrcode)

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(110, 380, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 420, 800, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(20, 120, 821, 241))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic")
        font.setPointSize(14)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 30, 201, 71))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "二维码生成器"))
        self.label_2.setText(_translate("MainWindow", "个数"))
        self.pushButton.setText(_translate("MainWindow", "生成"))
        self.label.setText(_translate("MainWindow", "输入二维码内容"))

    def generateQrcode(self):
        now = datetime.now()
        target_dir = "{}{}{}_{:0>2d}{:0>2d}{:0>2d}".format(
            now.year, now.month, now.day, now.hour, now.minute, now.second)
        print("create base directory for this round: ", target_dir)
        os.makedirs(target_dir)

        target_count = self.lineEdit.text()

        qrcontent = self.textEdit.toPlainText()
        qrcontent = qrcontent.replace(
            "(01)", "({{:0>{0}d}})".format(len(target_count)))
        print("will generate qrcode for")
        print(qrcontent)

        pdf_filename = "qrcode_{}.pdf".format(target_dir)
        my_canvas = canvas.Canvas(pdf_filename)
        for i in range(0, int(target_count)):
            qrcode = segno.make_qr(qrcontent.format(i+1))
            qrcode_file = "{}/qrcode_{}.svg".format(target_dir, i+1)
            qrcode.save(qrcode_file, scale=1.85)

            drawing = svg2rlg(qrcode_file)
            index = i % COUNT_PER_LINE
            line = i % COUNT_PER_PAGE//COUNT_PER_LINE
            x = 50+index*100
            y = 725-(line * 100)
            print("draw qrcode {} at x:{} y:{}".format(i+1, x, y))
            renderPDF.draw(drawing, my_canvas, x, y)
            if i > 0 and i % COUNT_PER_PAGE == COUNT_PER_PAGE-1:
                print("create a new page in pdf")
                my_canvas.showPage()

        my_canvas.save()
        print("save pdf {}".format(pdf_filename))
        shutil.rmtree(target_dir)
        print("qrcode svg files have been cleaned at {}".format(target_dir))
        self.label_3.setText("生成pdf文件 {}".format(pdf_filename))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
