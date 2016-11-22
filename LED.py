from RPi.GPIO import *

class LED:
    def __init__(self, pin):
        self.pin = pin
        setup(self.pin, OUT)
        self.pwm = PWM(self.pin, 1000)
        self.pwm.start(0)

    def On(self):
        self.pwm.ChangeDutyCycle(100)
        #output(self.pin, True)

    def Off(self):
        self.pwm.ChangeDutyCycle(0)
        #output(self.pin, False)

    def SetBrightness(self, brightness):
        self.pwm.ChangeDutyCycle(100 * brightness / 255)
