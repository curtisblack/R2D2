import sys
import time
import math
from Wire import *

tests = sys.argv[2:]

# Ah ratings of batteries
batteries = [20]

# current ratings of fuses
fuses = [2, 3, 5, 7.5, 10, 15, 20, 25, 30, 35]
def FindFuse(I):
    for f in fuses:
        if f > I:
            return f
    return I

# lengths of wires (in metres, round trip) from each of the fuses to their final destination
wireLengths = {
    -1: 1.0, # battery to fuse block
     1: 0.5, # raspberry pi
     2: 0,
     3: 3.0, # dome lights
     4: 0, # body lights
     5: 0, # dome servos
     6: 0, # body servos
     7: 1.0, # dome motor
     8: 1.0, # sound system
     9: 0,
    10: 0,
    11: 0, # left foot motor
    12: 0, # right foot motor
}

#r2.StatusDisplay.SetText(4, "Running Diagnostics")

r2.Relay1.Disable()
r2.Relay2.Disable()
r2.Relay3.Disable()
r2.Relay4.Disable()
r2.Relay5.Disable()
r2.Relay6.Disable()
r2.Relay7.Disable()
r2.Relay8.Disable()

#r2.Relay2.Enable()
#r2.Relay3.Enable()
#r2.Relay4.Enable()
#r2.Relay5.Enable()
#r2.Relay6.Enable()
#r2.Relay7.Enable()
#r2.Relay8.Enable()

def MeasureCurrent(count=50000):
    m = 0
    a = 0
    for i in range(count):
        c = r2.Current.GetCurrent()
        a += c
        m = max(m, c)
    return (a / count, m)

def AverageVoltage(count=10000):
    V = 0
    for i in range(count):
        V += r2.Voltage.GetVoltage()
    return V / count;

def PrintPower(Iavg, Imax, fuse=0):
    print "Average current: {:.2f}".format(Iavg)
    print "Maximum current: {:.2f} A".format(Imax)
    if fuse > 0:
        f = FindFuse(Imax)
        print "Fuse {:} should be at least {:} A".format(fuse, f)
        print "Wire from fuse {:} should be at least {:}".format(fuse, CalculateWireSize(V, f, wireLengths[fuse], loss=3))
    elif fuse == -1:
        print "Wire from battery to fuse block should be at lease {:}".format(CalculateWireSize(V, Imax, wireLengths[fuse]))
    print "Average power {:.2f} W".format(Iavg * V)
    print "Maximum power: {:.2f} W".format(Imax * V)
    for B in batteries:
        t = B / Iavg
        h = int(math.floor(t))
        m = int((t - h) * 60)
        d = (str(h) + "h, " + str(m) + "m") if h >= 1 else (str(m) + "m")
        print "Average runtime on " + str(B) + "Ah battery: " + d

print
print "==================="
print "RUNNING DIAGNOSTICS"
print "==================="

print

print "Measuring battery voltage"
print "-------------------------"
V = AverageVoltage()
print "Voltage: {:.2f} V".format(V)

print
print "Measuring microcontroller current (fuse 1)"
print "------------------------------------------"
Iidle = MeasureCurrent()
PrintPower(Iidle[0], Iidle[1], 1)

def DomeLights(brightness):
    print
    s = "Measuring dome lights current (fuse 3) at brightness = " + str(brightness)
    print s
    print "-" * len(s)
    if not r2.DomeLightsRelay.Enabled:
        r2.DomeLightsRelay.Enable()
        time.sleep(2)
    if brightness >= 0:
        #r2.Head.SetDefault()
        #r2.LifeFormScanner.SetOn()
        r2.MagicPanel.SetOn()
        r2.FrontHoloProjector.SetOn()
        r2.RearHoloProjector.SetOn()
        r2.TopHoloProjector.SetOn()
        r2.SetBrightness(brightness, limit=False)
    #else:
    #    r2.Head.SetOff()
    time.sleep(0.1)
    IdomeLights = MeasureCurrent()
    IdomeLights = (IdomeLights[0] - Iidle[0], IdomeLights[1] - Iidle[0])
    PrintPower(IdomeLights[0], IdomeLights[1], 3)
    return IdomeLights

IdomeLightsDefault = (0, 0)
IdomeLightsMax = (0, 0)
if len(tests) == 0 or "3" in tests:
    IdomeLightsMin = DomeLights(0)
    IdomeLightsDefault = DomeLights(10)
    IdomeLightsMax = DomeLights(255)
    r2.DomeLightsRelay.Disable()

IdomeMotor = (0, 0)
if len(tests) == 0 or "7" in tests:
    print
    print "Measuring dome motor current (fuse 7)"
    print "-------------------------------------"
    r2.DomeMotorRelay.Enable()
    time.sleep(0.2)
    r2.Head.SetRequirePing(False)
    r2.Head.Enable()
    time.sleep(1)
    r2.Head.SetSpeed(255)
    time.sleep(1)
    IdomeMotor = MeasureCurrent()#(5, 10)
    IdomeMotor = (IdomeMotor[0] - Iidle[0], IdomeMotor[1] - Iidle[0])
    r2.Head.SetSpeed(127)
    time.sleep(1)
    r2.DomeMotorRelay.Disable()
    r2.Head.SetRequirePing(True)
    PrintPower(IdomeMotor[0], IdomeMotor[1], 7)

Isound = (0, 0)
if len(tests) == 0 or "8" in tests:
    print 
    print "Measuring amplifier current (fuse 8)"
    print "===================================="
    r2.SoundRelay.Enable()
    r2.Sound.PlayFile("startup.mp3")
    time.sleep(0.2)
    Isound = MeasureCurrent(180000)
    Isound = (Isound[0] - Iidle[0], Isound[1] - Iidle[0])
    r2.SoundRelay.Disable()
    PrintPower(Isound[0], Isound[1], 8)


print
print "Calculating total current"
print "-------------------------"
Itotal = Iidle[0] + IdomeLightsDefault[0] + IdomeMotor[0] + Isound[0]
Imax = Iidle[1] + IdomeLightsMax[1] + IdomeMotor[1] + Isound[1]
PrintPower(Itotal, Imax, -1)

sys.exit(0)
