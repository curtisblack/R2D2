from I2C import I2C

class LogicDisplay(I2C):
    def __init__(self, address, relay=None):
        I2C.__init__(self, address, relay)

    def SetBrightness(self, brightness):
        self.Send(4, [brightness])

    def SetDefault(self):
        self.Send(1)

    def SetOff(self):
        self.Send(2)

    def SetError(self):
        self.Send(3)

class FrontLogicDisplay(LogicDisplay):
    def __init__(self, relay=None):
        LogicDisplay.__init__(self, 11, relay)

class RearLogicDisplay(LogicDisplay):
    def __init__(self, relay=None):
        LogicDisplay.__init__(self, 10, relay)
