from I2C import I2C

class LifeFormScanner(I2C):
    def __init__(self, relay=None):
        I2C.__init__(self, 22, relay)

    def SetOff(self):
        self.Send(2)

    def SetOn(self):
        self.Send(3)
