import time

try:
    exec(open("/home/pi/R2D2/demo.py").read(), globals())
except Exception as e:
    while True:
        print e
        time.sleep(1)
# Turn on the power indicator light

#from RPi.GPIO import *
#from LED import *

#setmode(BCM)
#l = LED(23)
#l.On()
#import time
#from R2D2 import *

#r2 = R2D2()
#r2.Head.FrontProcessStateIndicator.SetBrightness(2)

#while True:
#    time.sleep(0.1)
