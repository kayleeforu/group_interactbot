import db
from datetime import datetime, timezone

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

    def getAge(self) -> str:
        now = datetime.now(timezone.utc)
        bornAt = datetime.fromisoformat(self.bornAt)
        difference = now - bornAt
        days = difference.days if difference.days >= 1 else None
        hours = difference.seconds // 3600 if (difference.seconds // 3600) >= 1 else None
        minutes = (difference.seconds % 3600) // 60
        if days is not None:
            age = f"{days} days {hours} hours {minutes} minutes"
        elif hours is not None:
            age = f"{hours} hours {minutes} minutes"
        else:
            age = f"{minutes} minutes"
        
        return age