import os
import sys
import time
import signal
import traceback

def handler(signal, frame):
    sys.exit(0)

signal.signal(signal.SIGTERM, handler)

pipe_path = "/home/pi/r2"
if not os.path.exists(pipe_path):
    os.mkfifo(pipe_path)

pipe_fd = os.open(pipe_path, os.O_RDONLY | os.O_NONBLOCK)
pipe = os.fdopen(pipe_fd)

def running():
    message = pipe.read()
    if message:
        message = message.rstrip("\n")
        if message == "stop":
            return False
    return True

try:
    exec(open("/home/pi/R2D2/basic.py").read(), globals())
except Exception as e:
    f = open("crash.log", "a")
    f.write(traceback.format_exc())
    f.write("\n")
    f.close()

