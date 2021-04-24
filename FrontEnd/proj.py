from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(0, 0, 300, 300)
    win.setWindowTitle("CSE 323: Course Project")

    win.show()
    sys.exit(app.exec_())

window()
    
