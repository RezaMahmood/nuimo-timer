#!/usr/bin/env python

from nuimo import Nuimo
from bluepy.btle import UUID, DefaultDelegate, Peripheral, BTLEException

import time

class NuimoTimerDelegate(DefaultDelegate):
    
    def __init__(self, nuimoTimer):
        DefaultDelegate.__init__(self)
        self.nuimoTimer = nuimoTimer
        
    def handleNotification(self, cHandle, data):
        if int(cHandle) == self.nuimo.characteristicValueHandles['BATTERY']:
            print('BATTERY', ord(data[0]))
            #nuimoOnkyo.battery(ord(data[0]))
        elif int(cHandle) == self.nuimo.characteristicValueHandles['FLY']:
            print('FLY', ord(data[0]), ord(data[1]))
            #nuimoOnkyo.fly(ord(data[0]), ord(data[1]))
        elif int(cHandle) == self.nuimo.characteristicValueHandles['SWIPE']:
            self.nuimoTimer.swipe(ord(data[0]))            
        elif int(cHandle) == self.nuimo.characteristicValueHandles['ROTATION']:
            value = ord(data[0]) + (ord(data[1]) << 8)
            if value >= 1 << 15:
                value = value - (1 << 16)
            self.nuimoTimer.rotate(value)
        elif int(cHandle) == self.nuimo.characteristicValueHandles['BUTTON']:
            self.nuimoTimer.button(ord(data[0]))


class NuimoTimer(Nuimo):
    def __init__(self, macAddress):
        Nuimo.__init__(self, macAddress)
        self.timer = Timer()
            
    def fly(self, flyValue):
        print(flyValue)
        
    def swipe(self, swipeValue):
        print(swipeValue)
        # Start Timer
        if swipeValue == 0:
            self.timer.Start()
        # Right
        elif swipeValue == 1:            
            return
        # Left
        elif swipeValue == 2:
            return
        # Pause Timer
        elif swipeValue == 3:
            self.timer.Pause()
        else:
            return
        
    def rotate(self, rotateValue):
        print(int(rotateValue))
        if rotateValue < 0:
            self.timer.decreaseTime(rotateValue)
        else:
            self.timer.increaseTime(rotateValue)
        
    def button(self, buttonValue):
        if buttonValue == 0:
            # check power state of Onkyo
            self.timer.display()

    def getNuimoBatteryLevel(self):
        return

if __name__ == "__main__":
    
    ######## Nuimo MAC Address #########
    nuimomac = "F6:B2:90:F2:DF:08"
    ####################################
    
    nuimoTimer = NuimoTimer()
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