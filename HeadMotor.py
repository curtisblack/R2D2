import time
from I2C import I2C

class HeadMotor(I2C):
    def __init__(self, relay=None):
        I2C.__init__(self, 9, relay)
        self.lastPing = 0

    def SetSpeed(self, speed):
        #speed = speed * speed if speed >= 0 else -speed * speed
        speed = int(127 + 127 * speed)
        self.Send(6, [speed])

    def SetPosition(self, position):
        b = int(255 * (position + 180) / 360)
        if b < 0: b = 0
        if b > 255: b = 255
        self.Send(5, [b])

    def Enable(self):
        self.Send(3)

    def Disable(self):
        self.Send(4)

    def SetRequirePing(self, require):
        self.Send(7, [1 if require else 0])

    def Ping(self):
        t = time.time()
        if t > self.lastPing + 0.05:
            self.Send(8)
            self.lastPing = t


