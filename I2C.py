import smbus
import logging
import traceback
import inspect

class I2C:
    def __init__(self, address, relay=None):
        self.address = address
        self.relay = relay
        self.i2c = smbus.SMBus(1)

    def Send(self, command, data = []):
        if self.relay != None and not self.relay.Enabled:
            return
        packet = [command, len(data)] + data
        crc = self.CRC(packet)
        bytes = [len(data)] + data + [crc]
        attempts = 3
        for i in range(attempts):
            try:
                self.i2c.write_i2c_block_data(self.address, command, bytes)
                break
            except IOError:
                if i == attempts - 1:
                    caller = inspect.stack()[1]
                    if "HoloProjector" not in caller[1]:
                        logging.warning(caller[1] + " " + caller[3] + "\n" + traceback.format_exc())

    def CRC(self, data):
        crc = 0x00
        for d in data:
            for i in range(8):
                sum = (crc ^ d) & 0x01
                crc >>= 1
                if sum:
                    crc ^= 0x8C
                d >>= 1
        return crc

