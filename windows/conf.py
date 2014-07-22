import os

directory = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/AppData/Roaming/MMU-AutoWifi"))

if not os.path.exists(directory):
    os.makedirs(directory)

filename = directory + "/config.json"
