import os
import sys
import time
import signal
import traceback
from R2D2 import R2D2

def handler(signal, frame):
    sys.exit(0)

signal.signal(signal.SIGTERM, handler)

pipe_path = "/home/pi/r2"
if not os.path.exists(pipe_path):
    os.mkfifo(pipe_path)

pipe_fd = os.open(pipe_path, os.O_RDONLY | os.O_NONBLOCK)
pipe = os.fdopen(pipe_fd)

r2 = R2D2()

def running():
    r2.StatusDisplay.Update()
    message = pipe.read()
    if message:
        message = message.rstrip("\n")
        if message == "stop":
            return False
        else:
            exec(message, { "running": running, "r2": r2 })
    return True

try:
    exec(open("/home/pi/R2D2/basic.py").read(), { "running": running, "r2": r2 })
except Exception as e:
    f = open("crash.log", "a")
    f.write(traceback.format_exc())
    f.write("\n")
    f.close()

