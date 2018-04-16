#!/usr/bin/env python

import os
import sys
import time
import fcntl
import signal
import pygame
import traceback
from R2D2 import R2D2

def KillCurrent():
    procs = os.popen("sudo ps ax | grep python").read().split("\n")
    for proc in procs:
        if "run.py" in proc:
            pid = int(proc.lstrip(" ").split(" ")[0])
            if pid != os.getpid():
                os.system("sudo kill " + str(pid))
                time.sleep(1)

r2 = R2D2()

def handler(signal, frame):
    r2.Exit()
    sys.exit(0)

signal.signal(signal.SIGTERM, handler)

lastUpdate = 0

def running():
    t = time.time()
    global lastUpdate
    if t - lastUpdate > 0.1:
        r2.Network.Update()
        r2.MagicPanel.Ping()
        r2.Head.Ping()
        r2.StatusDisplay.Update()
        r2.BodyServos.Update()
        lastUpdate = t
    return True

def run(script):
    exec(open(os.path.realpath(script)).read(), { "running": running, "r2": r2, "args": sys.argv[2:] })

running()

if len(sys.argv) > 1:
    run(sys.argv[1])
#for script in sys.argv[1:]:
#    run(script)

r2.Relay1.Disable()
r2.Relay2.Disable()
r2.Relay3.Disable()
r2.Relay4.Disable()
r2.Relay5.Disable()
r2.Relay6.Disable()
r2.Relay7.Disable()
r2.Relay8.Disable()
r2.Relay9.Disable()
r2.Relay10.Disable()
r2.Relay11.Disable()
r2.Relay12.Disable()

clock = pygame.time.Clock()
while running():
    clock.tick(50)
