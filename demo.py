import time
from R2D2 import *
from DualShock import *

r2 = R2D2()
r2.DomeLights.Enable()
r2.DomeServos.Enable()
r2.BodyLights.Enable()
r2.BodyServos.Enable()

controller = DualShock()

def PlayGeneric(pressed):
    if pressed:
        r2.Sound.Play("Generic")
controller.events["R1"].append(PlayGeneric) 

def PlayWhistle(pressed):
    if pressed:
        r2.Sound.Play("Whistle")
controller.events["L1"].append(PlayWhistle)

#time.sleep(100)

#r2.Head.Motor.Enable()
r2.Head.MagicPanel.SetBrightness(50)

while True:
    controller.update()
    if controller.cross:
        print "ENABLE"
        r2.Head.Motor.Enable()
    if controller.circle:
        print "DISABLE"
        r2.Head.Motor.Disable()
    if controller.square:
        r2.DomeLights.Enable()
        r2.DomeServos.Enable()
        r2.BodyLights.Enable()
        r2.BodyServos.Enable()
    if controller.triangle:
        r2.DomeLights.Disable()
        r2.DomeServos.Disable()
        r2.BodyLights.Disable()
        r2.BodyServos.Disable()
    if controller.start:
        break
    x = controller.Rx
    x *= abs(x)
    speed = int(127 + 127 * x)
    r2.Head.Motor.SetSpeed(speed)
    r2.Head.Motor.Ping()
    if r2.DomeLights.Enabled:
        if r2.Head.Motor.Enabled:
            r2.Head.MagicPanel.SetDefault()
            #r2.Head.SetDefault()
        else:
            r2.Head.MagicPanel.SetOn()
            #r2.Head.SetError()
    r2.StatusDisplay.Update()
    time.sleep(1.0 / 30.0)
