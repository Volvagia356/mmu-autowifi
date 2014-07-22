from wlanconninfo import WlanConnInfo, WlanConnError

info = WlanConnInfo()

def isSSID(ssid):
    try:
        return info.isConnected(ssid)
    except WlanConnError:
        return False
