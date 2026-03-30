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
    
    def insertNewUser(self, userID, chatID, firstname):
        db = self.getClient()
        db.table("users").upsert({
            "userID": int(userID),
            "chatID": int(chatID),
            "firstname": firstname
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
        return response[0]["marriedTo"]
    
    def getUserMarriedAt(self, userID, chatID):
        db = self.getClient()
        response = (db.table("users").select("*").eq("userID", int(userID)).eq("chatID", int(chatID)).execute()).data
        return response[0]["marriedAt"]
    
    def getFirstname(self, userID, chatID):
        db = self.getClient()
        response = (db.table("users").select("*").eq("userID", int(userID)).eq("chatID", int(chatID)).execute()).data
        return response[0]["firstname"]
    
    def getPet(self, userID, chatID):
        db = self.getClient()
        response = (db.table("users").select("*").eq("userID", int(userID)).eq("chatID", int(chatID)).execute()).data
        return response[0]["petID"]
    
    def getUser(self, userID, chatID):
        db = self.getClient()
        response = db.table("users") \
            .select("*") \
            .eq("userID", int(userID)) \
            .eq("chatID", int(chatID)) \
            .execute().data

        if not response:
            return None

        return response[0]