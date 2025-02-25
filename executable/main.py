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
	import  QDate , \
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
			QWidget

from xlwt \
	import  Workbook 	#for excel export

from pyqtgraph          \
	import  PlotWidget, \
			mkPen 		#from data plotting

from math \
	import  sin

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

		#constants
		self.max_height    = 150   # mm
		self.max_freq      = 200   # 0.1Hz
		self.max_time_span = 1000  #millisec
		
		#init default params
		self.frequency  = 0      # 0.1Hz
		self.amplitude  = 0      # mm
		self.origin     = 75     # mm
		self.signal     = "sine" # (triangular, sine, sawlike, square)

		#sfive base dir
		self.base_dir   = os.path.dirname(__file__) + "/../"

		#plotting variables
		self.data       = {
			"time"  : [0],  			# 100 millisec
			"idle"  : [self.origin],	# mm
			"real"  : [self.origin]		# mm
		}    
		self.plot_graph  = PlotWidget()
		self.sample_duration = 1 		# millisec
		self.exchange = True

		#Main update timer
		self.timer = QTimer()

		#getting ui ready
		self.initUI()

		#Connect the model
		self.device = self.detectDevice()

		#set plot
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
		}

		#enforce input constrains
		self.ui_elements["frequency"].setValidator(QIntValidator(0, self.max_freq))
		self.ui_elements["amplitude"].setValidator(QIntValidator(0, self.max_height))
		self.ui_elements["origin"].setValidator(QIntValidator(0, self.max_height))

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

		#set today date
		self.ui_elements["date"].setDate(QDate.currentDate())

	#setting plot and etc.
	def initPlot(self):
		#add graph
		self.ui_elements["graph_layout"].addWidget(self.plot_graph)

		#configure graph
		self.plot_graph.setBackground("w")
		self.plot_graph.showGrid(x = True, y = True)
		self.plot_graph.setYRange(0, self.max_height)
		self.plot_graph.setMouseEnabled(x=True, y=False)
		self.plot_graph.setLabel("left", "Высота mm")
		self.plot_graph.setLabel("bottom", "Время sec")

		self.idle = self.plot_graph.plot(
						name="Ожидаемое положение",
						pen=mkPen(color=(255, 0, 0)),
					 )

		self.real = self.plot_graph.plot(
						name="Фактическое положение",
						pen=mkPen(color=(0, 0, 255)),
					 )

	def detectDevice(self):
		device = Device();
		info = device.getModelInfo()

		print(">>>", info["status"])

		self.ui_elements["port"].setText(info["port"])
		self.ui_elements["status"].setText(info["status"])
		self.ui_elements["model"].setText(info["model"])
		self.ui_elements["prak"].setText(info["prak"])
		self.ui_elements["about"].setText(info["about"])
		self.ui_elements["author"].setText(info["author"])

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
		self.data["time"].clear()
		self.data["idle"].clear()
		self.data["real"].clear()

		#set "zeroes"
		self.data["time"].append(0)
		self.data["idle"].append(self.origin)
		self.data["real"].append(self.origin)

		#дописать отчитку графика
		self.idle.setData( self.data["time"], self.data["idle"])
		self.real.setData( self.data["time"], self.data["real"])

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
		self.frequency = int((0, frq)[ frq!="" ]) # = (frq == "") ? 0 : frq 
		self.amplitude = int((0, amp)[ amp!="" ])
		self.origin    = int((0, ori)[ ori!="" ])
		self.signal    = sig

		#applying changes to export parameters
		self.ui_elements["frq_lbl"].setText(str(self.frequency))
		self.ui_elements["amp_lbl"].setText(str(self.amplitude))
		self.ui_elements["ori_lbl"].setText(str(self.origin))
		self.ui_elements["sig_lbl"].setText(locale[self.signal])

		#send new params to device
		self.device.set(signal_num[self.signal], self.frequency, self.amplitude, self.origin)

	def set_updaters(self):
		self.timer.setInterval(self.sample_duration)
		self.timer.timeout.connect(self.update_plot)
		self.timer.start()

	def update_plot(self):
		if(self.exchange):
			#get data from device [time, idle_val(-s), real_val(-s)]
			raw_data = self.device.get()

			self.data["time"].append(raw_data[0])
			self.data["idle"].append(raw_data[1])
			self.data["real"].append(raw_data[2])

			sample_count = int(1000/self.sample_duration)

			self.idle.setData( self.data["time"][-sample_count:], self.data["idle"][-sample_count:])
			self.real.setData( self.data["time"][-sample_count:], self.data["real"][-sample_count:])
			



app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()