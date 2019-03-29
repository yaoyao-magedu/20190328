"""
QT UI for translator
|- Work with transapp class
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
class UiTranslator(QWidget):
    def __init__(self, bdtr, ydtr):
        super().__init__()
        self.bdtr = bdtr
        self.ydtr = ydtr
        # window
        self.setWindowTitle("Translator")
        self.setGeometry(400, 400, 400, 300)
        # TextArea (input)
        self.keywordEditor = QLineEdit(self)
        self.keywordEditor.setGeometry(10, 10, 330, 30)
        # Button (submit)
        self.translateButton = QPushButton(self)
        self.translateButton.setGeometry(350, 10, 40, 30)
        self.translateButton.setText("翻译")
        # lable (show result)

        self.bdlabelarea = QLabel(self)
        self.bdlabelarea.setGeometry(10, 50, 25, 110)
        self.bdlabelarea.setText("百度")

        self.bdresultArea = QLabel(self)
        self.bdresultArea.setGeometry(40, 50, 350, 110)
        self.bdresultArea.setText("<p>result area baidu</p>")
        self.bdresultArea.setAlignment(Qt.AlignTop)
        self.bdresultArea.setFrameStyle(3)

        self.ydlabelarea = QLabel(self)
        self.ydlabelarea.setGeometry(10, 170, 25, 110)
        self.ydlabelarea.setText("有道")

        self.ydresultArea = QLabel(self)
        self.ydresultArea.setGeometry(40, 170, 350, 110)
        self.ydresultArea.setText("<p>result area youdao</p>")
        self.ydresultArea.setAlignment(Qt.AlignTop)
        self.ydresultArea.setFrameStyle(3)

        # 处理事件
        self.translateButton.clicked.connect(self.translate)

    def translate(self):
        # get text
        kw = self.keywordEditor.text()
        # call translator
        bdresult = self.bdtr.translate(kw)
        ydresult = self.ydtr.translate(kw)
        # show result
        self.bdresultArea.setText(bdresult)
        self.ydresultArea.setText(ydresult)
