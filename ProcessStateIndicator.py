import smbus
import logging

class ProcessStateIndicator:
    def __init__(self, address):
        self.address = address
        self.i2c = smbus.SMBus(1)

    def SetBrightness(self, brightness):
        try:
            self.i2c.write_i2c_block_data(self.address, 255, [brightness])
        except IOError:
            logging.warning("I2C communication error in " + self.Name + "ProcessStateIndicator.SetBrightness")

    def SetDefault(self):
        try:
            self.i2c.write_byte(self.address, 0)
        except IOError:
            logging.warning("I2C communication error in " + self.Name + "ProcessStateIndicator.SetDefault")

    def SetOff(self):
        try:
            self.i2c.write_byte(self.address, 1)
        except IOError:
            logging.warning("I2C communication error in " + self.Name + "ProcessStateIndicator.SetOff")

    def SetError(self):
        try:
            self.i2c.write_byte(self.address, 2)
        except IOError:
            logging.warning("I2C communication error in " + self.Name + "ProcessStateIndicator.SetError")

    def SetColor1(self, r, g, b):
        try:
            self.i2c.write_i2c_block_data(self.address, 252, [r, g, b])
        except IOError:
            logging.warning("I2C communication error in " + self.Name + "ProcessStateIndicator.SetColor1")

    def SetColor2(self, r, g, b):
        try:
            self.i2c.write_i2c_block_data(self.address, 253, [r, g, b])
        except IOError:
            logging.warning("I2C communication error in " + self.Name + "ProcessStateIndicator.SetColor2")

    def ResetColors(self):
        try:
            self.i2c.write_byte(self.address, 254)
        except IOError:
            logging.warning("I2C communication error in " + self.Name + "ProcessStateIndicator.ResetColors")

class FrontProcessStateIndicator(ProcessStateIndicator):
    def __init__(self):
        ProcessStateIndicator.__init__(self, 28)
        self.Name = "Front"

class RearProcessStateIndicator(ProcessStateIndicator):
    def __init__(self):
        ProcessStateIndicator.__init__(self, 29)
        self.Name = "Rear"

