import time
import random
from ProController import *

brightness = 15

j = ProController(0)

def PlayGeneric(pressed):
    if pressed:
        if j.R:
            r2.Sound.Play("Chatty")
        elif j.ZR:
            r2.Sound.Play("Scream")
        elif j.L:
            pass
        elif j.ZL:
            pass
        else:
            r2.Sound.Play("Generic")
j.Register('A', PlayGeneric)

def B(pressed):
    if pressed:
        if j.R:
            r2.Sound.Play("Laugh")
        elif j.ZR:
            r2.Sound.Play("Whistle")
        elif j.L:
            pass
        elif j.ZL:
            pass
        else:
            r2.Sound.Play("Happy")
j.Register('B', B)

def Y(pressed):
    if pressed:
        if j.R:
            r2.Sound.Play("Alarmed")
        elif j.ZR:
            r2.Sound.Play("Annoyed")
        elif j.L:
            pass
        elif j.ZL:
            pass
        else:
            r2.Sound.Play("Sad")
j.Register('Y', Y)

def X(pressed):
    if pressed:
        if j.R:
            r2.Sound.Play("ShortCircuit")
        elif j.ZR:
            r2.Sound.Play("Music")
        elif j.L:
            pass
        elif j.ZL:
            pass
        else:
            r2.Sound.Play("Leia")
j.Register('X', X)

def Plus(pressed):
    if pressed:
        if j.R:
            global brightness
            brightness = min(255, brightness + 15)
            r2.SetBrightness(brightness)
        else:
            r2.Sound.Volume = min(100, r2.Sound.Volume + 5)
j.Register('Plus', Plus)

def Minus(pressed):
    if pressed:
        if j.R:
            global brightness
            brightness = max(0, brightness - 15)
            r2.SetBrightness(brightness)
        else:
            r2.Sound.Volume = max(0, r2.Sound.Volume - 5)
j.Register('Minus', Minus)

def RightY(value):
    if j.R:
        r2.FrontHoloProjector.SetPositionY(value)
    if j.ZR:
        r2.RearHoloProjector.SetPositionY(value)
    if j.L:
        r2.TopHoloProjector.SetPositionY(value)
    if not (j.R or j.ZR or j.L or j.ZL):
        pass
j.Register('RightY', RightY)

def RightStick(pressed):
    if pressed:
        if j.R:
            r2.FrontHoloProjector.ToggleLight()
        if j.ZR:
            r2.RearHoloProjector.ToggleLight()
        if j.L:
            r2.TopHoloProjector.ToggleLight()
        if j.ZL:
            pass
        if not (j.R or j.ZR or j.L or j.ZL):
            r2.Head.SetPosition(0)
j.Register('RightStick', RightStick)

def RightX(value):
    if j.R:
        r2.FrontHoloProjector.SetPositionX(value)
    if j.ZR:
        r2.RearHoloProjector.SetPositionX(value)
    if j.L:
        r2.TopHoloProjector.SetPositionX(value)
    if j.ZL:
        pass
    if not (j.R or j.ZR or j.L or j.ZL):
        r2.Head.SetSpeed(value)
j.Register('RightX', RightX)


def DX(value):
    if j.R:
        if value == 1:
            print "Open Front Body Panels"
        elif value == -1:
            print "Close Front Body Panels"
    if j.ZR:
        if value == 1:
            print "Open Rear Body Panels"
        elif value == -1:
            print "Close Rear Body Panels"
    if j.L:
        pass
    if j.ZL:
        pass
    if not(j.R or j.ZR or j.L or j.ZL):
        if value == 1:
            r2.LeftUtilityArm.Open()
            r2.RightUtilityArm.Open()
        elif value == -1:
            r2.LeftUtilityArm.Close()
            r2.RightUtilityArm.Close()
j.Register('DX', DX)

def DY(value):
    if j.R:
        if value == -1:
            print "Open Periscope"
        elif value == 1:
            print "Close Periscope"
    if j.ZR:
        if value == -1:
            r2.LifeFormScanner.SetOn()
        elif value == 1:
            r2.LifeFormScanner.SetOff()
    if j.L:
        pass
    if j.ZL:
        pass
    if not (j.R or j.ZR or j.L or j.ZL):
        if value == -1:
            print "Open Dome Panels"
        elif value == 1:
            print "Close Dome Panels"
j.Register('DY', DY)

r2.DomeLightsRelay.Enable()
r2.DomeServosRelay.Enable()
r2.DomeMotorRelay.Enable()
r2.SoundRelay.Enable()
r2.BodyServosRelay.Enable()

time.sleep(1)

r2.SetBrightness(brightness)

r2.Head.Enable()

r2.LeftUtilityArm.SetTarget(0)
r2.RightUtilityArm.SetTarget(0)

while running():
    t = time.time()

    j.Update()
    
    if r2.Network.Changed("BB8"):
        if r2.Network.IsConnected("BB8"):
            r2.Sound.Play("Happy")
        else:
            r2.Sound.Play("Sad")

r2.DomeMotorRelay.Disable()
