from .Lock import Lock

class Doorlock:
    def __init__(self, dryRun):
        self.lock = Lock(dryRun)
        
    def status(self, sid):
        if not self.isAuthorized(sid):
            return {"code": "invalid_sid"}
        
        doorOpen = self.lock.isOpen()

        return {"code": "ok", "doorOpen": doorOpen}


    def open(self, sid):
        if not self.isAuthorized(sid):
            return {"code": "invalid_sid"}
        
        self.lock.doOpen()

        return {"code": "ok"}

    def tick(self):
        self.lock.tick()
            
    def isAuthorized(self, sid):
        if sid == 'abcdef':
            return True
        else:
            return False
