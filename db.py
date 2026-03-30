from supabase import create_client
import os

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

class Database:
    def __init__(self):
        self.supabase = create_client(url, key)
    def getClient(self):
        return self.supabase
    
    def lookUpUser(self, userID):
        db = self.getClient()
        response = db.table("users").select("*").eq("userID", int(userID)).execute()
        return bool(response.data)
    
    def insertNewUser(self, userID, firstname):
        db = self.getClient()
        db.table("users").upsert({
            "userID": int(userID),
            "firstname": firstname
        }).execute()

    def updateUserFirstname(self, userID, firstname):
        db = self.getClient()
        db.table("users").upsert({
            "userID": int(userID),
            "firstname": firstname
        }).execute()

    def updateUserMarriedTo(self, userID, marriedTo):
        db = self.getClient()
        db.table("users").upsert({
            "userID": int(userID),
            "marriedTo": marriedTo
        }).execute()

    def updateUserMarriedAt(self, userID, marriedAt):
        db = self.getClient()
        db.table("users").upsert({
            "userID": int(userID),
            "marriedAt": marriedAt
        }).execute()

    def updateUserPet(self, userID, petID):
        db = self.getClient()
        db.table("users").upsert({
            "userID": userID,
            "petID": petID
        }).execute()

    def getUserMarriedTo(self, userID):
        db = self.getClient()
        response = (db.table("users").select("*").eq("userID", int(userID)).execute()).data
        return response[0]["marriedTo"]
    
    def getUserMarriedAt(self, userID):
        db = self.getClient()
        response = (db.table("users").select("*").eq("userID", int(userID)).execute()).data
        return response[0]["marriedAt"]
    
    def getFirstname(self, userID):
        db = self.getClient()
        response = (db.table("users").select("*").eq("userID", int(userID)).execute()).data
        return response[0]["firstname"]
    
    def getPet(self, userID):
        db = self.getClient()
        response = (db.table("users").select("*").eq("userID", int(userID)).execute()).data
        return response[0]["petID"]