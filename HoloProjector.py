from I2C import I2C

class HoloProjector(I2C):
    def __init__(self, address):
        I2C.__init__(self, address)

    def SetBrightness(self, brightness):
        self.Send(9, [brightness])

    def SetDefault(self):
        self.Send(1)

    def SetOff(self):
        self.Send(2)

    def SetOn(self):
        self.Send(4)

    def SetError(self):
        self.Send(3)

    def SetMessage(self):
        self.Send(5)

    def SetColor(self, r, g, b):
        self.Send(8, [r, g, b])

class FrontHoloProjector(HoloProjector):
    def __init__(self):
        HoloProjector.__init__(self, 25)

class TopHoloProjector(HoloProjector):
    def __init__(self):
        HoloProjector.__init__(self, 26)

class RearHoloProjector(HoloProjector):
    def __init__(self):
        HoloProjector.__init__(self, 27)


