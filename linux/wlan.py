import os
import array
import fcntl
import socket
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
maxLength = {
    "interface": 16,
    "essid": 32
}
calls = {
    "SIOCGIWESSID": 0x8B1B
}

def getESSID(interface):
    """Return the ESSID for an interface, or None if we aren't connected."""
    essid = array.array("c", "\0" * maxLength["essid"])
    essidPointer, essidLength = essid.buffer_info()
    request = array.array("c",
        interface.ljust(maxLength["interface"], "\0") +
        struct.pack("PHH", essidPointer, essidLength, 0)
    )
    fcntl.ioctl(sock.fileno(), calls["SIOCGIWESSID"], request)
    name = essid.tostring().rstrip("\0")
    if name:
        return name
    return None 

def isSSID(ssid):
    interfaces = os.listdir("/sys/class/net")
    for interface in interfaces:
        try:
            if getESSID(interface)==ssid: return True
        except IOError:
            pass
    return False