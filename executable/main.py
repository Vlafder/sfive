import sys
import os
import atexit

from PyQt5  \
	import  uic	#for ui parsing

from PyQt5.QtGui 		   \
	import  QIntValidator, \
		    QPixmap,	   \
		    QIcon, 		   \
		    QWheelEvent

from PyQt5.QtCore   \
	import  QDate,  \
			QTimer

from PyQt5.QtWidgets      \
	import  QMainWindow,  \
			QApplication, \
			QLabel,       \
			QTabWidget,   \
			QHBoxLayout,  \
			QPushButton,  \
			QGroupBox,    \
			QVBoxLayout,  \
			QRadioButton, \
			QFormLayout,  \
			QLineEdit,    \
			QDateEdit,    \
			QButtonGroup, \
			QWidget,	  \
			QSlider

from xlwt \
	import  Workbook 	#for excel export

from pyqtgraph          \
	import  PlotWidget, \
			mkPen 		#from data plotting

from math \
	import  sin

import platform

from random import randint

from device import Device


#signal type macros
signal_num = {
    "triangular" : 0,
    "sine"       : 1,
    "sawlike"    : 2,
    "square"     : 3
}


# ports = serial.tools.list_ports.comports()

# for port, desc, hwid in sorted(ports):
#     print(f"{port}: {desc} [{hwid}]")


