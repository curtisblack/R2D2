
class WiFiSerial:
    def __init__(self, *addresses):
        self.addresses = addresses

class BB8WiFiSerial(WiFiSerial):
    def __init__(self):
        WiFiSerial.__init__(self, "b8:27:eb:fa:26:48")

class R2D2WiFiSerial(WiFiSerial):
    def __init__(self):
        WiFiSerial.__init__(self, "b8:27:eb:c4:25:de", "b8:27:eb:91:70:8b")
