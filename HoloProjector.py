import smbus
import logging

class HoloProjector:
    def __init__(self, address):
        self.address = address
        self.i2c = smbus.SMBus(1)

    def SetBrightness(self, brightness):
        try:
            self.i2c.write_i2c_block_data(self.address, 255, [brightness])
        except IOError:
            logging.warning("I2C communication error in " + self.Name + "HoloProjector.SetBrightness")

    def SetDefault(self):
        try:
            self.i2c.write_byte(self.address, 0)
        except IOError:
            logging.warning("I2C communication error in " + self.Name + "HoloProjector.SetDefault")

    def SetOff(self):
        try:
            self.i2c.write_byte(self.address, 1)
        except IOError:
            logging.warning("I2C communication error in " + self.Name + "HoloProjector.SetOff")

    def SetError(self):
        try:
            self.i2c.write_byte(self.address, 2)
        except IOError:
            logging.warning("I2C communication error in " + self.Name + "HoloProjector.SetError")

    def SetMessage(self):
        try:
            self.i2c.write_byte(self.address, 3)
        except IOError:
            logging.warning("I2C communication error in " + self.Name + "HoloProjector.SetMessage")

    def SetColor(self, r, g, b):
        try:
            self.i2c.write_i2c_block_data(self.address, 254, [r, g, b])
        except IOError:
            logging.warning("I2C communication error in " + self.Name + "HoloProjector.SetColor")

class FrontHoloProjector(HoloProjector):
    def __init__(self):
        HoloProjector.__init__(self, 25)
        self.Name = "Front"

class TopHoloProjector(HoloProjector):
    def __init__(self):
        HoloProjector.__init__(self, 26)
        self.Name = "Top"

class RearHoloProjector(HoloProjector):
    def __init__(self):
        HoloProjector.__init__(self, 27)
        self.Name = "Rear"

