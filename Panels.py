import math
import time
import logging
from Adafruit_PCA9685 import *

class Panel:
    def __init__(self, panels, channel, minimum, maximum):
        self.panels = panels
        self.channel = channel
        self.minimum = minimum
        self.maximum = maximum
        self.state = 0

    def SetState(self, state):
        state = min(max(float(state), 0.0), 1.0)
        self.state = state
        try:
            self.panels.pwm.set_pwm(self.channel, 0, int(self.minimum + state * (self.maximum - self.minimum)))
        except IOError:
            logging.warning("I2C communication error in Panel.SetState")

    def Open(self):
        self.SetState(0)

    def Close(self):
        self.SetState(1)

    def IsOpen(self):
        return self.state == 0

    def IsClosed(self):
        return self.state == 1

class Panels:
    def __init__(self, address=64):
        try:
            self.pwm = PCA9685(address)
            self.pwm.set_pwm_freq(60)
        except IOError:
            logging.warning("I2C communication error in Panels.__init__")
        self.panels = [Panel(self, i, 180, 620) for i in range(13)]
        if address == 64: # head panels
            self.Top = self.panels[0]
            self.Panel1 = self.panels[1]
            self.Panel2 = self.panels[2]
            self.Panel3 = self.panels[3]
            self.Panel4 = self.panels[4]
            self.Panel7 = self.panels[5]
            self.Panel10 = self.panels[6]
            self.Panel11 = self.panels[7]
            self.Panel13 = self.panels[8]
            self.LightsaberLauncherPanel = self.PiePanel1 = self.panels[9] # Lightsaber Launcher
            self.LifeFormScannerPanel = self.PiePanel2 = self.panels[10] # Life Form Scanner
            self.PiePanel5 = self.panels[11]
            self.PiePanel6 = self.panels[12]

    def __getitem__(self, i):
        return self.panels[i]

    def __len__(self):
        return len(self.panels)
