import os
import random
from pygame import mixer

class Sound(object):
    def __init__(self):
        self.directory = "/home/pi/R2D2/Sounds"
        self.device = "PCM"
        mixer.init()
        self.Volume = 3

    #@property
    def get_Volume(self):
        try:
            return int(os.popen("amixer sget " + self.device).read().split("[")[1].split("%")[0])
        except IndexError:
            return 0

    #@Volume.setter
    def set_Volume(self, value):
        volume = max(0, min(100, value))
        os.system("amixer set " + self.device + " " + str(volume) + "% > /dev/null")

    Volume = property(get_Volume, set_Volume)

    def Mute(self):
        os.system("amixer set " + self.device + " mute > /dev/null")

    def Unmute(self):
        os.system("amixer set " + self.device + " unmute > /dev/null")

    def IsMute(self):
        return "[off]" in os.popen("amixer sget " + self.device).read()

    def PlayFile(self, file):
        if not os.path.isabs(file):
            file = os.path.join(self.directory, file)
        mixer.music.load(file)
        mixer.music.set_volume(0.1)
        mixer.music.play()
        pass

    def Play(self, directory, number=None):
        d = os.path.join(self.directory, directory)
        files = sorted(os.listdir(d))
        if number == None:
            number = random.randint(0, len(files) - 1)
        self.PlayFile(os.path.join(d, files[number]))
