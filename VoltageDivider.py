import logging

class VoltageDivider:
    def __init__(self, MCP3008, channel, R1, R2):
        self.MCP3008 = MCP3008
        self.channel = channel
        self.R1 = float(R1)
        self.R2 = float(R2)
        self.Vcc = 3.3
        logging.info("Voltage divider on analog input {:} has maximum sensor voltage {:.2f} V".format(self.channel, self.Vcc * (self.R1 + self.R2) / self.R2))

    def GetVoltage(self):
        V = self.Vcc * self.MCP3008.read_adc(self.channel) / 1023.0
        return V * (self.R1 + self.R2) / self.R2

