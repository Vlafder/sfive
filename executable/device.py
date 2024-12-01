from serial_port import SerialPort
import numpy as np
import time

STOP = "STOP"
SETK = "SETK"
SETFRIC = "SETFRIC"
SIN_U = "SIN_U"
STEP = "STEP"
SIN = "SIN_PHI"
SQUARE = "SQUARE"
TRIANGLE = "TRI"
OUT = "OUT"

MAX_VOLTAGE = 12

class Device():
    def __init__(self, port='/dev/ttyACM0', baudrate=500000) -> None:
        self.sp = SerialPort(port=port, baudrate=baudrate) 

    def connect(self):
        self.sp.connect()

    def disconnect(self):
        self.sp.disconnect()
    
    def stop(self):
        self.sp.send_request(f"{STOP}")

    def is_ready(self):
        return self.sp.ack
    
    def get_data_lag(self):
        return self.sp.data_lag
    
    def reset_readiness(self):
        self.sp.ack = False

    def set_k(self, kx, kv):
        self.sp.send_request(f"{SETK} {kx} {kv}")

    def set_fric(self, gain, offset):
        self.sp.send_request(f"{SETFRIC} {gain} {offset}")

    def start_sin_u(self, ampl, freq):
        self.sp.send_request(f"{SIN_U} {ampl} {freq}")

    def start_step(self, ref):
        self.sp.send_request(f"{STEP} {ref}")

    def start_sin(self, ampl, freq):
        self.sp.send_request(f"{SIN} {ampl} {freq}")

    def start_triangle(self, ampl, freq):
        self.sp.send_request(f"{TRIANGLE} {ampl} {freq}")

    def start_square(self, ampl, freq):
        self.sp.send_request(f"{SQUARE} {ampl} {freq}")

    def get_data(self):
        data_lst = self.sp.get_data().split(" ") # 0 - time, 1 - ref, 2 - real
        if data_lst[0] == OUT and len(data_lst) > 4:
            try:
                cur = float(data_lst[3])
            except:
                cur = 0
                # print(f"ebat: {data_lst[3]}")
            return float(data_lst[2]), cur, float(data_lst[1])/1000, float(data_lst[4])
        else:
            # print(data_lst)
            return -1, -1, -1, -1
        
    def wait_step(self, delta):
        it = 0
        time.sleep(0.2)
        while True:
            ref, real, t, d_ref = self.get_data()
            print(f"time: {t:.3f} | ref: {ref:.0f} | real: {real:.2f} | delta: {delta:.2f}")
            if np.abs(ref - real) > np.abs(delta):
                time.sleep(0.002)
            else:
                it += 1
            if it >= 5 or t == -1:
                break
        time.sleep(0.1)

    def pwm2volts(self, pwm):
        return 12*pwm/255


if __name__ == "__main__":

    # def wait_null(device : Device, delta):
    #     while True:
    #         ref, real, t = device.get_data()
    #         # print(f"time: {t:.3f} | ref: {ref:.0f} | real: {real:.2f} | delta: {delta:.2f}")
    #         if np.abs(real) > np.abs(delta):
    #             time.sleep(0.005)
    #         else:
    #             break
    #     time.sleep(0.5)

    delta = 0.03
    device = Device(port='/dev/ttyACM0', baudrate=500000)
    device.stop()
    device.set_k(16, 0)
    device.start_step(0)
    device.wait_step(delta)
    device.set_k(1, 0)
    # device.start_sin(1, 1)
    device.start_step(0.5)

    t = 0.0
    while t < 60.0:
        ref, real, t = device.get_data()
        # if t >= 0.0:
            # print(f"time: {t:.3f} | ref: {ref:.0f} | real: {real:.2f}")
        time.sleep(0.005)

    device.set_k(16, 0)
    device.start_step(0)
    device.wait_step(delta)
    device.stop()
