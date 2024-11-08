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
		self.showMaximized()
		
		pwd = os.path.dirname(__file__)
		self.setWindowIcon(QtGui.QIcon(pwd + '/icons/icon.png'))

		self.plot_graph = pg.PlotWidget()
		self.setCentralWidget(self.plot_graph)
		self.plot_graph.setBackground("w")
		pen = pg.mkPen(color=(255, 0, 0))
		self.plot_graph.setTitle("Temperature vs Time", color="b", size="20pt")
		styles = {"color": "red", "font-size": "18px"}
		self.plot_graph.setLabel("left", "Temperature (°C)", **styles)
		self.plot_graph.setLabel("bottom", "Time (min)", **styles)
		self.plot_graph.addLegend()
		self.plot_graph.showGrid(x=True, y=True)
		self.plot_graph.setYRange(0, 15)
		self.time = list(range(10))
		self.temperature = [randint(20, 40) for _ in range(10)]
		# Get a line reference
		
		self.line = self.plot_graph.plot(
			self.time,
			self.temperature,
			name="Temperature Sensor",
			pen=pen,
			symbol="+",
			symbolSize=15,
			symbolBrush="b",
		)
		# Add a timer to simulate new temperature measurements
		self.timer = QtCore.QTimer()
		self.timer.setInterval(50)
		self.timer.timeout.connect(self.update_plot)
		self.timer.start()

	def update_plot(self):
		self.time.append(self.time[-1] + 1)
		self.temperature.append(sin(self.time[-1])*6+5)
		self.line.setData(self.time[-10:], self.temperature[-10:])




if __name__ == "__main__":
	app = QApplication(sys.argv)

	window = MainWindow()
	window.show()
	
	app.exec()