from serial_port import SerialPort
import numpy as np
import time
import atexit

SET   = 0 
START = 1
STOP  = 2
DROP  = 3
GET   = 4


class Device():
    def __init__(self, port='/dev/ttyACM0', baudrate=500000) -> None:
        self.sp = SerialPort(port=port, baudrate=baudrate) 

    def connect(self):
        self.sp.connect()

    def disconnect(self):
        self.sp.disconnect()
    
    def set(self, signal, *args):
        #get signal number by name
        signal = args[0]
        args.pop(0)

        #turn [3, 1, 2] -> "003001002"
        params = ''.join([to_len_3(param) for param in args])

        #self.sp.send_request(f"{SET}{signal_num[signal]}{params}")
        print(f"{SET}{signal}{params}")

    def start(self):
        #self.sp.send_request(f"{START}")
        print(f"{START}")

    def stop(self):
        #self.sp.send_request(f"{STOP}")
        print(f"{STOP}")

    def drop(self):
        #self.sp.send_request(f"{DROP}")
        print(f"{DROP}")

    def get(self):
        #self.sp.send_request(f"{GET}")
        print( self.sp.get_data().split(" ") )


def to_len_3(param):
    result = "000"
    param  = string(param)
    for i in range(len(param)):
        result[i] = param[i]

    #reverse a string
    return result[::-1]