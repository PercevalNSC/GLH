from pymongo import MongoClient
import json

class MongoDBSet :
    def __init__(self, db_name = "glh_db", clct_name = "glh_clct_full"):
        mongodb_path = "mongodb://127.0.0.1:27017"
        with MongoClient(mongodb_path) as client:
            self.db = client[db_name]
            self.collection = self.db[clct_name]

    def query(self, query, limit = 0):
        corsor = self.collection.find(query).limit(limit)
        return corsor
    
    def count_query(self, query):
        return self.collection.count_documents(query)
    
    def assrp_query(self, limit = 0):
        query = {"activitySegment.simplifiedRawPath" : {"$exists": True}}
        return self.query(query, limit)
    
    def aswp_query(self, limit = 0):
        query = {"activitySegment.waypointPath" : {"$exists": True}}
        return self.query(query, limit)
    
    def pvsrp_query(self, limit = 0):
        query = {"placeVisit.simplifiedRawPath" : {"$exists": True}}
        return self.query(query, limit)
    
    def pvlocation_query(self, limit = 0):
        query = {"placeVisit.location" : {"$exists": True}}
        return self.query(query, limit)

    def insert(self, data_dict):
        result = self.collection.insert_one(data_dict)
        print(result)
    
    def insertmany(self, data_list: list):
        self.collection.delete_many({})
        result = self.collection.insert_many(data_list)
        print(result)
        print("Insert", len(data_list), "objects.")


    def stat(self):
        querys = [{"activitySegment" : {"$exists": True}},
            {"placeVisit" : {"$exists": True}},
            {"activitySegment.simplifiedRawPath" : {"$exists": True}},
            { "placeVisit.simplifiedRawPath" : {"$exists": True}}]    
        for query in querys :
            print("Query: " + json.dumps(query) + ", Count: " + str(self.count_query(query)))
            
    def print_corsor(self, corsor):
        for i in corsor:
            print(i)
        corsor.rewind()

if __name__ == "__main__" :
    cl = MongoDBSet()
    cl.print_corsor(cl.query({}, 10))