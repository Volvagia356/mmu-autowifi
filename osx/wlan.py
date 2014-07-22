import objc

objc.loadBundle('CoreWLAN',
                bundle_path='/System/Library/Frameworks/CoreWLAN.framework',
                module_globals=globals())

def isSSID(ssid):
    for iname in CWInterface.interfaceNames():
        interface = CWInterface.interfaceWithName_(iname)
        if interface.ssid() == ssid:
            return True
    return False