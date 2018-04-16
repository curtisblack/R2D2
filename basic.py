import time
import random

r2.DomeLightsRelay.Enable()
r2.DomeMotorRelay.Enable()
if not "-mute" in args:
    r2.SoundRelay.Enable()
r2.BodyServosRelay.Enable()

time.sleep(1)

r2.Head.Enable()
r2.Head.SetPosition(0)

r2.LeftUtilityArm.SetTarget(0)
r2.RightUtilityArm.SetTarget(0)

nextHeadMove = time.time() + 10
nextSound = time.time()
nextHologram = time.time()
hologramOff = time.time() + 1e6

class HeadMove:
    def __init__(self, head):
        self.Head = head
        self.NextMoveTime = 0

    def Update(self):
        t = time.time()
        if t > self.NextMoveTime:
            self.Head.SetPosition(random.randint(-90, 90))
            self.NextMoveTime = t + random.randint(1, 10)

scripts = []

scripts.append(HeadMove(r2.Head))

from HoloProjector import *
scripts.append(TwitchHoloProjector(r2.FrontHoloProjector))
scripts.append(TwitchHoloProjector(r2.TopHoloProjector))
scripts.append(TwitchHoloProjector(r2.RearHoloProjector))

while running():
    t = time.time()

    for script in scripts:
        script.Update()

    if t > nextHologram:
        nextHologram = t + random.randint(60, 180)
        hologramOff = t + 30
        r2.FrontHoloProjector.SetMessage()
        #r2.Sound.Play("")
    elif t > hologramOff:
        r2.FrontHoloProjector.SetDefault()
        hologramOff = t + 1e6
    
    if t > nextSound:
        nextSound = t + random.randint(10, 20)
        r2.Sound.Play("Generic")
    
    if r2.Network.Changed("BB8"):
        if r2.Network.IsConnected("BB8"):
            r2.Sound.Play("Happy")
        else:
            r2.Sound.Play("Sad")

r2.DomeMotorRelay.Disable()
