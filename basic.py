import time
import random
from R2D2 import *

r2 = R2D2()
r2.DomeLightsRelay.Enable()
r2.DomeMotorRelay.Enable()

time.sleep(1)

r2.Head.Enable()
r2.Head.SetPosition(0)

r2.Sound.Volume = 100

nextHeadMove = time.time() + 10
nextSound = time.time()

brightness = -2

lastPing = time.time()

while running():
    t = time.time()
    
    if t > lastPing + 0.5:
        lastPing = t
        r2.MagicPanel.Ping()
    
    if t > nextHeadMove:
        nextHeadMove = t + random.randint(1, 10)
        r2.Head.SetPosition(random.randint(-90, 90))
    
    if t > nextSound:
        nextSound = t + random.randint(10, 20)
        r2.Sound.Play("Generic")
    
    b = int(255 * r2.BrightnessControl.GetValue())
    if abs(brightness - b) > 2:
        brightness = b
        r2.SetBrightness(brightness)
    
    r2.BB8.Update()
    if r2.BB8.JustConnected:
        r2.Sound.Play("Happy")
    elif r2.BB8.JustDisconnected:
        r2.Sound.Play("Sad")
    r2.StatusDisplay.Update()
