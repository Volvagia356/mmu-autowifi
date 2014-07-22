import requests
import json
from threading import Event
from sys import exc_info
from linux import wlan
from linux import conf

config = {'username': '', 'password': ''}

def xor(x):
    return b"".join([chr(ord(x[n])^ord(b"\x52\x49\x4E"[n%3])) for n in range(len(x))])

def load_config():
    global config
    try:
        config = json.loads(xor(open(conf.filename,'rb').read()))
    except (IOError, ValueError):
        pass

def write_config():
    open(conf.filename, 'wb').write(xor(json.dumps(config, separators=(',',':'))))

def is_logged_in():
    resp = requests.get("http://www.mmu.edu.my/", allow_redirects=False, timeout=5)
    if resp.headers['server'] == "HTTP Appgw": return False
    else: return True

def log_in():
    form = {
        'username': config['username'],
        'password': config['password'],
        'buttonClicked': "4",
    }
    resp = requests.post("https://wifi.mmu.edu.my/login.html", data=form, verify="cabundle", timeout=5)
    if "Login Successful" in resp.content: return
    elif "You are already logged in." in resp.content: return
    elif "The User Name and Password combination you have entered is invalid." in resp.content: raise LoginError("Incorrect login details!")
    else: raise LoginError("Unknown error, unable to login!")

class LoginError(Exception):
    def __init__(self, message):
        self.message = message

class SaveRetryException(Exception):
    pass

def main_loop(app):
    while True:
        try:
            if config['username'] == '' or config['password'] == '':
                app.queue.put("Enter username/password!")
                app.retry_event.wait()
                raise SaveRetryException()
            if wlan.isSSID("MMU"):
                app.queue.put("Connected to MMU access point")
                if app.retry_event.wait(2): raise SaveRetryException()
                app.queue.put("Checking status...")
                if not is_logged_in():
                    app.queue.put("Logging in...")
                    try:
                        log_in()
                    except requests.exceptions.SSLError:
                        app.queue.put("HTTPS certificate error!")
                    except LoginError as e:
                        app.queue.put(e.message)
                else:
                    app.queue.put("Logged in")
                    if app.retry_event.wait(59): raise SaveRetryException()
            else:
                app.queue.put("Not connected to MMU access point")
            if app.retry_event.wait(1): raise SaveRetryException()
        except SaveRetryException:
            app.retry_event.clear()
            config['username'] = app.username_input.get()
            config['password'] = app.password_input.get()
            write_config()
            app.queue.put("savecomplete")
        except requests.exceptions.RequestException:
            app.queue.put("Connection Error!")
            app.retry_event.wait(2)
        except:
            app.queue.put(("exception",exc_info()))
            raise
