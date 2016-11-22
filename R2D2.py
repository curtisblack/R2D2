import atexit
import time
import logging
from RPi.GPIO import *
from Relay import *
from LED import *
from Head import *
from Sound import *
from ACS711EX import *
from VoltageDivider import *
from LiPo import *
import Adafruit_GPIO.SPI as SPI
from Adafruit_MCP3008 import *

class R2D2:
    def __init__(self):
        logging.basicConfig(format="%(levelname)s (%(asctime)s): %(message)s", datefmt="%I:%M:%S %p", level=logging.DEBUG)
        setmode(BCM)
        atexit.register(self.Exit)
        self.MCP3008 = MCP3008(clk=24, cs=27, miso=25, mosi=26)
        self.Current = ACS711EX(self.MCP3008, 0)
        self.Voltage = VoltageDivider(self.MCP3008, 1, 1.011e6, 0.98e5)
        self.Battery = LiPo(self.Voltage, 3, 2.2)
        self.DomeLights = self.Relay1 = Relay(4)
        self.DomeServos = self.Relay2 = Relay(5)
        self.Relay3 = Relay(6)
        self.Relay4 = Relay(12)
        self.BodyLights = self.Relay5 = Relay(13)
        self.BodyServos = self.Relay6 = Relay(16)
        self.Relay7 = Relay(17)
        self.Relay8 = Relay(19)
        self.Head = Head()
        self.Sound = Sound()

    def Exit(self):
        self.Relay1.Disable()
        self.Relay2.Disable()
        self.Relay3.Disable()
        self.Relay4.Disable()
        self.Relay5.Disable()
        self.Relay6.Disable()
        self.Relay7.Disable()
        self.Relay8.Disable()
        cleanup()

    def SetBrightness(self, brightness):
        self.Head.SetBrightness(brightness)

