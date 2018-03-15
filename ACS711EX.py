class ACS711EX:
    def __init__(self, MCP3008, channel):
        self.MCP3008 = MCP3008
        self.channel = channel

    def GetCurrent(self):
        return abs(36.7 * self.MCP3008.read_adc(self.channel) / 1023.0 - 18.35)

