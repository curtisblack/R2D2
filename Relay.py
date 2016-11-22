from RPi.GPIO import *

class Relay:
    def __init__(self, pin):
        self.pin = pin
        setup(self.pin, OUT)
        self.Enabled = False

    def Enable(self):
        output(self.pin, True)
        self.Enabled = True

    def Disable(self):
        output(self.pin, False)
        self.Enabled = False
