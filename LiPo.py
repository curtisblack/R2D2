class LiPo:
    def __init__(self, voltage, current, cells, capacity):
        self.voltage = voltage
        self.current = current
        self.cells = cells
        self.capacity = capacity

    def ChargePercentage(self):
        v = self.voltage.GetVoltage() / self.cells
        percent = 100 * (v - 3.7) / (4.2 - 3.7)
        return max(0, min(100, int(percent)))

    def IsLowVoltage(self):
        return self.voltage.GetVoltage() < 3.7 * self.cells

    def IsCriticalVoltage(self):
        return self.voltage.GetVoltage() < 3.3 * self.cells

    def TimeRemaining(self):
        p = self.ChargePercentage()
        capacity = self.capacity * (p / 100.0)
        A = self.current.GetCurrent()
        return capacity / max(A, 0.001)
