from tkinter import *
from tkinter import messagebox
import localsettings
import sys

# This pop-up window is used for the client server configuration of the client

class ConfigLocal():
    
    # Track whether config window open to stop duplicate windows
    configWindowOpen = False

    def __init__ (self, config, configfile, settings, defaults, command):
        self.config = config
        self.configfile = configfile
        self.settings = settings
        self.defaults = defaults
        self.command = command              # Used to update current ClientController


    # called from window manager handler or from Cancel button
    def closeConfig(self):
        self.configWindowOpen = False
        self.configTop.destroy()
        
    def restoreDefaults(self): 
        self.hostnameString.set(self.defaults['hostname'])
        self.portString.set(self.defaults['port'])
        if (bool(self.defaults['ssl'])):
            self.sslVar.set(1)
        else :
            self.sslVar.set(0)
        

    def saveConfig(self):
        # Check for valid entries - if not restore previous value and give error message
        if (self._validateHostname(self.hostnameString.get(), "Hostname ")):
            self.config['Server']['hostname'] = self.hostnameString.get()
        else :
            # Restore previous value
            self.hostnameString.set(self.config['Server']['hostname'])
            return        
        if (self._validateNumber(self.portString.get(), 0, 65535, "Port number ")):
            self.config['Server']['port'] = self.portString.get()
        else :
            # Restore previous value
            self.portString.set(self.config['Server']['port'])
            return  
        if (self.sslVar.get() == 1):
            self.config['Server']['ssl'] = "True"
        else:
            self.config['Server']['ssl'] = "False"

        # Save config
        try:
            with open(self.configfile, 'w') as cfgfile:
                self.config.write(cfgfile)
                self.closeConfig()
                # Change server info dynamically
                self.command.chgServer (self.config['Server']['hostname'], self.config['Server']['port'], self.config['Server']['ssl']) 
                messagebox.showinfo("Info", "Configuration saved.")
        except : 
            self.closeConfig()
            messagebox.showinfo("Error", "Error saving configuration file "+configfile)
            
        
    def windowClient (self):
        if (self.configWindowOpen) :
            return
                   
        self.configWindowOpen = True
        self.configTop = Toplevel()
        self.configTop.wm_title("Local Configuration")
        self.configTop.wm_geometry("450x300")
        # set handler for close window using WM X
        self.configTop.wm_protocol('WM_DELETE_WINDOW',  self.closeConfig)

        
        self.hostnameString = StringVar()
        self.hostnameString.set(self.config['Server']['hostname'])
        self.portString = StringVar()
        self.portString.set(int(self.config['Server']['port']))
        self.sslVar = IntVar()
        if (self.config['Server']['ssl'] == 'True'):
            self.sslVar.set(1)
        else:
            self.sslVar.set(0)
        
        configTitleLabel = Label(self.configTop,
                text="NeoPixel - Local Configuration",
                foreground="blue", font="Verdana 16 bold").grid(columnspan=4, sticky=W, pady=(4, 15), padx=5)
                
        hostnameLabel = Label(self.configTop,
                    font="Verdana 14",
                    text="Hostname").grid(row=1, column=1, columnspan=1, sticky=W, padx=(15,2))
                    
        hostnameEntry = Entry(self.configTop,
                    font="Verdana 14",
                    width=15,
                    textvariable=self.hostnameString).grid(row=1, column=2, columnspan=2, sticky=W)
                    
        portLabel = Label(self.configTop,
                    font="Verdana 14",
                    text="Port").grid(row=2, column=1, columnspan=1, sticky=W, padx=(15,2))
                    
        portEntry = Entry(self.configTop,
                    font="Verdana 14",
                    width=5,
                    textvariable=self.portString).grid(row=2, column=2, sticky=W)
                    
        sslLabel = Label(self.configTop,
                    font="Verdana 14",
                    text="SSL").grid(row=3, column=1, columnspan=1, sticky=W, padx=(15,2))


        sslCheckBox = Checkbutton(self.configTop,
                    font="Verdana 14",
                    variable=self.sslVar).grid(row=3, column=2, sticky=W)

        buttonRow = 6

        restoreButton = Button(self.configTop, 
                    text="Restore\ndefaults",
                    font="Verdana 9",
                    width = 8,
                    height = 2,
                    command=self.restoreDefaults)
        restoreButton.grid(row=buttonRow, column=1, pady=(40, 10), padx=5)


        cancelButton = Button(self.configTop, 
                    text="Cancel",
                    font="Verdana 14",
                    width = 8,
                    height = 1,
                    command=self.closeConfig)
        cancelButton.grid(row=buttonRow, column=2, pady=(40, 10), padx=5)
    
    
        saveButton = Button(self.configTop, 
                    text="Save",
                    font="Verdana 14",
                    width = 8,
                    height = 1,
                    command=self.saveConfig)
        saveButton.grid(row=buttonRow, column=3, pady=(40, 10), padx=5)
        
    
    # return true if a valid integer - otherwise false
    # error message is issued based on errormsg and whether it's greater than min / max
    # if no min / max required then set to suitably huge values
    # eg 1000000 is a huge number of LEDs to try and control using a single PWM channel
    def _validateNumber (self, string, min, max, errormsg):
        try:
            testval = int(string)
        except (TypeError, ValueError):
            messagebox.showinfo("Warning", errormsg + "is not a number.\nSee User Guide for more details.", parent=self.configTop)
            return False
        if (testval < min):
            messagebox.showinfo("Warning", errormsg + "is below the minimum value.\nSee User Guide for more details.", parent=self.configTop)
            return False
        if (testval > max):
            messagebox.showinfo("Warning", errormsg + "is above the maximum value.\nSee User Guide for more details.", parent=self.configTop)
            return False
        return True
        
        
        
    # Warning this is for user of a local hostname and has no checking
    # at the moment, provided as a stub if further checking required in 
    # future (eg. to pass hostname to server)
    def _validateHostname (self, string, errormsg):
        return True