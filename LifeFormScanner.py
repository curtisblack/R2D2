import smbus
import logging

class LifeFormScanner:
    def __init__(self):
        self.address = 22
        self.i2c = smbus.SMBus(1)

    def SetDefault(self):
        try:
            self.i2c.write_byte(self.address, 0)
        except IOError:
            logging.warning("I2C communication error in LifeFormScanner.SetDefault")

    def SetOff(self):
        try:
            self.i2c.write_byte(self.address, 1)
        except IOError:
            logging.warning("I2C communication error in LifeFormScanner.SetOff")

    def SetError(self):
        try:
            self.i2c.write_byte(self.address, 2)
        except IOError:
            logging.warning("I2C communication error in LifeFormScanner.SetError")

    def SetOn(self):
        try:
            self.i2c.write_byte(self.address, 3)
        except IOError:
            logging.warning("I2C communication error in LifeFormScanner.SetOn")
