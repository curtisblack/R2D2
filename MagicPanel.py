import time
from I2C import I2C

class MagicPanel(I2C):
    def __init__(self, relay=None):
        I2C.__init__(self, 20, relay)
        self.lastPing = 0

    def SetBrightness(self, brightness):
        self.Send(7, [brightness])

    def SetDefault(self):
        self.Send(1)

    def SetOff(self):
        self.Send(2)

    def SetError(self):
        self.Send(3)

    def SetOn(self):
        self.Send(4)

    def Ping(self):
        t = time.time()
        if t > self.lastPing + 0.5:
            self.Send(6)
            self.lastPing = t

    def SetRequirePing(self, require):
        self.Send(5, [1 if require else 0])
