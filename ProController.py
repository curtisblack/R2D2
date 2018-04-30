import os, struct, array, atexit
from fcntl import ioctl
from multiprocessing import Process, Queue

VENDOR = 0x057E
PRODUCT = 0x2009

class ProController:
    def __init__(self, id=0):
        self.Connected = False
        self.axis_states = {}
        self.button_states = {}
        self.events = {}

        self.axis_names = {
            0x00: 'LeftX',
            0x01: 'LeftY',
            0x03: 'RightX',
            0x04: 'RightY',
            0x10: 'DX',
            0x11: 'DY',
        }

        for axis in self.axis_names.values():
            setattr(self, axis, 0.0)
            self.events[axis] = []
            self.axis_states[axis] = 0.0

        self.button_names = {
            0x130: 'B',
            0x131: 'A',
            0x132: 'Y',
            0x133: 'X',
            0x134: 'L',
            0x135: 'R',
            0x136: 'ZL',
            0x137: 'ZR',
            0x138: 'Minus',
            0x139: 'Plus',
            0x13A: 'LeftStick',
            0x13B: 'RightStick',
            0x13C: 'Home',
            0x13D: 'Capture',
            0x13E: 'Unknown1',
            0x13F: 'Unknown2'
        }

        for button in self.button_names.values():
            setattr(self, button, False)
            self.events[button] = []
            self.button_states[button] = False

        self.axis_map = []
        self.button_map = []

        self.fn = '/dev/input/js' + str(id)
        self.jsdev = None

        self.queue = Queue()
        self.process = Process(target=self.Run, args=(self.queue,))
        self.process.start()
        atexit.register(self.Quit)

    def begin(self):
        if not os.path.exists(self.fn):
            return

        self.jsdev = open(self.fn, 'rb')

        buf = array.array('c', ['\0'] * 64)
        ioctl(self.jsdev, 0x80006A13 + (0x10000 * len(buf)), buf) # JSIOCGNAME(len)
        self.js_name = buf.tostring()

        buf = array.array('B', [0])
        ioctl(self.jsdev, 0x80016A11, buf) # JSIOCGAXES
        self.num_axes = buf[0]

        buf = array.array('B', [0])
        ioctl(self.jsdev, 0x80016A12, buf) # JSIOCGBUTTONS
        self.num_buttons = buf[0]

        buf = array.array('B', [0] * 0x40)
        ioctl(self.jsdev, 0x80406A32, buf) # JSIOCGAXMAP

        for axis in buf[:self.num_axes]:
            axis_name = self.axis_names.get(axis, 'unknown(0x%02x)' % axis)
            self.axis_map.append(axis_name)
            #self.axis_states[axis_name] = 0.0

        buf = array.array('H', [0] * 200)
        ioctl(self.jsdev, 0x80406A34, buf) # JSIOCGBTNMAP

        for btn in buf[:self.num_buttons]:
            btn_name = self.button_names.get(btn, 'unknown(0x%03x)' % btn)
            self.button_map.append(btn_name)
            #self.button_states[btn_name] = 0

        #self.queue = Queue()
        #self.process = Process(target=self.Run, args=(self.queue,))
        #self.process.start()
        #atexit.register(self.Quit)

    def Quit(self):
        self.process.terminate()

    def Run(self, queue):
        while True:
            try:
                if self.jsdev == None:
                    self.begin()
                if self.jsdev == None:
                    continue
                evbuf = self.jsdev.read(8)
                if evbuf:
                    time, value, type, number = struct.unpack('IhBB', evbuf)
                    initial = type & 0x80
                    if initial:
                        queue.put(True)
                    if type & 0x01:
                        queue.put((time, value, type, self.button_map[number]))
                    elif type & 0x02:
                        queue.put((time, value, type, self.axis_map[number]))
            except:
                queue.put(False)
                self.jsdev = None

    def Register(self, button, function):
        self.events[button].append(function)

    def Update(self):
        while self.queue.qsize() > 0:
            values = self.queue.get()
            if isinstance(values, bool):
                self.Connected = values
                continue
            time, value, type, number = values
            if type & 0x01:
                button = number#self.button_map[number]
                if button:
                    bvalue = True if value else False
                    self.button_states[button] = bvalue
                    setattr(self, button, bvalue)
                    for e in self.events[button]:
                        e(bvalue)

            elif type & 0x02:
                axis = number#self.axis_map[number]
                if axis:
                    fvalue = value / 32767.0
                    fvalue = fvalue / 0.8
                    if fvalue > 1.0: fvalue = 1.0
                    if fvalue < -1.0: fvalue = -1.0
                    self.axis_states[axis] = fvalue
                    setattr(self, axis, fvalue)
                    for e in self.events[axis]:
                        e(fvalue)
            else:#if type & 0x80:
                print time, value, type, number

if __name__ == "__main__":
    p = ProController(0)
    while True:
        p.Update()
        print p.Connected, p.A, p.Unknown1, p.Unknown2
