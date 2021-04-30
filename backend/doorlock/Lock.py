from time import time

class Lock:
    def __init__(self, dryRun):
        self.openFlag = False
        self.closeTimestamp = time()

    def isOpen(self):
        return self.openFlag

    def doOpen(self, timeout=5):
        newTimestamp = time() + timeout
        if (self.closeTimestamp < newTimestamp):
            self.closeTimestamp = newTimestamp

        self.openFlag = True
        self.setDoorOpen()

    def tick(self):
        if self.openFlag and time() > self.closeTimestamp:
            self.setDoorClosed()
            self.openFlag = False;

    def setDoorOpen(self):
        print("door open")

    def setDoorClosed(self):
        print("door closed")
