from BluetoothSerial import *

class BB8(BluetoothSerial):
    def __init__(self):
        BluetoothSerial.__init__(self, 0, 12)

    def SetDefault(self):
        self.Write('d')

    def SetOff(self):
        self.Write('o')

    def SetError(self):
        self.Write('e')

    def SetMessage(self):
        self.Write('m')

