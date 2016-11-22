import smbus
import logging

class MagicPanel:
    def __init__(self):
        self.address = 20
        self.i2c = smbus.SMBus(1)

    def SetBrightness(self, brightness):
        try:
            self.i2c.write_i2c_block_data(self.address, 255, [brightness])
        except IOError:
            logging.warning("I2C communication error in MagicPanel.SetBrightness")

    def SetDefault(self):
        try:
            self.i2c.write_byte(self.address, 0)
        except IOError:
            logging.warning("I2C communication error in MagicPanel.SetDefault")

    def SetOff(self):
        try:
            self.i2c.write_byte(self.address, 1)
        except IOError:
            logging.warning("I2C communication error in MagicPanel.SetOff")

    def SetError(self):
        try:
            self.i2c.write_byte(self.address, 2)
        except IOError:
            logging.warning("I2C communication error in MagicPanel.SetError")

    def SetOn(self):
        try:
            self.i2c.write_byte(self.address, 3)
        except IOError:
            logging.warning("I2C communication error in MagicPanel.SetOn")
