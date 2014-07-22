from wlanconninfo import WlanConnInfo, WlanConnError

info = WlanConnInfo()

def isSSID():
    try:
        return info.isConnected(ssid)
    except WlanConnError:
        return False
