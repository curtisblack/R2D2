from I2C import I2C
import random

class HoloProjector(I2C):
    def __init__(self, address, relay=None):
        I2C.__init__(self, address, relay)
        self.LightOn = False

    def SetBrightness(self, brightness):
        self.Send(10, [brightness])

    def SetDefault(self):
        self.Send(1)

    def SetOff(self):
        self.Send(2)
        self.LightOn = False

    def SetOn(self):
        self.Send(4)
        self.LightOn = True

    def SetError(self):
        self.Send(3)
        self.LightOn = True

    def SetMessage(self):
        self.Send(5)
        self.LightOn = True

    def SetPositionX(self, x):
        x = int(127 + float(x) * 127)
        self.Send(6, [x])

    def SetPositionY(self, y):
        y = int(127 + float(y) * 127)
        self.Send(7, [y])

    def SetPosition(self, x, y):
        x = int(127 + float(x) * 127)
        y = int(127 + float(y) * 127)
        self.Send(8, [x, y])

    def SetColor(self, r, g, b):
        self.Send(9, [r, g, b])
        self.LightOn = r > 0 or g > 0 or b > 0

    def ToggleLight(self):
        if self.LightOn:
            self.SetOff()
        else:
            #self.SetColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.SetOn()

class FrontHoloProjector(HoloProjector):
    def __init__(self, relay=None):
        HoloProjector.__init__(self, 25, relay)
        self.CheckCRC = True

class TopHoloProjector(HoloProjector):
    def __init__(self, relay=None):
        HoloProjector.__init__(self, 26, relay)

class RearHoloProjector(HoloProjector):
    def __init__(self, relay=None):
        HoloProjector.__init__(self, 27, relay)
        self.CheckCRC = True

import time
import random

class TwitchHoloProjector:
    def __init__(self, hp):
        self.HoloProjector = hp
        self.NextLightChange = 0
        self.NextPositionChange = 0

    def Update(self):
        t = time.time()
        if t > self.NextPositionChange:
            x = random.randint(-1000, 1000) / 1000.0
            y = random.randint(-1000, 1000) / 1000.0
            self.HoloProjector.SetPosition(x, y)
            self.NextPositionChange = t + random.randint(500, 5000) / 1000.0
        if t > self.NextLightChange:
            c = random.randint(0, 1)
            r = c * random.randint(0, 255)
            g = c * random.randint(0, 255)
            b = c * random.randint(0, 255)
            self.HoloProjector.SetColor(r, g, b)
            self.NextLightChange = t + random.randint(500, 5000) / 1000.0

