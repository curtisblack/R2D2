import os
import logging
import serial
from RPi.GPIO import *

class BluetoothSerial:
    def __init__(self, usb, pin):
        self.usb = usb
        self.pin = pin
        self.port = None
        self.buffer = ""
        setmode(BCM)
        setup(self.pin, IN)
        self.Connected = False
        self.JustConnected = False
        self.JustDisconnected = False

    def Update(self):
        c = True if input(22) else False
        if self.port == None:
            if os.path.exists("/dev/ttyUSB" + str(self.usb)):
                self.port = serial.Serial("/dev/ttyUSB" + str(self.usb), 38400)
                self.port.flushInput()
            else:
                c = False
                return
        self.JustConnected = False
        self.JustDisconnected = False
        if c != self.Connected:
            self.Connected = c
            if c:
                self.JustConnected = True
            else:
                self.JustDisconnected = True
            self.port.flushInput()
            logging.info("Bluetooth Serial " + str(self.usb) + " " + ("Connected" if c else "Disconnected"))
        if self.Connected:
            a = self.port.inWaiting()
            for b in range(a):
                c = self.port.read()
                if c == '\r' or c == '\n':
                    if len(self.buffer) > 0:
                        logging.info("Bluetooth Serial " + str(self.usb) + " Message: " + self.buffer)
                    self.buffer = ""
                else:
                    self.buffer += c

    def Write(self, data):
        if self.Connected:
            self.port.write(data)

