import logging
import serial
from RPi.GPIO import *

class BB8:
    def __init__(self):
        self.port = serial.Serial("/dev/ttyUSB0", 38400)
        self.port.flushInput()
        self.buffer = ""
        setmode(BCM)
        setup(22, IN)
        self.Connected = False
        self.JustConnected = False
        self.JustDisconnected = False

    def Update(self):
        self.JustConnected = False
        self.JustDisconnected = False
        c = True if input(22) else False
        if c != self.Connected:
            self.Connected = c
            if c:
                self.JustConnected = True
            else:
                self.JustDisconnected = True
            self.port.flushInput()
            logging.info("BB8 Bluetooth " + ("Connected" if c else "Disconnected"))
        if self.Connected:
            a = self.port.inWaiting()
            for b in range(a):
                c = self.port.read()
                if c == '\r' or c == '\n':
                    if len(self.buffer) > 0:
                        logging.info("BB8 Message: " + self.buffer)
                    self.buffer = ""
                else:
                    self.buffer += c

    def SetDefault(self):
        if self.Connected:
            self.port.write('d')

    def SetOff(self):
        if self.Connected:
            self.port.write('e')

    def SetError(self):
        if self.Connected:
            self.port.write('e')

    def SetMessage(self):
        if self.Connected:
            self.port.write('m')

