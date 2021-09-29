from pymongo import MongoClient
import json

class MongoDBSet :
    def __init__(self):
        mongodb_path = "mongodb://127.0.0.1:27017"
        with MongoClient(mongodb_path) as client:
            self.glh_db = client.glh_db
            self.glh_clct = self.glh_db.glh_clct_1

    def query(self, query, limit = 0):
        corsor = self.glh_clct.find(query).limit(limit)
        return corsor
    
    def countQuery(self, query):
        return self.glh_clct.count_documents(query)
    
    def asSrpQuery(self, limit = 0):
        query = {"activitySegment.simplifiedRawPath" : {"$exists": True}}
        return self.query(query, limit)
    
    def asWpQuery(self, limit = 0):
        query = {"activitySegment.waypointPath" : {"$exists": True}}
        return self.query(query, limit)
    
    def pvSrpQuery(self, limit = 0):
        query = {"activitySegment.waypointPath" : {"$exists": True}}
        return self.query(query, limit)
    
    def pvLocatinQuery(self, limit = 0):
        query = {"placeVisit.location" : {"$exists": True}}
        return self.query(query, limit)

    def stat(self):
        querys = [{"activitySegment" : {"$exists": True}},
            {"placeVisit" : {"$exists": True}},
            {"activitySegment.simplifiedRawPath" : {"$exists": True}},
            { "placeVisit.simplifiedRawPath" : {"$exists": True}}]    
        for query in querys :
            print("Query: " + json.dumps(query) + ", Count: " + str(self.countQuery(query)))
            
    def printCorsor(self, corsor):
        for i in corsor:
            print(i)

if __name__ == "__main__" :
    cl = MongoDBSet()
    cl.printCorsor(cl.queryMongodb({}, 10))