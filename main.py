from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui

from random import randint

from math import sin

import pyqtgraph as pg
from PyQt5 import QtCore

import sys
import os


class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()

		self.setWindowTitle("sFive")
		self.setGeometry(0, 0, 500, 500)
		self.showMaximized()
		
		pwd = os.path.dirname(__file__)
		self.setWindowIcon(QtGui.QIcon(pwd + '/icons/icon.png'))






if __name__ == "__main__":
	app = QApplication(sys.argv)

	window = MainWindow()
	window.show()
	
	app.exec()