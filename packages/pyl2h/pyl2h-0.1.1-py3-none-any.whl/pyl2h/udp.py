import socket
import copy

class UDPServer:
    def __init__(self) -> None:
        self.devices = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(("", 35932))

    def decodeStatusBroadcast(self, data, ip, dev):
        mac = data[2:8]
        channel = data[len(data)-2]
        is_on = False if data[len(data)-1] is 0 else True

        dev["mac"] = mac
        dev["channels"][channel] = is_on
        dev["ip"] = ip

        return dev

    def processMessage(self, data, address):
        ip = address[0]
        oldState = self.devices[ip] if ip in self.devices else {"channels": {}}
        newState = self.decodeStatusBroadcast(data, ip, copy.deepcopy(oldState))

        if oldState == newState:
            return None

        self.devices[ip] = newState
        return newState

    def sendMessage(self, ip, message):
        self.sock.sendto(message, (ip, 35932))

    def setStatus(self, ip, channel: int, state):
        stateByte = b'\xff' if state else b'\x00'
        channelByte = bytes([channel])
        device = self.devices[ip]
        mac = device["mac"]
        message = b'\xa1\x04'+mac+b'\x00\x09\x01\xf2\x02\xd1\x71\x50\x01'+channelByte+stateByte
        self.sendMessage(ip, message)

    def getDevices(self):
        return self.devices

    def listen(self, subscriber=None):
        while True:
            data, addr = self.sock.recvfrom(1024)
            deviceStatus = self.processMessage(data, addr)
            if deviceStatus is not None and subscriber is not None:
                subscriber(deviceStatus)