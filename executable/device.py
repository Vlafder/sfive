import serial
import numpy as np
import time
import atexit

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
            "port"   : port,
            "status" : 'Не подключено',
            "model"  : '',
            "prak"   : '',
            "about"  : '',
            "author" : ''
        }

        if port=='':
            return

        try:
            self.sp = serial.Serial(port=port, baudrate=baudrate) 
            self.getInfo()

        except serial.SerialException as se:
            self.sp = False
            self.info["status"] = f"Ошибка: {str(se)}"
            return

        except Exception as e:
            self.sp = False
            self.info["status"] = f"Ошибка: {str(e)}"
            return


    def __del__(self):
        if self.sp:
            self.sp.close


    #get info from model
    def getInfo(self):
        self.sp.write(msg(f"{INFO}"))
        raw_data = self.sp.readline().decode().strip()
        
        result = raw_data.split("\n")
        self.info["status"] = result[0]
        self.info["model"]  = result[1]
        self.info["prak"]   = result[2]
        self.info["about"]  = result[3]
        self.info["author"] = result[4]


    def getModelInfo(self):
        return self.info

    
    def set(self, *args):
        if not self.sp:
            return 

        #get signal number by name
        signal = args[0]

        #turn [3, 1, 2] -> "003001002"
        params = ''.join([to_len_3(param) for param in args[1:]])

        self.sp.write(msg(f"{SET}{signal}{params}"))
        #print(self.msg(f"{SET}{signal}{params}"))

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
            return [0, 75, 75]

        self.sp.write(msg(f"{GET}"))
        raw_data = self.sp.readline().decode().strip()
        
        result = raw_data.split(" ")

        if(len(result)==3):
            return [int(i) for i in result]
        else:
            print("GET error")
            return [0, 75, 75]


def msg(text):
    return bytes(text + "\n", 'utf-8')


def to_len_3(param):
    result = ["0", "0", "0"]

    for i in range(3):
        result[i] = str(param % 10);
        param //= 10

    #reverse a string
    return ''.join(result[::-1])