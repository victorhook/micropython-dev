import serial
import time
import threading

class Servo:

    CW_SLOW = 73
    CCW_SLOW = 80

    def __init__(self, mcu, pin):
        self.mcu = mcu
        self.name = f'servo_{pin}' 

        self.mcu.write('from machine import Pin, PWM')
        self.mcu.write(f'{self} = PWM(Pin({pin}))')
        self.mcu.write(f'{self}.freq(50)')
        self.stop()


    def rotate_180(self, clockwise=True):
        threading.Thread(target=self._rotate_180, args=(clockwise, )).start()

    def _rotate_180(self, clockwise=True):
        t1 = time.time()
        self.start_slow(clockwise=clockwise)

        while time.time() - t1 < 1.3:
            pass

        self.stop()

    def start_slow(self, clockwise=True):
        if clockwise:
            self.mcu.write(f'{self}.duty({self.CW_SLOW})')
        else:
            self.mcu.write(f'{self}.duty({self.CCW_SLOW})')

    def stop(self):
        self.mcu.write(f'{self}.duty(0)')

    def __repr__(self):
        return self.name


class ESP8266:

    def __init__(self, port='/dev/ttyUSB0', baud=115200, timeout=.1):

        # Open instantly. Not doing so fails on my Ubuntu version (18.04)
        self.serial = serial.Serial('/dev/ttyUSB0', 115200, timeout=.1)
        print('Connected')

        self.servo = Servo(self, pin=0)


    def write(self, data, should_read=False):
        self.serial.write(f'{data}\r\n'.encode())
        if self.serial.inWaiting:
            # empty the buffer
            if should_read:
                return self.serial.read(300).decode().split('\r\n')
            self.serial.read(300)
            

    def disconnect(self):
        self.__exit__()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.serial.close()
        print('disconnected')
        for arg in args:
            if arg:
                print(arg)







if __name__ == "__main__":
    with ESP8266() as mcu:
        
        mcu.servo.rotate_180(False)

        time.sleep(2)

        mcu.servo.stop()

