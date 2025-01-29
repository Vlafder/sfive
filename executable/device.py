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
            exit()
        except Exception as e:
            print("An error occurred:", str(e))
            exit()

        atexit.register(self.sp.close)
    
    def set(self, *args):
        #get signal number by name
        signal = args[0]

        #turn [3, 1, 2] -> "003001002"
        params = ''.join([to_len_3(param) for param in args[1:]])

        self.sp.write(self.msg(f"{SET}{signal}{params}"))
        #print(self.msg(f"{SET}{signal}{params}"))

    def start(self):
        self.sp.write(self.msg(f"{START}"))
        #print(f"{START}")

    def stop(self):
        self.sp.write(self.msg(f"{STOP}"))
        #print(f"{STOP}")

    def drop(self):
        self.sp.write(self.msg(f"{DROP}"))
        #print(f"{DROP}")

    def get(self):
        self.sp.write(self.msg(f"{GET}"))
        raw_data = self.sp.readline().decode().strip()
        
        result = raw_data.split(" ")

        if(len(result)==3):
            return [int(i) for i in result]
        else:
            print("GET error")
            return [0, 75, 75]

    def msg(self, text):
        return bytes(text + "\n", 'utf-8')


def to_len_3(param):
    result = ["0", "0", "0"]

    for i in range(3):
        result[i] = str(param % 10);
        param //= 10

    #reverse a string
    return ''.join(result[::-1])