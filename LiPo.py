class LiPo:
    def __init__(self, voltageDivider, cells, capacity):
        self.voltageDivider = voltageDivider
        self.cells = cells
        self.capacity = capacity

    def IsLowVoltage(self):
        return self.voltageDivider.GetVoltage() < 3.3 * self.cells

    def IsCriticalVoltage(self):
        return self.voltageDivider.GetVoltage() < 3.0 * self.cells
