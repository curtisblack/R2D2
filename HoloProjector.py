from I2C import I2C

class HoloProjector(I2C):
    def __init__(self, address, relay=None):
        I2C.__init__(self, address, relay)

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
    def __init__(self, relay=None):
        HoloProjector.__init__(self, 25, relay)

class TopHoloProjector(HoloProjector):
    def __init__(self, relay=None):
        HoloProjector.__init__(self, 26, relay)

class RearHoloProjector(HoloProjector):
    def __init__(self, relay=None):
        HoloProjector.__init__(self, 27, relay)


