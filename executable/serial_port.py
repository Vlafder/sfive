
import serial
import time
from threading import Thread

class SerialPort():
    def __init__(self, port='/dev/ttyACM0', baudrate=500000) -> None:



class SerialPort():
    def __init__(self, port='/dev/ttyACM0', baudrate=500000) -> None:
        self.ser = serial.Serial()
        self.ser.baudrate = self.baudrate
        self.ser.port = self.port

        th = Thread(target=self.check_callback, daemon=True)
        th.start()

    def connect(self):
        self.ser.open()
        

    def disconnect(self):
        self.kill = True
        self.data = b""
        self.ser.reset_input_buffer()
        self.ser.close()

    def callback(self, msg : bytes):
        self.data += msg
        # print(self.data)
        if msg == b"\n":
            # self.busy = False
            self.ack = True
            # self.data_lag = self.data.count(b'\n')
            # if self.data_lag > 2:
            #     print(self.data_lag)

    def check_callback(self):
        while True:
            if self.kill == False and self.ser.is_open == True: 
                if self.ser.in_waiting > 0:
                    self.busy = True
                    msg = self.ser.read()
                    self.callback(msg)
                    self.busy = False
            else:
                time.sleep(0.005)

    def send_data(self, data : str):
        while self.busy == True:
            continue
        # print(bytes(data, 'utf-8'))
        self.ser.write(bytes("#"+data+"\n", 'utf-8'))


    def get_data(self):
        # if self.data != b'':
        #     print(self.data)
        string = self.data.decode("utf-8")
        begin = string.find("#")
        end = string.find("\r\n")
        string_out = string[begin+1:end]
        self.data = self.data[end+2:]
        # return self.data.decode("utf-8").replace("\r", "").replace("\n", "")
        self.data_lag = self.data.count(b'\n')
        return string_out
    
