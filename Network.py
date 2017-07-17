import os
import time
import socket
import logging
import atexit

class Network:
    def __init__(self):
        self.IP = None
        self.lastUpdateTime = time.time()
        self.incoming = None
        self.MACs = { "b8:27:eb:fa:26:48": "BB8",
                      "b8:27:eb:c4:25:de": "R2D2",
                      "b8:27:eb:91:70:8b": "R2D2" }
        self.IPs = { "R2D2": None, "BB8": None }
        self.outgoing = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.messages = { "R2D2": [], "BB8": [] }
        self.port = 5000
        atexit.register(self.Exit)
        self.changed = []
        self.nextPing = 0
        self.pingTimes = { "R2D2": 0, "BB8": 0 }
        self.pingInterval = 1
        self.pingTimeout = 2

    def Exit(self):
        for k in self.IPs.keys():
            self.Send(k, "bye")
        self.outgoing.close()
        if self.incoming != None:
            self.incoming.close()

    def Update(self):
        t = time.time()

        if t > self.lastUpdateTime + 1:
            ip = None
            try:
                ip = os.popen("ip addr show wlan0").read().split("inet ")[1].split("/")[0]
            except IndexError:
                try:
                    ip = os.popen("ip addr show eth0").read().split("inet ")[1].split("/")[0]
                except IndexError:
                    ip = None
            if self.IP != ip:
                self.IP = ip
                if self.incoming != None:
                    self.incoming.close()
                if self.IP != None:
                    logging.info("Opening port " + str(self.port) + " on " + self.IP)
                    self.incoming = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    self.incoming.bind((self.IP, self.port))
                    broadcast = ".".join(os.popen("ifconfig | grep Bcast").read().split("Bcast:")[1].split(" ")[0].split(".")[:3] + ["0"])
                    os.popen("sudo arp-scan " + broadcast + "/24 | tail -n +3 | head -n -3 | cut -d'	' -f1 | awk '{ printf \"echo -n hi > /dev/udp/%s/" + str(self.port) + "\\n\", $1 }' | bash &")
                    #for i in range(1, 255):
                    #    self.outgoing.sendto("hi", ("192.168.0." + str(i), self.port))
                else:
                    self.incoming = None

        self.changed = []

        if self.incoming != None:
            try:
                data, (address, port) = self.incoming.recvfrom(1024, socket.MSG_DONTWAIT)
                if address != self.IP:
                    #print "IP", address
                    mac = os.popen("arp -na | grep " + address + " | cut -d' ' -f4").read().split("\n")[0]
                    #print "MAC", mac
                    if mac in self.MACs:
                        droid = self.MACs[mac]
                        logging.info("Received " + data + " from " + droid)
                        if self.IPs[droid] != address:
                            logging.info("Discovered " + droid)
                            self.IPs[droid] = address
                            self.pingTimes[droid] = time.time()
                        if data == "hi":
                            self.Send(droid, "hello")
                            self.changed.append(droid)
                        elif data == "hello":
                            self.pingTimes[droid] = time.time()
                            self.changed.append(droid)
                        elif data == "bye":
                            self.IPs[droid] = None
                            self.changed.append(droid)
                        elif data == "ping":
                            self.pingTimes[droid] = time.time()
                        else:
                            self.messages[droid].append(data)
                    else:
                        logging.info("Received " + data + " from " + address)
            except socket.error:
                pass

        t = time.time()
        if t > self.nextPing:
            self.nextPing = t + self.pingInterval
            for droid in self.IPs.keys():
               self.Send(droid, "ping")

        for droid in self.pingTimes:
            if t > self.pingTimes[droid] + self.pingTimeout and self.IPs[droid] != None:
                self.IPs[droid] = None
                self.changed.append(droid)
                logging.info("Lost " + droid)

    def Receive(self, droid):
        if len(self.messages[droid]) > 0:
            msg = self.messages[droid][0]
            del self.messages[droid][0]
            return msg
        return None

    def Send(self, droid, message):
        ip = self.IPs[droid]
        if ip != None:
            self.outgoing.sendto(message, (ip, self.port))

    def Changed(self, droid):
        return droid in self.changed

    def IsConnected(self, droid):
        return self.IPs[droid] != None
