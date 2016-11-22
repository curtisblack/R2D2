import smbus
import logging

class HeadMotor:
    def __init__(self):
        self.address = 9
        self.i2c = smbus.SMBus(1)
        self.Enabled = False

    def SetSpeed(self, speed):
        try:
            self.i2c.write_i2c_block_data(self.address, 254, [speed])
        except IOError:
            logging.warning("I2C communication error in HeadMotor.SetSpeed")

    def SetManual(self):
        try:
            self.i2c.write_byte(self.address, 1)
        except IOError:
            logging.warning("I2C communication error in HeadMotor.SetManual")

    def SetAutomatic(self):
        try:
            self.i2c.write_byte(self.address, 2)
        except IOError:
            logging.warning("I2C communication error in HeadMotor.SetAutomatic")

    def Enable(self):
        try:
            self.i2c.write_byte(self.address, 251)
        except IOError:
            logging.warning("I2C communication error in HeadMotor.Enable")

    def Disable(self):
        try:
            self.i2c.write_byte(self.address, 252)
        except IOError:
            logging.warning("I2C communication error in HeadMotor.Disable")

    def Ping(self):
        try:
            self.i2c.write_byte(self.address, 255)
            self.Enabled = self.i2c.read_byte(self.address)
        except IOError:
            self.Enabled = False
            logging.warning("I2C communication error in HeadMotor.Ping")

