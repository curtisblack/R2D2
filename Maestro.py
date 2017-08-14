import os
import termios
import time
import glob

class Maestro:
    def __init__(self, port="/dev/ttyACM0", resetPin=255, deviceNumber=255, CRCEnabled=False):
        self.resetPin = resetPin
        self.deviceNumber = deviceNumber
        self.targets = {}
        self.moveStatus = {}
        for i in range(24):
            self.targets[i] = 0
            self.moveStatus[i] = 0
        self.stream = os.open(sorted(glob.glob("/dev/ttyACM*"))[0], os.O_RDWR | os.O_NOCTTY)
        options = termios.tcgetattr(self.stream)
        options[0] &= ~(termios.INLCR | termios.IGNCR | termios.ICRNL | termios.IXON | termios.IXOFF)
        options[1] &= ~(termios.ONLCR | termios.OCRNL)
        options[3] &= ~(termios.ECHO | termios.ECHONL | termios.ICANON | termios.ISIG | termios.IEXTEN)
        termios.tcsetattr(self.stream, termios.TCSANOW, options)

    def Close(self):
        os.close(self.stream)

    def Reset(self):
        if self.resetPin != 255:
            pass
            #digitalWrite(self.resetPin, LOW)
            #pinMode(self.resetPin, OUTPUT)
            #delay(1)
            #pinMode(self.resetPin, INPUT)
            #delay(200)

    def Disable(self, channel):
        os.write(self.stream, "".join(map(chr, [0x84, channel, 0, 0])))

    def Enable(self, channel):
        self.SetTarget(channel, self.targets[channel])

    def SetTarget(self, channel, target):
        if self.targets[channel] == target:
            return
        self.moveStatus[channel] = -1
        self.targets[channel] = target
        target = int(target * 4)
        os.write(self.stream, "".join(map(chr, [0x84, channel, target & 0x7F, (target >> 7) & 0x7F])))

    def SetSpeed(self, channel, speed):
        speed = int(speed * 4)
        os.write(self.stream, "".join(map(chr, [0x87, channel, speed & 0x7F, (speed >> 7) & 0x7F])))

    def SetAcceleration(self, channel, acceleration):
        acceleration = int(acceleration * 4)
        os.write(self.stream, "".join(map(chr, [0x89, channel, acceleration & 0x7F, (acceleration >> 7) & 0x7F])))

    def GetPosition(self, channel):
        os.write(self.stream, "".join(map(chr, [0x90, channel])))
        r1 = os.read(self.stream, 1)
        r2 = os.read(self.stream, 1)
        return (ord(r1) + 256 * ord(r2)) / 4

    def Update(self):
        for i in range(2):
            if self.targets[i] != 0 and self.moveStatus[i] < 0:
                p = self.GetPosition(i)
                if p != 0 and self.targets[i] == p:
                    self.moveStatus[i] = time.time()
            elif self.moveStatus[i] > 0:
                if self.moveStatus[i] + 0.5 < time.time():
                    #self.Disable(i)
                    self.moveStatus[i] = 0

class MaestroServo:
    def __init__(self, maestro, channel, minimum=1000, maximum=2000, speed=0, acceleration=0):
        self.maestro = maestro
        self.channel = channel
        self.minimum = minimum
        self.maximum = maximum
        self.speed = speed
        self.acceleration = acceleration
        self.maestro.SetSpeed(channel, speed)
        self.maestro.SetAcceleration(channel, acceleration)

    def SetTarget(self, target):
        self.Enable()
        self.maestro.SetSpeed(self.channel, self.speed)
        self.maestro.SetAcceleration(self.channel, self.acceleration)
        self.maestro.SetTarget(self.channel, int(self.minimum + target * (self.maximum - self.minimum)))
        #self.maestro.SetAcceleration(self.channel, self.acceleration)
        #self.maestro.SetSpeed(self.channel, self.speed)


    def Enable(self):
        self.maestro.Enable(self.channel)

    def Disable(self):
        self.maestro.Disable(self.channel)
