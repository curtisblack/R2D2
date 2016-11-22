import os
import random
from pygame import mixer

class Sound:
    def __init__(self):
        self.directory = "/home/pi/Sounds"
        mixer.init()

    def PlayFile(self, file):
        mixer.music.load(file)
        mixer.music.set_volume(1)
        mixer.music.play()
        pass

    def Play(self, directory, number=None):
        d = os.path.join(self.directory, directory)
        files = sorted(os.listdir(d))
        if number == None:
            number = random.randint(0, len(files) - 1)
        self.PlayFile(os.path.join(d, files[number]))
