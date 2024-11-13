from random import randint
from math import sin
import pyqtgraph as pg

from base_gui import Ui_MainWindow
from PyQt5 import QtWidgets

import sys
import os




class MainLayout(Ui_MainWindow):
	def __init__(self):
		super(Ui_MainWindow, self).__init__()

		self.setWindowTitle("sFive")
		self.setGeometry(0, 0, 500, 500)
		self.showMaximized()
		
		pwd = os.path.dirname(__file__)
		self.setWindowIcon(QtGui.QIcon(pwd + '/icons/icon.png'))






if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()

	ui = MainLayout()
	ui.setupUi(MainWindow)

	MainWindow.show()
	sys.exit(app.exec_())