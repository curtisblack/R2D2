class Potentiometer:
    def __init__(self, MCP3008, channel):
        self.MCP3008 = MCP3008
        self.channel = channel

    def GetValue(self):
        return self.MCP3008.read_adc(self.channel) / 1023.0

