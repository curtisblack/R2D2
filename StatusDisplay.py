import os
import re
import time
from LCD import LCD

class StatusDisplay(LCD):
    def __init__(self, r2d2):
        LCD.__init__(self, 0x20)
        self.R2D2 = r2d2
        #self.CreateChar(0, [0b01110,0b11111,0b10001,0b10001,0b10001,0b10001,0b10001,0b11111]) # battery
        self.CreateChar(1, [0b00010,0b00011,0b00010,0b00010,0b00010,0b01110,0b11110,0b01100]) # music note
        self.CreateChar(2, [0b01110, 0b10001, 0b10001, 0b10001, 0b01110, 0b01010, 0b01010, 0b00100]) # light bulb
        self.CreateChar(3, [0b01110, 0b10101, 0b10001, 0b01110, 0b10001, 0b10001, 0b10001, 0b01110]) # BB-8
        self.CreateChar(6, [0b00000,0b00000,0b00111,0b01000,0b10011,0b10100,0b10101,0b00000]) # wifi
        self.CreateChar(7, [0b01010,0b01010,0b11111,0b10001,0b10001,0b01110,0b00100,0b00100]) # power plug
        self.lastBattery = -1
        self.lastBrightness = -1
        self.lastIP = ""
        self.percent = []
        self.V = []
        self.A = []
        self.W = []
        self.lastLine1UpdateTime = 0
        self.lastLine2UpdateTime = 0
        self.lastLine3UpdateTime = 0
        self.lastLine4UpdateTime = 0

    def Update(self):
        percent = self.R2D2.Battery.ChargePercentage()
        V = self.R2D2.Voltage.GetVoltage()
        A = self.R2D2.Current.GetCurrent()
        self.percent.append(percent)
        self.V.append(V)
        self.A.append(A)
        self.W.append(V * A)

        t = time.time()

        if t > self.lastLine1UpdateTime + 1 or self.R2D2.BB8.JustConnected or self.R2D2.BB8.JustDisconnected:
            try:
                #if re.match("\d+\.\d+\.\d+\.\d+", self.lastIP):
                #    ip = os.popen("iwgetid -r").read()
                #    ip = ip[0:len(ip) - 1]
                #else:
                    ip = os.popen("ip addr show wlan0").read().split("inet ")[1].split("/")[0]# + " " + os.popen("iwgetid -r").read()
            except:
                try:
                    ip = os.popen("ip addr show eth0").read().split("inet ")[1].split("/")[0]
                except:
                    ip = "No Network"
            if ip != self.lastIP or self.R2D2.BB8.JustConnected or self.R2D2.BB8.JustDisconnected:
                line1 = "\6 " + ip
                if self.R2D2.BB8.Connected:
                    line1 = line1.ljust(19, ' ') + '\3'
                self.SetText(1, line1)
                self.lastIP = ip
                self.lastLine1UpdateTime = t

        if t > self.lastLine2UpdateTime + 1:
            percent = sum(self.percent) / len(self.percent)
            V = sum(self.V) / len(self.V)
            A = sum(self.A) / len(self.A)
            W = sum(self.W) / len(self.W)

            self.percent = []
            self.V = []
            self.A = []
            self.W = []

            c = 5 * percent / 100
            if c == 0 and c != self.lastBattery: self.CreateChar(0, [0b01110,0b11111,0b10001,0b10001,0b10001,0b10001,0b10001,0b11111]) # battery
            elif c == 1 and c != self.lastBattery: self.CreateChar(0, [0b01110,0b11011,0b10001,0b10001,0b10001,0b10001,0b11111,0b11111])
            elif c == 2 and c != self.lastBattery: self.CreateChar(0, [0b01110,0b11011,0b10001,0b10001,0b10001,0b11111,0b11111,0b11111])
            elif c == 3 and c != self.lastBattery: self.CreateChar(0, [0b01110,0b11011,0b10001,0b10001,0b11111,0b11111,0b11111,0b11111])
            elif c == 4 and c != self.lastBattery: self.CreateChar(0, [0b01110,0b11011,0b10001,0b11111,0b11111,0b11111,0b11111,0b11111])
            elif c == 5 and c != self.lastBattery: self.CreateChar(0, [0b01110,0b11111,0b11111,0b11111,0b11111,0b11111,0b11111,0b11111])
            self.lastBattery = c

            line2 = "\0 " + str(percent) + "% " + self.format(V) + "V " + self.format(A) + "A"
            self.SetText(2, line2)
            self.lastLine2UpdateTime = t

        if t > self.lastLine3UpdateTime + 0.05:
            b = int(100 * self.R2D2.BrightnessControl.GetValue())
            if abs(b - self.lastBrightness) > 2:
                line3 = "\1 " + ("mute" if self.R2D2.Sound.IsMute() else str(self.R2D2.Sound.Volume) + "%") + " \2 " + str(b) + "%"
                self.SetText(3, line3)
                self.lastBrightness = b
                self.lastLine3UpdateTime = t

        #h = self.R2D2.Battery.TimeRemaining()
        #h = percent * self.R2D2.Battery.capacity / (A * 100.0)
        #line3 = str(int(h)) + ":" + str(int(60 * (h - int(h)))).rjust(2, "0")
        #line4 = "%0.2fh" % self.R2D2.Battery.TimeRemaining()

    def format(self, number):
        if number >= 100:
            return str(int(round(number)))
        elif number >= 10:
            return "%.1f" % number
        else:
            return "%.2f" % number
