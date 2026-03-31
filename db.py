from supabase import create_client
import os

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

class Database:
    def __init__(self):
        self.supabase = create_client(url, key)

    def getClient(self):
        return self.supabase
    
    def lookUpUser(self, userID, chatID):
        db = self.getClient()
        response = db.table("users").select("*").eq("userID", int(userID)).eq("chatID", int(chatID)).execute()
        return bool(response.data)
    
    def insertNewUser(self, userID, chatID, firstname, username=None):
        db = self.getClient()
        db.table("users").upsert({
            "userID": int(userID),
            "chatID": int(chatID),
            "firstname": firstname,
            "username": username
        }).execute()

    def getUserByUsername(self, username, chatID):
        db = self.getClient()
        username = username.lstrip("@")
        response = db.table("users").select("*").eq("username", username).eq("chatID", int(chatID)).execute()
        return response.data[0] if response.data else None

    def updateUserProfile(self, userID, chatID, firstname, username=None):
        db = self.getClient()
        db.table("users").upsert({
            "userID": int(userID),
            "chatID": int(chatID),
            "firstname": firstname,
            "username": username
        }).execute()

    def updateUserFirstname(self, userID, chatID, firstname):
        db = self.getClient()
        db.table("users").upsert({
            "userID": int(userID),
            "chatID": int(chatID),
            "firstname": firstname
        }).execute()

    def updateUserMarriedTo(self, userID, chatID, marriedTo):
        db = self.getClient()
        db.table("users").upsert({
            "userID": int(userID),
            "chatID": int(chatID),
            "marriedTo": marriedTo
        }).execute()

    def updateUserMarriedAt(self, userID, chatID, marriedAt):
        db = self.getClient()
        db.table("users").upsert({
            "userID": int(userID),
            "chatID": int(chatID),
            "marriedAt": marriedAt
        }).execute()

    def updateUserPet(self, userID, chatID, petID):
        db = self.getClient()
        db.table("users").upsert({
            "userID": int(userID),
            "chatID": int(chatID),
            "petID": petID
        }).execute()

    def getUserMarriedTo(self, userID, chatID):
        db = self.getClient()
        response = (db.table("users").select("*").eq("userID", int(userID)).eq("chatID", int(chatID)).execute()).data
        return response[0]["marriedTo"] if response else None
    
    def getUserMarriedAt(self, userID, chatID):
        db = self.getClient()
        response = (db.table("users").select("*").eq("userID", int(userID)).eq("chatID", int(chatID)).execute()).data
        return response[0]["marriedAt"] if response else None
    
    def getFirstname(self, userID, chatID):
        db = self.getClient()
        response = (db.table("users").select("*").eq("userID", int(userID)).eq("chatID", int(chatID)).execute()).data
        return response[0]["firstname"] if response else None
    
    def getUserPetID(self, userID, chatID):
        db = self.getClient()
        response = (db.table("users").select("*").eq("userID", int(userID)).eq("chatID", int(chatID)).execute()).data
        return response[0]["petID"] if response else None

    def getUser(self, userID, chatID):
        db = self.getClient()
        response = db.table("users").select("*").eq("userID", int(userID)).eq("chatID", int(chatID)).execute().data
        return response[0] if response else None
    
    def getMarriedList(self, chatID):
        db = self.getClient()
        response = db.table("users").select("*").eq("chatID", int(chatID)).not_.is_("marriedTo", "NULL").order("marriedAt", desc=False).execute().data
        return response if response else None
    
    def getPet(self, userID):
        db = self.getClient()
        response = db.table("pets").select("*").eq("userID", int(userID)).execute().data
        return response[0] if response else None
    
    def insertNewPet(self, userID, petName, petType, isRare, bornAt):
        db = self.getClient()
        db.table("pets").insert({
            "userID": int(userID),
            "petName": petName,
            "petType": petType,
            "isRare": isRare,
            "bornAt": bornAt
        }).execute()