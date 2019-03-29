"""
Combination of Translate app
|- ui
|- function of baidu translate
"""
from PyQt5.QtCore import QObject
from Translators.uitrans import *
from Translators.transfrombaidu import *
from Translators.transfromyoudao import *

class TransApp(QObject):
    def __init__(self):
        super().__init__()
        self.baidu = BaiduTranslator()
        self.youdao = YoudaoTranslator()
        self.ui = UiTranslator(self.baidu, self.youdao)
        self.ui.show()

