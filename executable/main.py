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

		#init default params
		self.frequancy  = 0      # 0.1Hz
		self.amplitude  = 0      # mm
		self.origin     = 75     # mm
		self.signal     = "sine" # (triangular, sine, sawlike, square)

		self.plot  = [] 		# Templates for plot construction
		self.sample_duration = 1 		# millisec
		self.exchange = True

		#Main update timer
		self.timer = QTimer()

		#getting ui ready
		self.initUI()

		self.pens  = [] #graphs
		self.plots = [] #plots
		self.data  = [] #points for graphs

		#Connect the model
		self.device = Device()
		self.detectDevice()

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
		#self.ui_elements["frequency"].setValidator(QIntValidator(self.device.info["min_freq"], self.device.info["max_freq"]))
		#self.ui_elements["amplitude"].setValidator(QIntValidator(self.device.info["min_amp"], self.device.info["max_amp"]))
		#self.ui_elements["origin"].setValidator(QIntValidator(self.device.info["min_orig"], self.device.info["max_orig"]))

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
	def initPlots(self):
		if not self.exchange:
			return

		for i in reversed(range(self.ui_elements["graph_layout"].count())): #remove previouse plots
			self.ui_elements["graph_layout"].takeAt(i).setParent(None)
		self.plots.clear()

		self.pens.clear() #remove previouse graphs


		for index, plot in self.device.info["plot_tepmlates"]["plots"].items():
			index = int(index)
			#add graph
			self.plots.append(PlotWidget())
			self.ui_elements["graph_layout"].addWidget(self.plots[index])

			#configure graph
			self.plots[index].setBackground("w")
			self.plots[index].showGrid(x = True, y = True)
			self.plots[index].setMouseEnabled(x=True, y=False)

			self.plots[index].setYRange(plot["lower_limit"], plot["upper_limit"])
			self.plots[index].setLabel("left", plot["left_label"])
			self.plots[index].setLabel("bottom", plot["bottom_label"])

			for pencil in plot["graphs"].values():
				self.pens.append( self.plots[index].plot(name=f'{pencil["name"]}', pen=mkPen(color=pencil["color"], width=pencil["width"])) )

		etc = self.device.info["plot_tepmlates"]["etc"]
		self.ui_elements["k1_slider"].setMinimum(etc["k1"]["min"])
		self.ui_elements["k1_slider"].setMaximum(etc["k1"]["max"])
		self.ui_elements["k1_slider"].setSingleStep(etc["k1"]["step"])
		self.ui_elements["k1_slider"].setValue(etc["k1"]["default"])
		self.ui_elements["k1_slider"].setMinimum(etc["k2"]["min"])
		self.ui_elements["k1_slider"].setMaximum(etc["k2"]["max"])
		self.ui_elements["k1_slider"].setSingleStep(etc["k2"]["step"])
		self.ui_elements["k1_slider"].setValue(etc["k2"]["default"])
		

	def detectDevice(self):
		self.exchange = False

		self.device = Device()

		match platform.system():
			case 'Linux': 
				self.device = Device(port='/dev/ttyACM0', baudrate=500000)
			case 'Darwin': 
				self.device = Device()
			case 'Windows': 
				self.device = Device()

		info = self.device.getModelInfo()

		self.ui_elements["port"].setText(info["port"])
		self.ui_elements["status"].setText(info["status"])
		self.ui_elements["model"].setText(info["model"])
		self.ui_elements["prak"].setText(info["prak"])
		self.ui_elements["about"].setText(info["about"])
		self.ui_elements["author"].setText(info["author"])

		if ("Ошибка" not in info["status"]):
			self.exchange = True

		self.drop()
		self.initPlots()

	#start data exchange
	def start(self):
		if ("Ошибка" not in self.device.info["status"]):
			self.exchange = True
			self.device.start()

	#stop data exchange
	def stop(self):
		self.exchange = False
		self.device.stop()

	#delete aqquaried data
	def drop(self):
		#clear data
		self.data.clear()
		self.data.append([])

		if (self.exchange):
			for index, plot in self.device.info["plot_tepmlates"]["plots"].items():
				for num in plot["graphs"].keys():
					self.data.append([])

		#drop data on device
		try:
			self.device.drop()
		except:
			pass

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
		k1 = self.ui_elements["k1_lbl"].text()
		k2 = self.ui_elements["k2_lbl"].text()

		locale = {
			"triangular" : "Треугольная",
			"sine" 		 : "Синусоида",
			"sawlike" 	 : "Пилообразная",
			"square"     : "Квадратная"
		}
		
		#mapping and applying parameters
		self.frequency = int((0, frq)[ frq!="" ])*10 # <=> (frq == "") ? 0 : frq 
		self.amplitude = int((0, amp)[ amp!="" ])
		self.origin    = int((0, ori)[ ori!="" ])
		self.signal    = sig
		self.k1    	   = int(k1)
		self.k2    	   = int(k2)

		#applying changes to export parameters
		self.ui_elements["frq_lbl"].setText(str(self.frequency))
		self.ui_elements["amp_lbl"].setText(str(self.amplitude))
		self.ui_elements["ori_lbl"].setText(str(self.origin))
		self.ui_elements["sig_lbl"].setText(locale[self.signal])

		#send new params to device
		self.device.set(signal_num[self.signal], self.frequency, self.amplitude, self.origin, self.k1, self.k2)

	def set_updaters(self):
		self.timer.setInterval(self.sample_duration)
		self.timer.timeout.connect(self.update_plots)
		self.timer.start()

	def update_plots(self):
		#if(self.exchange):
		if(self.exchange):
			#get data from device [time, idle_val(-s), real_val(-s)]
			try:
				raw_data = self.device.get()
			except Exception:
				self.exchange = False
				self.detectDevice()
				return

			if raw_data==[] :
				self.exchange = False
				self.ui_elements["status"] = "Ошибка передачи данных"
				return

			self.data[0].append(raw_data[0])
			index = 0
			for plot in self.device.info["plot_tepmlates"]["plots"].values():
				for j in plot["graphs"].keys():
					self.data[index+1].append(raw_data[index+1])
					self.pens[index].setData( self.data[0], self.data[index+1])
					index += 1

			
			



app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()