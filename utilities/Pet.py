import db
from datetime import datetime

class Pet:
    def __init__(self, userID, petName = None, petType = None, isRare = False):
        self.userID = userID
        
        self.database = db.Database()
        data = self.database.getPet(self.userID)

        if data is None:
            self.insertNewPet(petName, petType, isRare)
            data = self.database.getPet(self.userID)

        self.petID = data.get("petID")
        self.petName = data.get("petName")
        self.petType = data.get("petType")
        self.isRare = data.get("isRare")
        self.petWeight = data.get("petWeight")
        self.feedStreak = data.get("feedStreak")
        self.lastFedAt = data.get("lastFedAt")
        self.bornAt = data.get("bornAt")
        self.petMarriedTo = data.get("petMarriedTo")
        self.petMarriedAt = data.get("petMarriedAt")

    def insertNewPet(self, petName, petType, isRare):
        bornAt = datetime.now().isoformat()
        self.database.insertNewPet(self.userID, petName, petType, isRare, bornAt)