import atexit
import time
import logging
import RPi.GPIO as GPIO
from Relay import *
from LED import *
from Sound import *
from Network import *
from ACS711EX import ACS711EX
from VoltageDivider import *
from LiPo import *
from StatusDisplay import *
from Potentiometer import *
from LogicDisplay import *
from ProcessStateIndicator import *
from HoloProjector import *
from MagicPanel import *
from LifeFormScanner import *
from Panels import *
from HeadMotor import *
from Maestro import *
from BB8 import *
import Adafruit_GPIO.SPI as SPI
from Adafruit_MCP3008 import MCP3008

class R2D2:
    def __init__(self):
        logging.basicConfig(format="%(levelname)s (%(asctime)s): %(message)s", datefmt="%I:%M:%S %p", level=logging.INFO, filename="/var/tmp/R2D2.log")        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        atexit.register(self.Exit)
        self.MCP3008 = MCP3008(spi=SPI.SpiDev(0, 0))
        self.Voltage = VoltageDivider(self.MCP3008, 0, 984.0, 101.0)
        self.Current = ACS711EX(self.MCP3008, 1)
        self.BrightnessControl = Potentiometer(self.MCP3008, 2)
        self.Battery = LiPo(self.Voltage, self.Current, 6, 10)
        
        self.DomeLightsRelay = self.Relay1 = Relay(16)
        self.DomeServosRelay = self.Relay2 = Relay(17)
        self.DomeMotorRelay = self.Relay3 = Relay(18)
        self.Relay4 = Relay(19)
        self.Relay5 = Relay(20)
        self.SoundRelay = self.Relay6 = Relay(21)
        self.BodyServosRelay = self.Relay7 = Relay(22)
        self.BodyLightsRelay = self.Relay8 = Relay(23)
        self.Relay9 = Relay(24)
        self.Relay10 = Relay(25)
        self.Relay11 = Relay(26)
        self.Relay12 = Relay(27)

        self.Network = Network()
        
        self.Head = HeadMotor(self.DomeMotorRelay)
        self.Sound = Sound()
        self.StatusDisplay = StatusDisplay(self)

        self.FrontLogicDisplay = FrontLogicDisplay(self.DomeLightsRelay)
        self.RearLogicDisplay = RearLogicDisplay(self.DomeLightsRelay)
        self.FrontProcessStateIndicator = FrontProcessStateIndicator(self.DomeLightsRelay)
        self.RearProcessStateIndicator = RearProcessStateIndicator(self.DomeLightsRelay)
        self.FrontHoloProjector = FrontHoloProjector(self.DomeLightsRelay)
        self.TopHoloProjector = TopHoloProjector(self.DomeLightsRelay)
        self.RearHoloProjector = RearHoloProjector(self.DomeLightsRelay)
        self.MagicPanel = MagicPanel(self.DomeLightsRelay)
        self.LifeFormScanner = LifeFormScanner(self.DomeLightsRelay)
        self.DomePanels = Panels()
        
        self.BodyServos = Maestro()
        self.LeftUtilityArm = MaestroServo(self.BodyServos, 16, 2390, 1520, 20, 1)
        self.RightUtilityArm = MaestroServo(self.BodyServos, 17, 2390, 1520, 20, 1)

    def Exit(self):
        self.Relay1.Disable()
        self.Relay2.Disable()
        self.Relay3.Disable()
        self.Relay4.Disable()
        self.Relay5.Disable()
        self.Relay6.Disable()
        self.Relay7.Disable()
        self.Relay8.Disable()
        self.Relay9.Disable()
        self.Relay10.Disable()
        self.Relay11.Disable()
        self.Relay12.Disable()
        self.StatusDisplay.SetBacklight(False)
        self.StatusDisplay.Clear()
        self.BodyServos.Close()
        GPIO.cleanup()

    def SetBrightness(self, brightness, limit = True):
        if self.DomeLightsRelay.Enabled:
            self.FrontLogicDisplay.SetBrightness(min(127, brightness / 2) if limit else brightness)
            self.RearLogicDisplay.SetBrightness(min(127, brightness / 2) if limit else brightness)
            self.FrontProcessStateIndicator.SetBrightness(min(127, brightness / 2) if limit else brightness)
            self.RearProcessStateIndicator.SetBrightness(min(127, brightness / 2) if limit else brightness)
            self.FrontHoloProjector.SetBrightness(brightness)
            self.TopHoloProjector.SetBrightness(brightness)
            self.RearHoloProjector.SetBrightness(brightness)
            self.MagicPanel.SetBrightness(brightness)

    def SetDefault(self):
        if self.DomeLightsRelay.Enabled:
            self.FrontLogicDisplay.SetDefault()
            self.RearLogicDisplay.SetDefault()
            self.FrontProcessStateIndicator.SetDefault()
            self.RearProcessStateIndicator.SetDefault()
            self.FrontHoloProjector.SetDefault()
            self.TopHoloProjector.SetDefault()
            self.RearHoloProjector.SetDefault()
            self.MagicPanel.SetDefault()
            self.LifeFormScanner.SetDefault()

    def SetError(self):
        if self.DomeLightsRelay.Enabled:
            self.FrontLogicDisplay.SetError()
            self.RearLogicDisplay.SetError()
            self.FrontProcessStateIndicator.SetError()
            self.RearProcessStateIndicator.SetError()
            self.FrontHoloProjector.SetError()
            self.TopHoloProjector.SetError()
            self.RearHoloProjector.SetError()
            self.MagicPanel.SetError()
            self.LifeFormScanner.SetError()

    def SetOff(self):
        if self.DomeLightsRelay.Enabled:
            self.FrontLogicDisplay.SetOff()
            self.RearLogicDisplay.SetOff()
            self.FrontProcessStateIndicator.SetOff()
            self.RearProcessStateIndicator.SetOff()
            self.FrontHoloProjector.SetOff()
            self.TopHoloProjector.SetOff()
            self.RearHoloProjector.SetOff()
            self.MagicPanel.SetOff()
            self.LifeFormScanner.SetOff()
