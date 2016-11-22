import logging

class VoltageDivider:
    def __init__(self, MCP3008, channel, R1, R2):
        self.MCP3008 = MCP3008
        self.channel = channel
        self.R1 = R1
        self.R2 = R2
        logging.info("Voltage divider on analog input {:} has maximum sensor voltage {:.2f} V".format(self.channel, 3.3 * (self.R1 + self.R2) / self.R2))

    def GetVoltage(self):
        V = 3.3 * self.MCP3008.read_adc(self.channel) / 1023.0
        return V * (self.R1 + self.R2) / self.R2

