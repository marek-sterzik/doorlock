import uuid, json, re, fcntl, os
from time import time

class DB:
    def __init__(self, filename):
        self.fd = open(filename, "a+")
        fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        self.readFile()
        #debug output
        print(json.dumps(self.data))

    def read(self, recordClass, idRecord):
        if (not recordClass in self.data):
            return None
        if (not idRecord in self.data[recordClass]):
            return None
        return self.data[recordClass][idRecord]

    def write(self, recordClass, idRecord, data):
        if (not recordClass in self.data):
            self.data[recordClass] = {}
        self.data[recordClass][idRecord] = data
        self.writeFile()
        #debug output
        print(json.dumps(self.data))

    def remove(self, recordClass, idRecord):
        if (recordClass in self.data and idRecord in self.data[recordClass]):
            del self.data[recordClass]
        self.writeFile()
        #debug output
        print(json.dumps(self.data))

    def list(self, recordClass):
        if (not recordClass in self.data):
            return []
        return self.data[recordClass].keys()

    def readFile(self):
        self.fd.seek(0)
        self.data = json.load(self.fd)

    def writeFile(self):
        self.fd.seek(0)
        self.fd.truncate()
        json.dump(self.data, self.fd)

class SessionDB:
    def __init__(self, db):
        self.db = db

    def createSession(self, username):
        sid=str(uuid.UUID(bytes = os.urandom(16)))
        self.db.write("session", sid, {"username": username, "timestamp": time()})
        return sid;

    def querySession(self, sid):
        sessionData = self.db.read("session", sid);
        if (sessionData is None):
            return None;

        return sessionData["username"]

    def logoutSession(self, sid):
        self.db.remove("session", sid)



class UserDB:
    def __init__(self, db):
        self.db = db

    def getUser(self, username):
        userData = self.db.read("user", username)
        if (username == 'admin' and not self.adminExists()):
            if (userData is None):
                userData = {"username": "admin", "password": "admin", "admin": True}
            userData["admin"] = True;

        if (userData is None):
            return None

        return User(self.db, userData);
    
    def createUser(self, username, password):
        userData = {"username": username, "password": None, "admin": False}
        user = User(self.db, userData)
        user.setPassword(password)
        user.store()

    def isValidUsername(self, username):
        return re.match(r'^[a-zA-Z0-9_\-\.]+$', username)

    def adminExists(self):
        for username in self.db.list("user"):
            userData = self.db.read("user", username)
            if (userData["admin"]):
                return True
        return False;


class User:
    def __init__(self, db, userData):
        self.db = db
        self.userData = userData

    def checkPassword(self, password):
        if (self.userData["password"] is None):
            return True
        if (self.userData["password"] == password):
            return True
        return False

    def allowedOpen(self):
        return True;

    def allowedQueryOpen(self):
        return True;

    def allowedAdmin(self):
        return self.userData["admin"];

    def setPassword(self, password):
        self.userData["password"] = password
    
    def setAdmin(self, isAdmin):
        self.userData["admin"] = isAdmin
        self.store()

    def store(self):
        self.db.write("user", self.userData["username"], self.userData)

    def delete(self):
        self.db.remove("user", self.userData["username"])
        for sid in self.db.list("session"):
            sessionData = self.db.read("session", sid)
            if (sessionData["username"] == self.userData["username"]):
                self.db.remove("session", db)
