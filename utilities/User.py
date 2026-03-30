import db

class User:
    def __init__(self, userID, chatID, firstname=None, username=None):
        self.id = int(userID)
        self.chatID = int(chatID)
        
        self.database = db.Database()
        data = self.database.getUser(self.id, self.chatID)

        if data is None:
            self.database.insertNewUser(self.id, self.chatID, firstname or "Unknown", username)
            data = self.database.getUser(self.id, self.chatID)

        if firstname and data.get("firstname") != firstname:
            self.database.updateUserFirstname(self.id, self.chatID, firstname)
            data["firstname"] = firstname
            
        if username and data.get("username") != username:
            self.database.updateUserProfile(self.id, self.chatID, data.get("firstname"), username)
            data["username"] = username

        self.firstname = data.get("firstname")
        self.username = data.get("username")
        self.marriedTo = data.get("marriedTo")
        self.marriedAt = data.get("marriedAt")
        self.petID = data.get("petID")

    def updateUser(self, firstname=None, marriedTo=None, marriedAt=None, petID=None):
        if firstname is not None:
            self.database.updateUserFirstname(self.id, self.chatID, firstname)

        if marriedTo is not None:
            self.database.updateUserMarriedTo(self.id, self.chatID, marriedTo)

        if marriedAt is not None:
            self.database.updateUserMarriedAt(self.id, self.chatID, marriedAt)

        if petID is not None:
            self.database.updateUserPet(self.id, self.chatID, petID)