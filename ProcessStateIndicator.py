from I2C import I2C

class ProcessStateIndicator(I2C):
    def __init__(self, address, relay=None):
        I2C.__init__(self, address, relay)

    def SetBrightness(self, brightness):
        self.Send(7, [brightness])

    def SetDefault(self):
        self.Send(1)

    def SetOff(self):
        self.Send(2)

    def SetError(self):
        self.Send(3)

    def SetColor1(self, r, g, b):
        self.Send(4, [r, g, b])

    def SetColor2(self, r, g, b):
        self.Send(5, [r, g, b])

    def ResetColors(self):
        self.Send(6)

    def SetTransition(self, duration, minPause, maxPause):
        self.Send(8, [duration / 10, minPause / 100, maxPause / 100])

    def ResetTransition(self):
        self.Send(9)

class FrontProcessStateIndicator(ProcessStateIndicator):
    def __init__(self, relay=None):
        ProcessStateIndicator.__init__(self, 28, relay)

class RearProcessStateIndicator(ProcessStateIndicator):
    def __init__(self, relay=None):
        ProcessStateIndicator.__init__(self, 29, relay)

