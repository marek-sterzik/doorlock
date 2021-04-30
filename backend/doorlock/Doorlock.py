from .Db import SessionDB
from .Db import UserDB
from .Db import DB
from .Lock import Lock

class Doorlock:
    def __init__(self):
        db = DB("db.json");
        self.sessionDB = SessionDB(db)
        self.userDB = UserDB(db)
        self.lock = Lock()
        
    def login(self, username, password):
        user = self.userDB.getUser(username);
        
        if user is None:
            return {"code": "invalid_credentials"}

        if not user.checkPassword(password):
            return {"code": "invalid_credentials"}

        sessionId = self.sessionDB.createSession(username)

        if sessionId is None:
            return {"code": "action_failed"}
        
        return {"code": "ok", "sessionId": sessionId}

    def logout(self, sid):
        if not self.sessionDB.logoutSession(sid):
            return {"code": "invalid_sid"}
        
        return {"code": "ok"}

    def status(self, sid):
        user = self.getLoggedInUser(sid)
        
        if user is None:
            return {"code": "invalid_sid"}
        
        if not user.allowedQueryOpen():
            return {"code": "not_authorized"}
        
        doorOpen = self.lock.isOpen()

        return {"code": "ok", "doorOpen": doorOpen}


    def open(self, sid):
        user = self.getLoggedInUser(sid)
        
        if user is None:
            return {"code": "invalid_sid"}
        
        if not user.allowedOpen():
            return {"code": "not_authorized"}
        
        self.lock.doOpen()

        return {"code": "ok"}


    def createUser(self, sid, username, password):
        user = self.getLoggedInUser(sid)
        if user is None:
            return {"code": "invalid_sid"}

        if not user.allowedAdmin():
            return {"code": "not_authorized"}

        if not self.userDB.isValidUsername(username):
            return {"code": "invalid_username"}

        if not (self.userDB.getUser(username) is None):
            return {"code": "user_exists"}

        self.userDB.createUser(username, password)

        return {"code": "ok"}


    def setUserPassword(self, sid, username, password, oldPassword):
        user = self.getLoggedInUser(sid)
        if user is None:
            return {"code": "invalid_sid"}

        if not (username is None) or (oldPassword is None):
            if not user.allowedAdmin():
                return {"code": "not_authorized"}
            
        if username is None:
            modifiedUser = user
        else:
            modifiedUser = self.userDB.getUser(username)

        if modifiedUser is None:
            return {"code": "unknown_user"}

        if (not (oldPassword is None)) and (not modifiedUser.checkPassword(oldPassword)):
            return {"code": "unknown_user"}

        modifiedUser.setPassword(password)
        modifiedUser.store()
            
        return {"code": "ok"}

    def setUserPermissions(self, sid, username, isAdmin):
        user = self.getLoggedInUser(sid)
        
        if user is None:
            return {"code": "invalid_sid"}
        
        if not user.allowedAdmin():
            return {"code": "not_authorized"}

        modifiedUser = self.userDB.getUser(username)

        if modifiedUser is None:
            return {"code": "unknown_user"}

        modifiedUser.setAdmin(isAdmin)
        
        return {"code": "ok"}

    def deleteUser(self, sid, username):
        user = self.getLoggedInUser(sid)
        
        if user is None:
            return {"code": "invalid_sid"}
        
        if not user.allowedAdmin():
            return {"code": "not_authorized"}
        
        deletedUser = self.userDB.getUser(username)

        if deletedUser is None:
            return {"code": "unknown_user"}

        deletedUser.delete()

        return {"code": "ok"}

    def tick(self):
        self.lock.tick()
            
    def getLoggedInUser(self, sid):
        username = self.sessionDB.querySession(sid)
        if username is None:
            return None
        user = self.userDB.getUser(username)
        if user is None:
            print ("logout: "+ sid)
            self.sessionDB.logoutSession(sid)
        return user
