import serial
import numpy as np
import time
import atexit
import json 
import time

SET   = 0 
START = 1
STOP  = 2
DROP  = 3
GET   = 4
INFO  = 5


class Device():
    def __init__(self, port='', baudrate=0):
        self.sp = False
        self.info = {
            "port"              : port,
            "status"            : 'Ошибка: Не подключено',
            "model"             : '',
            "prak"              : '',
            "about"             : '',
            "author"            : '',
            "plot_tepmlates"    : {}
        }   

        if port=='':
            return

        try:
            self.sp = serial.Serial(port=port, baudrate=baudrate, timeout=0.3) 
            self.getInfo()

        except serial.SerialException as se:
            if self.sp:
                self.sp.close
            self.sp = False
            self.info["status"] = f"Ошибка: {str(se)}"

        except Exception as e:
            if self.sp.is_open:
                self.sp.close
            self.sp = False
            self.info["status"] = f"Ошибка: {str(e)}"


    def __del__(self):
        if self.sp:
            self.sp.close


    #get info from model
    def getInfo(self):
        self.sp.write(msg(f"{INFO}"))
        raw_data = self.sp.readline().decode().strip()
        
        result = raw_data.split("|")

        self.info["status"] = result[0]
        self.info["model"]  = result[1]
        self.info["prak"]   = result[2]
        self.info["about"]  = result[3]
        self.info["author"] = result[4]

        gui_requirements = json.loads(result[5])
        self.info["plot_tepmlates"] = gui_requirements["plot_tepmlates"]
        print(self.info["plot_tepmlates"])


    def getModelInfo(self):
        return self.info

    
    def set(self, *args):
        if not self.sp:
            return 

        #turn [3, 1, 2] -> "3|1|2"
        params = '|'.join(args)

        self.sp.write(msg(f"{SET}{signal}{params}"))

    def start(self):
        if not self.sp:
            return 

        self.sp.write(msg(f"{START}"))
        #print(f"{START}")

    def stop(self):
        if not self.sp:
            return 

        self.sp.write(msg(f"{STOP}"))
        #print(f"{STOP}")

    def drop(self):
        if not self.sp:
            return 

        self.sp.write(msg(f"{DROP}"))
        #print(f"{DROP}")

    def get(self):
        if not self.sp:
            return []

        try:
            self.sp.write(msg(f"{GET}"))
        except Exception as e:
            self.sp.close
            self.info = Device().getModelInfo()
            raise Exception
        
        raw_data = self.sp.readline().decode().strip()
        
        result = raw_data.split(" ")

        if(len(result)):
            return [round(float(i)) for i in result]
        else:
            return []


def msg(text):
    return bytes(text + "\n", 'utf-8')
