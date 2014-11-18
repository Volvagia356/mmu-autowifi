#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mmu_autowifi
import threading
import Tkinter
from tkMessageBox import showerror, showinfo
from Queue import Queue
from sys import exit, exc_info
from traceback import format_exception
from logo import logo


class App(Tkinter.Frame):
    def __init__(self, master=None):
        Tkinter.Frame.__init__(self, master)
        self.tklogo = Tkinter.PhotoImage(data=logo)
        master.tk.call("wm", "iconphoto", master._w, self.tklogo)
        master.title("MMU AutoWiFi")
        master.resizable(0, 0)
        self['padx'] = 10
        self['pady'] = 10
        self.pack()
        
        #Widgets
        self.menubar = Tkinter.Menu(self)
        self.menubar.add_command(label="About", command=self.about)
        self.username_label = Tkinter.Label(self, text="Username:")
        self.username_input = Tkinter.Entry(self, width=30)
        self.password_label = Tkinter.Label(self, text="Password:")
        self.password_input = Tkinter.Entry(self, width=30, show='*')
        self.save_button = Tkinter.Button(self, text="Save and re-login")
        self.status_label = Tkinter.Label(self)
        
        #Positioning
        self.master.config(menu=self.menubar)
        self.username_label.grid(row=0, column=0, sticky=Tkinter.W)
        self.username_input.grid(row=0, column=1)
        self.password_label.grid(row=1, column=0, sticky=Tkinter.W)
        self.password_input.grid(row=1, column=1)
        self.save_button.grid(row=3, columnspan=2)
        self.status_label.grid(row=4, columnspan=2, sticky=Tkinter.W)
        
        #Commands
        self.save_button['command'] = self.save_config
        
        #Initialize some GUI values
        self.username_input.insert(0, mmu_autowifi.config['username'])
        self.password_input.insert(0, mmu_autowifi.config['password'])
        self.set_status("Initializing...")
        
        #Program init
        self.queue = Queue()
        self.retry_event = threading.Event()
        self.save_lock = threading.Lock()
        self.thread = threading.Thread(target=mmu_autowifi.main_loop, args=(self,))
        self.thread.daemon = True
        self.thread.start()
    
    def about(self):
        showinfo("About", "© 2014 Volvagia356\n\
Version 1.0.0\n\
A community project for Hackerspace MMU\n\
\n\
Logo designed by eXodes\n\
\n\
http://mmuwifi.volzel.net/")
    
    def save_config(self):
        self.set_status("Saving...")
        self.username_input['state'] = 'disabled'
        self.password_input['state'] = 'disabled'
        self.save_button['state'] = 'disabled'
        self.retry_event.set()
    
    def set_status(self, status):
        self.status_label['text'] = "Status: %s" % status
    
    def eventloop(self):
        while not self.queue.empty():
            event = self.queue.get(False)
            if event == "savecomplete":
                self.set_status("Saved. Retrying...")
                self.username_input['state'] = 'normal'
                self.password_input['state'] = 'normal'
                self.save_button['state'] = 'normal'
            elif event[0] == "exception":
                showerror("Unexpected Exception", "An unexpected exception has occured.\n\
Please file a bug report.\n\
The application will now close.\n\n"+
"".join(format_exception(*event[1])))
                exit()
            else:
                self.set_status(event)
        self.after(100, self.eventloop)

mmu_autowifi.load_config()
root = Tkinter.Tk()
app = App(master=root)

app.eventloop()
showinfo("Notice", "This software may stop working on the 16th of December, 2014 due to a change regarding the security of the WiFi network.\n\
Please check for updates on the website when this occurs.")
app.mainloop()
