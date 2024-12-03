import serial
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
        try:
            self.sp = serial.Serial(port=port, baudrate=baudrate) 
        except serial.SerialException as se:
            print("Serial port error:", str(se))
        except Exception as e:
            print("An error occurred:", str(e))

        #atexit.register(self.sp.close())
    
    def set(self, *args):
        #get signal number by name
        signal = args[0]
        del args[0]

        #turn [3, 1, 2] -> "003001002"
        params = ''.join([to_len_3(param) for param in args]) + "\n"
        msg = (f"{SET}{signal}{params}").encode('ASCII')


        #self.sp.write(b"{msg}")
        print(msg)

    def start(self):
        #self.sp.write(f"{START}")
        print(f"{START}")

    def stop(self):
        #self.sp.write(f"{STOP}")
        print(f"{STOP}")

    def drop(self):
        #self.sp.write(f"{DROP}")
        print(f"{DROP}")

    def get(self):
        #self.sp.write(f"{GET}")
        #c = self.sp.read(1)
        raw_data = ""

        #while c!="\n" and c!="\0":
        #    raw_data += c
        #    #c = self.sp.read(1)

        #print( raw_data.split("") )
        return 100, 75, 75


def to_len_3(param):
    result = "000"
    param  = string(param)
    for i in range(len(param)):
        result[i] = param[i]

    #reverse a string
    return result[::-1]