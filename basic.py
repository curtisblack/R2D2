import time
import random

#r2.StatusDisplay.SetText(4, "Demo Script")

r2.DomeLightsRelay.Enable()
r2.DomeMotorRelay.Enable()

time.sleep(1)

r2.Head.Enable()
r2.Head.SetPosition(0)

r2.Sound.Volume = 50

nextHeadMove = time.time() + 10
nextSound = time.time()

brightness = -2

while running():
    t = time.time()
    
    if t > nextHeadMove:
        nextHeadMove = t + random.randint(1, 10)
        r2.Head.SetPosition(random.randint(-90, 90))
    
    if t > nextSound:
        nextSound = t + random.randint(10, 20)
        r2.Sound.Play("Generic")
    
    b = int(round(255 * r2.BrightnessControl.GetValue()))
    if brightness != b:
        brightness = b
        r2.SetBrightness(brightness)
    
    if r2.Network.Changed("BB8"):
        if r2.Network.IsConnected("BB8"):
            r2.Sound.Play("Happy")
        else:
            r2.Sound.Play("Sad")

r2.DomeMotorRelay.Disable()
