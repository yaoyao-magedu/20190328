"""
main
"""

from Translators.transapp import TransApp
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

trans_app = TransApp()

sys.exit(app.exec())
