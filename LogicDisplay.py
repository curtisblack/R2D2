from I2C import I2C

class LogicDisplay(I2C):
    def __init__(self, address):
        I2C.__init__(self, address)

    def SetBrightness(self, brightness):
        self.Send(4, [brightness])

    def SetDefault(self):
        self.Send(1)

    def SetOff(self):
        self.Send(2)

    def SetError(self):
        self.Send(3)

class FrontLogicDisplay(LogicDisplay):
    def __init__(self):
        LogicDisplay.__init__(self, 11)

class RearLogicDisplay(LogicDisplay):
    def __init__(self):
        LogicDisplay.__init__(self, 10)