class UI(QMainWindow):
	def __init__(self):
		super(UI, self).__init__()

		#sfive base dir
		self.base_dir   = os.path.dirname(__file__) + "/../"


		self.plot_tepmlates  = [] 		# Templates for plot construction
		self.sample_duration = 1 		# millisec
		self.exchange = True

		#Main update timer
		self.timer = QTimer()

		#getting ui ready
		self.initUI()

		#Connect the model
		self.device = self.detectDevice()

		#set plot
		if self.device :
			self.initPlot()

		#setting update timers
		self.set_updaters()


		self.show()


	#setting up GUI
	def initUI(self):  
		#Load the ui file
		uic.loadUi(self.base_dir + "ui/main.ui", self)

		self.setWindowTitle("sFive")
		self.setWindowIcon(QIcon(self.base_dir + "icons/sfive.png"))

		#ui to py objects
		self.ui_elements = {
			"graph_layout"	: self.findChild(QVBoxLayout,	"graph_layout"),
			"start"			: self.findChild(QPushButton, 	"start_btn"),
			"stop"			: self.findChild(QPushButton, 	"stop_btn"),
			"drop"			: self.findChild(QPushButton, 	"drop_btn"),
			"apply_params"	: self.findChild(QPushButton, 	"apply_params_btn"),
			"export"		: self.findChild(QPushButton, 	"export_btn"),
			"frequency"		: self.findChild(QLineEdit,   	"freq_input"),
			"amplitude"		: self.findChild(QLineEdit,   	"amp_input"),
			"origin"		: self.findChild(QLineEdit,   	"null_point_input"),
			"signal"		: self.findChild(QButtonGroup,  "buttonGroup"),
			"author"		: self.findChild(QLineEdit,   	"author_input"),
			"date"			: self.findChild(QDateEdit,   	"date_input"),
			"comment"		: self.findChild(QLineEdit,   	"comment_input"),
			"title"			: self.findChild(QLineEdit,   	"title_input"),
			"frq_lbl"		: self.findChild(QLabel, 	  	"freq_val_lbl"),
			"amp_lbl"		: self.findChild(QLabel, 	  	"amp_val_lbl"),
			"ori_lbl"		: self.findChild(QLabel, 	  	"null_pnt_lbl"),
			"sig_lbl"		: self.findChild(QLabel, 	  	"sig_form_lbl"),
			"port"			: self.findChild(QLabel, 	  	"port_lbl"),
			"status"		: self.findChild(QLabel, 	  	"status_lbl"),
			"model"			: self.findChild(QLabel, 	  	"model_lbl"),
			"prak"			: self.findChild(QLabel, 	  	"prak_lbl"),
			"about"			: self.findChild(QLabel, 	  	"about_lbl"),
			"author"		: self.findChild(QLabel, 	  	"author_lbl"),
			"detect"		: self.findChild(QPushButton, 	"detect_btn"),
			"detect"		: self.findChild(QPushButton, 	"watch_btn"),
			"k1_lbl"		: self.findChild(QLabel, 	  	"k1_lbl"),
			"k1_slider"		: self.findChild(QSlider, 	  	"k1_slider"),
			"k2_lbl"		: self.findChild(QLabel, 	  	"k2_lbl"),
			"k2_slider"		: self.findChild(QSlider, 	  	"k2_slider"),
		}

		#enforce input constrains
		self.ui_elements["frequency"].setValidator(QIntValidator(self.form_limits["min_freq"], self.form_limits["max_freq"]))
		self.ui_elements["amplitude"].setValidator(QIntValidator(self.form_limits["min_amp"], self.form_limits["max_amp"]))
		self.ui_elements["origin"].setValidator(QIntValidator(self.form_limits["min_orig"], self.form_limits["max_orig"]))

		#apply images
		self.findChild(QLabel, "sfive_logo").setPixmap(QPixmap(self.base_dir + "icons/sfive.png"))
		self.findChild(QLabel, "signal_forms_img").setPixmap(QPixmap(self.base_dir + "icons/signals.png"))

		#define startup tab
		self.findChild(QTabWidget, "tabWidget").setCurrentWidget(self.findChild(QWidget, "about"))

		#bind buttons
		self.ui_elements["start"].clicked.connect(self.start)
		self.ui_elements["stop"].clicked.connect(self.stop)
		self.ui_elements["drop"].clicked.connect(self.drop)
		self.ui_elements["export"].clicked.connect(self.export)
		self.ui_elements["apply_params"].clicked.connect(self.apply_params)
		self.ui_elements["detect"].clicked.connect(self.detectDevice)
		self.ui_elements["k1_slider"].valueChanged.connect(self.update_koef)
		self.ui_elements["k2_slider"].valueChanged.connect(self.update_koef)

		#set today date
		self.ui_elements["date"].setDate(QDate.currentDate())

	#setting plot and etc.
	def initPlot(self):
		for i in range(len(plot_tepmlates)):
			#add graph
			self.ui_elements["graph_layout"].addWidget(plot_tepmlates[i])

			#configure graph
			self.plot_tepmlates[i].setBackground("w")
			self.plot_tepmlates[i].showGrid(x = True, y = True)
			self.plot_tepmlates[i].setMouseEnabled(x=True, y=False)

			self.plot_tepmlates[i].setYRange(self.plot_tepmlates[i]["height_bottom"], self.plot_tepmlates[i]["height_top"])
			self.plot_tepmlates[i].setLabel("left", self.plot_tepmlates[i]["left_label"])
			self.plot_tepmlates[i].setLabel("bottom", self.plot_tepmlates[i]["bottom_label"])

			self.pens.append([]);
			for pen in plot_tepmlates[i]["pens"]:
				self.pens.append( self.plot_graph.plot(name=pen["label"], pen=mkPen(color=pen["color"])) )

	def detectDevice(self):
		self.exchange = False

		device = Device()

		match platform.system():
			case 'Linux': 
				device = Device(port='/dev/ttyACM0', baudrate=500000)
			case 'Darwin': 
				device = Device()
			case 'Windows': 
				device = Device()

		info = device.getModelInfo()

		self.ui_elements["port"].setText(info["port"])
		self.ui_elements["status"].setText(info["status"])
		self.ui_elements["model"].setText(info["model"])
		self.ui_elements["prak"].setText(info["prak"])
		self.ui_elements["about"].setText(info["about"])
		self.ui_elements["author"].setText(info["author"])	

		if ("Ошибка" not in info["status"]):
			self.exchange = True
			self.plot_tepmlates = info["plot_tepmlates"]
			self.data_templates = info["data_templates"]
			self.form_limits    = info["form_limits"]

		return device
		
	#start data exchange
	def start(self):
		self.exchange = True
		self.device.start()

	#stop data exchange
	def stop(self):
		self.exchange = False
		self.device.stop()

	#delete aqquaried data
	def drop(self):
		#clear data
		self.data["time"].clear()
		for i in range(len(plot_tepmlates)):
			for j in range(len(plot_tepmlates[i])):
				self.data[i][j].clear()

		#drop data on device
		self.device.drop()

	#export to excel
	def export(self):
		wb = Workbook()
		sheet = wb.add_sheet("Data")

		sheet.write(0, 0, "Author")
		sheet.write(0, 1, self.ui_elements["author"].text())

		sheet.write(1, 0, "Date")
		sheet.write(1, 1, self.ui_elements["date"].text())

		sheet.write(2, 0, "Title")
		sheet.write(2, 1, self.ui_elements["title"].text())

		sheet.write(3, 0, "Comment")
		sheet.write(3, 1, self.ui_elements["comment"].text())

		wb.save(os.path.abspath(f"~/Desktop{self.ui_elements['title'].text()}.xls"))

	def update_koef(self):
		self.ui_elements["k1_lbl"].setText(str(self.ui_elements["k1_slider"].value()))
		self.ui_elements["k2_lbl"].setText(str(self.ui_elements["k2_slider"].value()))
		self.apply_params()

	#applying parameters
	def apply_params(self):
		#getting raw parameters
		frq = self.ui_elements["frequency"].text()
		amp = self.ui_elements["amplitude"].text()
		ori = self.ui_elements["origin"].text()
		sig = self.ui_elements["signal"].checkedButton().objectName()

		locale = {
			"triangular" : "Треугольная",
			"sine" 		 : "Синусоида",
			"sawlike" 	 : "Пилообразная",
			"square"     : "Квадратная"
		}
		
		#mapping and applying parameters
		self.frequency = int((0, frq)[ frq!="" ]) # <=> (frq == "") ? 0 : frq 
		self.amplitude = int((0, amp)[ amp!="" ])
		self.origin    = int((0, ori)[ ori!="" ])
		self.signal    = sig

		#applying changes to export parameters
		self.ui_elements["frq_lbl"].setText(str(self.frequency))
		self.ui_elements["amp_lbl"].setText(str(self.amplitude))
		self.ui_elements["ori_lbl"].setText(str(self.origin))
		self.ui_elements["sig_lbl"].setText(locale[self.signal])

		#send new params to device
		self.device.set(signal_num[self.signal], self.frequency, self.amplitude, self.origin, self.k1, self.k2)

	def set_updaters(self):
		self.timer.setInterval(self.sample_duration)
		self.timer.timeout.connect(self.update_plot)
		self.timer.start()

	def update_plot(self):
		if(self.exchange):
			#get data from device [time, idle_val(-s), real_val(-s)]
			try:
				raw_data = self.device.get()
			except Exception:
				self.exchange = False
				self.device = self.detectDevice()
				return

			if raw_data==[] :
				self.exchange = False
				self.ui_elements["status"] = "Ошибка передачи данных"
				return

			self.data["time"].append(raw_data[0])
			index = 1
			for i in range(len(plot_tepmlates)):
				for j in range(len(plot_tepmlates[i])):
					self.data[i][j].append(raw_data[index])
					self.idle.setData( self.data["time"], self.data[i][j])
					index += 1

			
			



app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()