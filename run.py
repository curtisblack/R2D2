#!/usr/bin/env python

import os
import sys
import time
import fcntl
import signal
import traceback
from R2D2 import R2D2

procs = os.popen("sudo ps ax | grep python").read().split("\n")
for proc in procs:
    if "run.py" in proc:
        pid = int(proc.lstrip(" ").split(" ")[0])
        if pid != os.getpid():
            os.system("sudo kill " + str(pid))
            time.sleep(1)
            #os.system("while ps -p " + str(pid) + "; do sleep 1; done;")

r2 = R2D2()

def handler(signal, frame):
    r2.Exit()
    sys.exit(0)

signal.signal(signal.SIGTERM, handler)

def running():
    r2.BB8.Update()
    r2.MagicPanel.Ping()
    r2.Head.Ping()
    r2.StatusDisplay.Update()
    return True

def run(script):
    exec(open(os.path.realpath(script)).read(), { "running": running, "r2": r2 })

running()

for script in sys.argv[1:]:
    run(script)

while True:
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
    r2.StatusDisplay.SetText(4, "")
    running()

