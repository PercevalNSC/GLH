from pymongo import MongoClient
import json
from math import inf

DB_URL = "mongodb://127.0.0.1:27017"
GLH_DB_NAME = "glh_db"
GLH_CLCT_NAME = "glh_clct_1"
REACH_DB_NAME = "glh_reach"
REACH_CLCT_NAME = "data2"

class MongoDBSetting :
    def __init__(self, db_url, db_name, collection_name) -> None:
        with MongoClient(db_url) as client :
            self.db = client[db_name]
            self.collection = self.db[collection_name]
    
    def query(self, query, limit = 0):
        corsor = self.collection.find(query).limit(limit)
        return corsor
    
    def count_query(self, query):
        return self.collection.count_documents(query)

    def insert(self, data_dict):
        insert_result_condition = self.collection.insert_one(data_dict)
        print(insert_result_condition)
    
    def insertmany(self, data_list: list):
        self.collection.delete_many({})
        insert_result_condition = self.collection.insert_many(data_list)
        print(insert_result_condition)
        print("Insert", len(data_list), "objects.")
    
    def print_corsor(self, corsor):
        for i in corsor:
            print(i)
        corsor.rewind()

class GLHDB (MongoDBSetting) :
    def __init__(self, db_name = GLH_DB_NAME, clct_name = GLH_CLCT_NAME):
        super().__init__(DB_URL, db_name, clct_name)

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

    def stat(self):
        querys = [{"activitySegment" : {"$exists": True}},
            {"placeVisit" : {"$exists": True}},
            {"activitySegment.simplifiedRawPath" : {"$exists": True}},
            { "placeVisit.simplifiedRawPath" : {"$exists": True}}]    
        for query in querys :
            print("Query: " + json.dumps(query) + ", Count: " + str(self.count_query(query)))

class ReachabilityDB(MongoDBSetting):
    def __init__(self, db_name = REACH_DB_NAME, collection_name = REACH_CLCT_NAME) -> None:
        super().__init__(DB_URL, db_name, collection_name)
    
    def reachability_query(self, limit = 0):
        query = {}
        return self.query(query, limit)
    
    def reachability_json(self, limit = 0):
        corsor = self.reachability_query()
        return self._convert_json(corsor)
    
    def _convert_json(self, corsor):
        result_json = {"coordinates": [], "reachability": [], "ordering": [], "order_status": "UNDEFINED"}
        for document in corsor :
            result_json["coordinates"].append(document["data"][:-1])
            if document["reachability"] != inf :
                result_json["reachability"].append(document["reachability"])
            else :
                result_json["reachability"].append("inf")
            result_json["ordering"].append(document["order"]) 
        check_order = list(range(len(result_json["ordering"])))
        if check_order == result_json["ordering"] :
            result_json["order_status"] = "True"
        else :
            result_json["order_status"] = "False"
        return result_json
    

    