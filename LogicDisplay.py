import smbus
import logging

class LogicDisplay:
    def __init__(self, address):
        self.address = address
        self.i2c = smbus.SMBus(1)

    def SetBrightness(self, brightness):
        try:
            self.i2c.write_i2c_block_data(self.address, 255, [brightness])
        except IOError:
            logging.warning("I2C communication error in " + self.Name + "LogicDisplay.SetBrightness")

    def SetDefault(self):
        try:
            self.i2c.write_byte(self.address, 0)
        except IOError:
            logging.warning("I2C communication error in " + self.Name + "LogicDisplay.SetDefault")

    def SetOff(self):
        try:
            self.i2c.write_byte(self.address, 1)
        except IOError:
            logging.warning("I2C communication error in " + self.Name + "LogicDisplay.SetOff")

    def SetError(self):
        try:
            self.i2c.write_byte(self.address, 2)
        except IOError:
            logging.warning("I2C communication error in " + self.Name + "LogicDisplay.SetError")

class FrontLogicDisplay(LogicDisplay):
    def __init__(self):
        LogicDisplay.__init__(self, 11)
        self.Name = "Front"

class RearLogicDisplay(LogicDisplay):
    def __init__(self):
        LogicDisplay.__init__(self, 10)
        self.Name = "Rear"
