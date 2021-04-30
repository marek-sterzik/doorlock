from .Lock import Lock

class Doorlock:
    def __init__(self, dryRun, key):
        self.lock = Lock(dryRun)
        self.key = key
        
    def status(self, sid):
        if not self.isAuthorized(sid):
            return {"code": "nuauthorized"}
        
        doorOpen = self.lock.isOpen()

        return {"code": "ok", "doorOpen": doorOpen}


    def open(self, sid):
        if not self.isAuthorized(sid):
            return {"code": "unauthorized"}
        
        self.lock.doOpen()

        return {"code": "ok"}

    def tick(self):
        self.lock.tick()
            
    def isAuthorized(self, sid):
        if self.key == None or self.key == sid:
            return True
        else:
            return False
