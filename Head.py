from LogicDisplay import *
from ProcessStateIndicator import *
from HoloProjector import *
from MagicPanel import *
from LifeFormScanner import *
from Panels import *
from HeadMotor import *

class Head:
    def __init__(self):
        self.FrontLogicDisplay = FrontLogicDisplay()
        self.RearLogicDisplay = RearLogicDisplay()
        self.FrontProcessStateIndicator = FrontProcessStateIndicator()
        self.RearProcessStateIndicator = RearProcessStateIndicator()
        self.FrontHoloProjector = FrontHoloProjector()
        self.TopHoloProjector = TopHoloProjector()
        self.RearHoloProjector = RearHoloProjector()
        self.MagicPanel = MagicPanel()
        self.LifeFormScanner = LifeFormScanner()
        self.Panels = Panels()
        self.Motor = HeadMotor()

    def SetBrightness(self, brightness):
        self.FrontLogicDisplay.SetBrightness(brightness)
        self.RearLogicDisplay.SetBrightness(brightness)
        self.FrontProcessStateIndicator.SetBrightness(brightness)
        self.RearProcessStateIndicator.SetBrightness(brightness)
        self.FrontHoloProjector.SetBrightness(brightness)
        self.TopHoloProjector.SetBrightness(brightness)
        self.RearHoloProjector.SetBrightness(brightness)
        self.MagicPanel.SetBrightness(brightness)

    def SetDefault(self):
        self.FrontLogicDisplay.SetDefault()
        self.RearLogicDisplay.SetDefault()
        self.FrontProcessStateIndicator.SetDefault()
        self.RearProcessStateIndicator.SetDefault()
        self.FrontHoloProjector.SetDefault()
        self.TopHoloProjector.SetDefault()
        self.RearHoloProjector.SetDefault()
        self.MagicPanel.SetDefault()
        self.LifeFormScanner.SetDefault()
        #self.Motor.Enable()
        #self.Motor.SetAutomatic()

    def SetError(self):
        self.FrontLogicDisplay.SetError()
        self.RearLogicDisplay.SetError()
        self.FrontProcessStateIndicator.SetError()
        self.RearProcessStateIndicator.SetError()
        self.FrontHoloProjector.SetError()
        self.TopHoloProjector.SetError()
        self.RearHoloProjector.SetError()
        self.MagicPanel.SetError()
        self.LifeFormScanner.SetError()
        #self.Motor.Disable()

    def SetOff(self):
        self.FrontLogicDisplay.SetOff()
        self.RearLogicDisplay.SetOff()
        self.FrontProcessStateIndicator.SetOff()
        self.RearProcessStateIndicator.SetOff()
        self.FrontHoloProjector.SetOff()
        self.TopHoloProjector.SetOff()
        self.RearHoloProjector.SetOff()
        self.MagicPanel.SetOff()
        self.LifeFormScanner.SetOff()
        #self.Motor.Disable()

