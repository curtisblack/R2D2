import os
import termios
import time
import glob
import logging

class Maestro:
    def __init__(self, serial, servos=24, resetPin=255, deviceNumber=255, CRCEnabled=False):
        self.serial = serial
        self.resetPin = resetPin
        self.deviceNumber = deviceNumber
        self.servos = servos
        self.targets = {}
        self.moveStatus = {}
        self.registered = {}
        for i in range(self.servos):
            self.targets[i] = 0
            self.moveStatus[i] = 0
            self.registered[i] = False
        self.stream = None
        self.begin()

    def begin(self):
        self.Close()
        devices = sorted(glob.glob("/dev/serial/by-id/usb*Pololu*Maestro*" + self.serial + "*"))
        for device in devices:
            try:
                logging.info("Using Maestro servo controller on " + device + ".")
                self.stream = os.open(device, os.O_RDWR | os.O_NOCTTY)
                options = termios.tcgetattr(self.stream)
                options[0] &= ~(termios.INLCR | termios.IGNCR | termios.ICRNL | termios.IXON | termios.IXOFF)
                options[1] &= ~(termios.ONLCR | termios.OCRNL)
                options[3] &= ~(termios.ECHO | termios.ECHONL | termios.ICANON | termios.ISIG | termios.IEXTEN)
                termios.tcsetattr(self.stream, termios.TCSANOW, options)
                break
            except:
                self.stream = None
                logging.warning("Unable to connect to Maestro servo controller")

    def Close(self):
        if self.stream == None:
            return
        try:
            os.close(self.stream)
        except:
            pass
        self.stream = None

    def Reset(self):
        if self.resetPin != 255:
            pass
            #digitalWrite(self.resetPin, LOW)
            #pinMode(self.resetPin, OUTPUT)
            #delay(1)
            #pinMode(self.resetPin, INPUT)
            #delay(200)

    def Disable(self, channel):
        if self.stream == None:
            self.begin()
        try:
            os.write(self.stream, "".join(map(chr, [0x84, channel, 0, 0])))
            #os.flush(self.stream)
        except:
            self.Close()

    def Enable(self, channel):
        if self.stream == None:
            self.begin()
        try:
            self.SetTarget(channel, self.targets[channel])
        except:
            self.Close()
    
    def SetTarget(self, channel, target):
        if self.stream == None:
            self.begin()
        if self.targets[channel] == target:
            return
        try:
            self.moveStatus[channel] = -1
            self.targets[channel] = target
            target = int(target * 4)
            os.write(self.stream, "".join(map(chr, [0x84, channel, target & 0x7F, (target >> 7) & 0x7F])))
            #os.flush(self.stream)
        except:
            self.Close()

    def SetSpeed(self, channel, speed):
        if self.stream == None:
            self.begin()
        try:
            speed = int(speed * 4)
            os.write(self.stream, "".join(map(chr, [0x87, channel, speed & 0x7F, (speed >> 7) & 0x7F])))
            #os.flush(self.stream)
        except:
            self.Close()

    def SetAcceleration(self, channel, acceleration):
        if self.stream == None:
            self.begin()
        try:
            acceleration = int(acceleration * 4)
            os.write(self.stream, "".join(map(chr, [0x89, channel, acceleration & 0x7F, (acceleration >> 7) & 0x7F])))
            #os.flush(self.stream)
        except:
            self.Close()

    def GetPosition(self, channel):
        if self.stream == None:
            self.begin()
        try:
            os.write(self.stream, "".join(map(chr, [0x90, channel])))
            #os.flush(self.stream)
            r1 = os.read(self.stream, 1)
            r2 = os.read(self.stream, 1)
            return (ord(r1) + 256 * ord(r2)) / 4
        except:
            self.Close()
            return 0

    def Update(self):
        if self.stream == None:
            return
        try:
            for i in range(self.servos):
                if self.registered[i]:
                    if self.targets[i] != 0 and self.moveStatus[i] < 0:
                        p = self.GetPosition(i)
                        if p != 0 and self.targets[i] == p:
                            self.moveStatus[i] = time.time()
                    elif self.moveStatus[i] > 0:
                        if self.moveStatus[i] + 0.5 < time.time():
                            #self.Disable(i)
                            self.moveStatus[i] = 0
        except:
            self.Close()

class MaestroServo:
    def __init__(self, maestro, channel, minimum=1000, maximum=2000, speed=0, acceleration=0):
        self.maestro = maestro
        self.channel = channel
        self.minimum = minimum
        self.maximum = maximum
        self.speed = speed
        self.acceleration = acceleration
        self.maestro.registered[channel] = True
        self.maestro.SetSpeed(channel, speed)
        self.maestro.SetAcceleration(channel, acceleration)

    def SetTarget(self, target):
        self.Enable()
        self.maestro.SetSpeed(self.channel, self.speed)
        self.maestro.SetAcceleration(self.channel, self.acceleration)
        self.maestro.SetTarget(self.channel, int(self.minimum + target * (self.maximum - self.minimum)))
        #self.maestro.SetAcceleration(self.channel, self.acceleration)
        #self.maestro.SetSpeed(self.channel, self.speed)

    def Open(self):
        self.SetTarget(1)

    def Close(self):
        self.SetTarget(0)

    def Enable(self):
        self.maestro.Enable(self.channel)

    def Disable(self):
        self.maestro.Disable(self.channel)

    def Toggle(self):
        mid = (self.minimum + self.maximum) / 2
        if self.maestro.targets[self.channel] > mid:
            self.SetTarget(0)
        else:
            self.SetTarget(1)
