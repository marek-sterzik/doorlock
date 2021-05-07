from .Lock import Lock

class Doorlock:
    def __init__(self, dryRun, key):
        self.lock = Lock(dryRun)
        self.key = key
        
    def status(self, sid):
        if not self.isAuthorized(sid):
            return {"code": "unauthorized"}
        
        return self.getStatus()


    def open(self, sid, timeout = 5000):
        if not self.isAuthorized(sid):
            return {"code": "unauthorized"}
        
        self.lock.doOpen(timeout)
        return self.getStatus()


    def getStatus(self):
        doorOpen = self.lock.isOpen()
        remainingDoorOpenTime = self.lock.getRemainingOpenTime()

        return {"code": "ok", "doorOpen": doorOpen, "remainingDoorOpenTime": remainingDoorOpenTime}


    def tick(self):
        self.lock.tick()


    def isAuthorized(self, sid):
        if self.key == None or self.key == sid:
            return True
        else:
            return False
