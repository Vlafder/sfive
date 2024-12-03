import serial
import time
import threading


class SerialPort():
    def __init__(self, port='/dev/ttyACM0', baudrate=500000) -> None:
        self.busy = False
        self.ack = False
        self.data = b""
        self.soft_timeout = 1.0
        self.t = 0.0
        self.port = port
        self.baudrate = baudrate
        self.data_lag = 0

        self.ser = serial.Serial()
        self.ser.baudrate = self.baudrate
        self.ser.port = self.port

        self.kill = True
        th1 = threading.Thread(target=self.check_callback, daemon=True)
        th1.start()

    def connect(self):
        self.kill = False
        
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

    def send_request(self, data : str):
        print(f"Request: {data}")
        self.data = b""
        self.t = 0.0
        self.send_data(data)
        data_lst = data.split(" ")
        while True:
            if self.data != "" and self.busy == False:
                get_data = self.get_data()
                # print(get_data)
                get_data_lst = list(get_data.split(" "))
                if len(get_data_lst) >= 2:
                    # print(f"{data}: {get_data_lst}")
                    if get_data_lst[0] == data_lst[0] and get_data_lst[1] == "OK":
                        break
            if self.t > self.soft_timeout:
                self.send_data(data)
                self.t = 0.0
            time.sleep(0.002)
            self.t += 0.002

        print(f"Responce: {get_data}")
        return get_data


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
    
    def get_last_data(self):
        end = -1
        while end == -1:
            string = self.data.decode("utf-8")
            
            end = string.rfind("\r\n")
            if end == -1:
                # return "-1"
                continue
            begin = string.rfind("#", 0, end)
            # print(string[begin:end+2].encode())
            string_out = string[begin+1:end]
            self.data = self.data[end+2:]
            # print(self.data)

            # print(f"{string_out} | {begin} | {end}")
            # return self.data.decode("utf-8").replace("\r", "").replace("\n", "")
            # time.sleep(0.002)
            return string_out
    
import serial.tools.list_ports
if __name__ == "__main__":
    # ports = serial.tools.list_ports.comports()

    # for port, desc, hwid in sorted(ports):
    #     print("{}: {} [{}]".format(port, desc, hwid))
    sp = SerialPort(port='/dev/ttyACM0', baudrate=500000)
    # sp.ser.reset_input_buffer()
    # sp.data = b""
    sp.send_request("STOP")
    sp.send_request("SETK 16 0")
    sp.send_request("STEP 0")
    time.sleep(0.5)
    sp.send_request("SETK 0.5 0")
    sp.send_request("SIN 4 5")

    t = 0
    while t < 10.0:
        print(sp.get_data())
        t += 0.005
        time.sleep(0.005)

    sp.send_request("SETK 16 0")
    sp.send_request("STEP 0")
    time.sleep(0.5)
    sp.send_request("STOP")
#----------------------------------------------
    # send_data = "STOP"
    # print(f"Request: {send_data}")
    # sp.send_data(send_data)
    # while True:
    #     get_data = sp.get_data()
    #     if get_data == "STOP OK\r\n":
    #         break
    # print(f"Responce: {get_data}")


    # send_data = "SETK 1 0"
    # print(f"Request: {send_data}")
    # sp.send_data(send_data)
    # while True:
    #     get_data = sp.get_data()
    #     if get_data.find("SETK") != -1:
    #         break
    # print(f"Responce: {get_data}")

    # send_data = "SIN 1 1"
    # print(f"Request: {send_data}")
    # sp.send_data(send_data)
    # while True:
    #     get_data = sp.get_data()
    #     if get_data.find("OUT") != -1:
    #         break

    # it = 0
    # while it < 1000:
    #     get_data = sp.get_data()
    #     print(get_data)
    #     it += 1
    #     time.sleep(0.005)
        
    # send_data = "STOP"
    # print(f"Request: {send_data}")
    # sp.send_data(send_data)
    # while True:
    #     get_data = sp.get_data()
    #     if get_data == "STOP OK\r\n":
    #         break
    # print(f"Responce: {get_data}")
#----------------------------------------------
    # send_data = "SETK 1 0"
    # print(f"Request: {send_data}")
    # get_data = sp.send_request(send_data)
    # print(f"Responce: {get_data}")

    # send_data = "SIN 1 1"
    # print(f"Request: {send_data}")
    # get_data = sp.send_request(send_data)
    
    # it = 0
    # while it < 1000:
    #     get_data = sp.get_data()
    #     # print(get_data)
    #     it += 1
    #     time.sleep(0.005)

# busy = False
# ack = False
# s = 0

# def callback():
#     global busy
#     global ack
#     global s

#     s = ser.readline()
#     print(s)
#     busy = False
#     ack = True

# def wait_callback():
#     global busy
#     global ser

#     while True:
#         if ser.in_waiting > 0:
#             busy = True
#             callback()
#         # time.sleep(0.001)

# ser = serial.Serial('/dev/ttyACM0', 500000)
# print(ser.name) 

# th1 = threading.Thread(target=wait_callback, daemon=True)
# th1.start()

# if busy == False: 
#     ser.write(b'STOP')

# while busy == True or ack == False:
#     continue

# ack = True
# if busy == False: 
#     ser.write(b'SETK 1 0\r\n')

# while busy == True or ack == False:
#     continue

# ack = True
# if busy == False: 
#     ser.write(b'SIN 1 1\r\n')

# # while(True): 
# time.sleep(2.1)

# while busy == True or ack == False:
#     continue

# if busy == False: 
#     ser.write(b'STOP')

# while busy == True or ack == False:
#     continue
# print(s)  

# while(True): 
#     if s == b'STOP OK\r\n':
#         break

#------------------------------------------

# print("send STOP")
# s = ser.readline()
# ser.write(b"SETK 1 0\r\n")
# print("send SETK")
# s = ser.readline()
# # ser.write(b"STEP 0\r\n")
# # print("send STEP")
# # time.sleep(0.2)

# # ser.write(b'STOP')
# # print("send STOP")
# # s = ser.readline()
# print(s)
# ser.write(b'SIN 1 1\r\n')
# print("send SIN")
# it = 0
# while it < 2000:
#     if ser.in_waiting > 0:
#         data_str = ser.readline()
#         print(data_str)
#         it += 1
#     time.sleep(0.001)

# ser.write(b'STOP')
# s = ser.readline()
# print(s)