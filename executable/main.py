import sys
import os

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




class UI(QMainWindow):
	def __init__(self):
		super(UI, self).__init__()

		#constants
		self.max_height    = 150   # mm
		self.max_freq      = 200   # 0.1Hz
		self.max_time_span = 1000  #millisec
		
		#init default params
		self.frequancy  = 0      # 0.1Hz
		self.amplitude  = 0      # mm
		self.origin     = 75     # mm
		self.signal     = "sine" # (triangular, sine, sawlike, square)
		self.exchange   = True	 # exchange data?

		#sfive base dir
		self.base_dir   = os.path.dirname(__file__) + "/../"

		#plotting variables
		self.data       = {
			"time"  : [0],  			# 100 millisec
			"idle"  : [self.origin],	# mm
			"real"  : [self.origin]		# mm
		}    
		self.plot_graph  = PlotWidget()
		self.max_samples = 50          # int
		self.sample_duration = 100  	# millisec

		#Main update timer
		self.timer = QTimer()




		#getting ui ready
		self.initUI()

		#set plot
		self.initPlot()

		#coonecting to the physical model
		#self.connect_with_apparatus()

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
			"frequancy"		: self.findChild(QLineEdit,   	"freq_input"),
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
		}

		#enforce input constrains
		self.ui_elements["frequancy"].setValidator(QIntValidator(0, self.max_freq))
		self.ui_elements["amplitude"].setValidator(QIntValidator(0, self.max_height))
		self.ui_elements["origin"].setValidator(QIntValidator(0, self.max_height))

		#apply images
		self.findChild(QLabel, "sfive_logo").setPixmap(QPixmap(self.base_dir + "icons/sfive.png"))
		self.findChild(QLabel, "signal_forms_img").setPixmap(QPixmap(self.base_dir + "icons/signals.png"))

		#bind buttons
		self.ui_elements["apply_params"]

		#define startup tab
		self.findChild(QTabWidget, "tabWidget").setCurrentWidget(self.findChild(QWidget, "about"))

		#bind buttons
		self.ui_elements["start"].clicked.connect(self.start)
		self.ui_elements["stop"].clicked.connect(self.stop)
		self.ui_elements["drop"].clicked.connect(self.drop)
		self.ui_elements["export"].clicked.connect(self.export)
		self.ui_elements["apply_params"].clicked.connect(self.apply_params)

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
		
	#start data exchange
	def start(self):
		self.exchange = True

	#stop data exchange
	def stop(self):
		self.exchange = False

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
		frq = self.ui_elements["frequancy"].text()
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
		self.frequancy = int((0, frq)[ frq!="" ]) # = (frq == "") ? 0 : frq 
		self.amplitude = int((0, amp)[ amp!="" ])
		self.origin    = int((0, ori)[ ori!="" ])
		self.signal    = sig

		#applying changes to export parameters
		self.ui_elements["frq_lbl"].setText(str(self.frequancy))
		self.ui_elements["amp_lbl"].setText(str(self.amplitude))
		self.ui_elements["ori_lbl"].setText(str(self.origin))
		self.ui_elements["sig_lbl"].setText(locale[self.signal])

	def set_updaters(self):
		self.timer.setInterval(self.sample_duration)
		self.timer.timeout.connect(self.update_plot)
		self.timer.start()

	def update_plot(self):
		if(self.exchange):
			self.data["time"].append(self.data["time"][-1] + self.sample_duration)
			self.data["idle"].append(self.get_idle(self.data["time"][-1]))
			self.data["real"].append(self.get_real(self.data["time"][-1]))

			self.real.setData( self.data["time"][-self.max_samples:], self.data["real"][-self.max_samples:])
			self.idle.setData( self.data["time"][-self.max_samples:], self.data["idle"][-self.max_samples:])
			
	def get_idle(self, time):
		#return sin(time)*self.amplitude + self.origin
		return randint(-50, 50) + self.origin

	def get_real(self, time):
		return sin(time)*self.amplitude + self.origin
		#return randint(-50, 50) + self.origin



app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()