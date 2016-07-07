#!/usr/bin/env python

from nuimo import Nuimo
from bluepy.btle import UUID, DefaultDelegate, Peripheral, BTLEException
from display import Display, ValidFonts


import time

class NuimoTimerDelegate(DefaultDelegate):
    
    def __init__(self, nuimoTimer):
        DefaultDelegate.__init__(self)
        self.nuimoTimer = nuimoTimer
        
    def handleNotification(self, cHandle, data):
        if int(cHandle) == self.nuimoTimer.characteristicValueHandles['BATTERY']:
            print('BATTERY', ord(data[0]))
            #nuimoOnkyo.battery(ord(data[0]))
        elif int(cHandle) == self.nuimoTimer.characteristicValueHandles['FLY']:
            print('FLY', ord(data[0]), ord(data[1]))
            #nuimoOnkyo.fly(ord(data[0]), ord(data[1]))
        elif int(cHandle) == self.nuimoTimer.characteristicValueHandles['SWIPE']:
            self.nuimoTimer.swipe(ord(data[0]))            
        elif int(cHandle) == self.nuimoTimer.characteristicValueHandles['ROTATION']:
            value = ord(data[0]) + (ord(data[1]) << 8)
            if value >= 1 << 15:
                value = value - (1 << 16)
            self.nuimoTimer.rotate(value)
        elif int(cHandle) == self.nuimoTimer.characteristicValueHandles['BUTTON']:
            self.nuimoTimer.button(ord(data[0]))


class NuimoTimer(Nuimo):
    def __init__(self, macAddress):
        Nuimo.__init__(self, macAddress)        
        self.display = Display()
        self.font = ValidFonts()
        self.timerValue = 0
            
    def fly(self, flyValue):
        print(flyValue)
        
    def swipe(self, swipeValue):
        print(swipeValue)
        # Left
        if swipeValue == 0:
            #self.timer.Start()
            self.displayLedMatrix(self.display.singleChar("2", "clb8x8"), 1.0)
            
        # Right
        elif swipeValue == 1:            
            self.displayLedMatrix(self.display.singleChar("1", "clb8x8"), 1.0)
        # Up
        elif swipeValue == 2:
            self.displayLedMatrix(self.display.icon("start"), 1.0)
        # Pause Timer
        elif swipeValue == 3:
            #self.timer.Pause()
            self.displayLedMatrix(self.display.icon("pause"), 1.0)
        else:
            pass
        
    def rotate(self, rotateValue):
        print(int(rotateValue))
        if rotateValue < 0:
            if self.timerValue <= 0:
                self.timerValue = 0               
            else:
                self.timerValue = self.timerValue-1                
        else:
            self.timerValue = self.timerValue + 1

        self.displayTimer()
                    
    
    def displayTimer(self):
        if self.timerValue <= 9:                
            self.displayLedMatrix(self.display.singleChar(str(self.timerValue),"clb8x8"),0.5)
        else:
            self.displayLedMatrix(self.display.icon(str(self.timerValue)),0.5)
             
                    
    def button(self, buttonValue):
        if buttonValue == 0:
            #self.selfTestFont()
            self.displayLedMatrix(self.display.icon("88"), 1.0)

    def selfTestFont(self):        
        chars = ["99","88","1","2","3","4","5","6","7","8","9","0","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        for x in range(0, len(chars)):
            self.displayLedMatrix(self.display.singleChar(chars[x], "clb8x8"), 0.5)
            print(chars[x])
            time.sleep(0.75)
            

    def getNuimoBatteryLevel(self):
        pass

if __name__ == "__main__":
    
    ######## Nuimo MAC Address #########
    nuimomac = "F6:B2:90:F2:DF:08"
    ####################################
    
    nuimoTimer = NuimoTimer(nuimomac)
    nuimoTimer.set_delegate(NuimoTimerDelegate(nuimoTimer))
    
    print("Trying to connect to %s.  Press Ctrl+C to cancel." % nuimomac)
    try:
        nuimoTimer.connect()
    except BTLEException as e:
        print("Bluetooth exception occurred:", str(e))
        sys.exit()
    print("Connected. Waiting for input events...")
    
    # Display some LEDs matrices and wait for notifications
    nuimoTimer.displayLedMatrix("          ***      *  *     *  * *   ***      *    *   *    *   *    *           ", 2.0)
    time.sleep(2)    

    try:
        while True:
            nuimoTimer.waitForNotifications()
    except BTLEException as e:
        print("Connection error:", str(e))
    except KeyboardInterrupt:
        print("Program aborted")