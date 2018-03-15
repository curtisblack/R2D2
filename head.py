import time
import random

r2.DomeMotorRelay.Enable()

time.sleep(1)

r2.Head.SetRequirePing(False)
r2.Head.Enable()
r2.Head.SetPosition(0)

nextHeadMove = time.time() + 10
left = False

while running():
    t = time.time()
    
    if t > nextHeadMove:
        nextHeadMove = t + 10
        r2.Head.SetPosition(-90 if left else 90)
        left = not left

r2.Head.SetRequirePing(True)
r2.DomeMotorRelay.Disable()
