import sys
import os

from PyQt5 import uic
from PyQt5.QtGui import QIntValidator, \
						QPixmap
from PyQt5.QtWidgets import QMainWindow,  \
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




"""
self.setWindowTitle("sFive")
self.setGeometry(0, 0, 500, 500)
self.showMaximized()

pwd = os.path.dirname(__file__)
self.setWindowIcon(QtGui.QIcon(pwd + '/icons/icon.png'))
"""

class UI(QMainWindow):
	def __init__(self):
		super(UI, self).__init__()

		#constants
		self.max_height = 150   # mm
		self.max_freq   = 200   # 0.1Hz
		
		#init default params
		self.frequancy = 0      # 0.1Hz
		self.amplitude = 0      # mm
		self.origin    = 75     # mm
		self.signal    = "sine" # (triangular, sine, sawlike, square)

		self.data      = []     # [ [sec, mm], ... ]

		self.initUI()

		self.show()



	#setting up GUI
	def initUI(self):  
		#Load the ui file
		uic.loadUi("../ui/main.ui", self)

		#ui to py objects
		self.ui_elements = {
			"graph_tab"		: self.findChild(QWidget,	  	"graph"),
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
			"sig_lbl"		: self.findChild(QLabel, 	  	"sig_form_lbl")
		}

		#enforce input constrains
		self.ui_elements["frequancy"].setValidator(QIntValidator(0, self.max_freq))
		self.ui_elements["amplitude"].setValidator(QIntValidator(0, self.max_height))
		self.ui_elements["origin"].setValidator(QIntValidator(0, self.max_height))

		#apply images
		self.findChild(QLabel, "sfive_logo").setPixmap(QPixmap("../icons/sfive.png"))
		self.findChild(QLabel, "signal_forms_img").setPixmap(QPixmap("../icons/signals.png"))

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


	#start data exchange
	def start(self):
		...

	#stop data exchange
	def stop(self):
		...

	#delete aqquaried data
	def drop(self):
		self.data.clear()
		#дописать отчитку графика

	#export to excel
	def export(self):
		...

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






app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()