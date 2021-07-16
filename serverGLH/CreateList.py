class BaseLngLatList :
    def __init__(self, corsor):
        self.corsor = corsor
        self.segment = ""
        self.v1 = ""
        self.v2 = ""
        self.lnglatlist = []
    def makingDocumentList(self, document):
        documentlist = []
        for item in document[self.segment][self.v1][self.v2] :
            documentlist.append([item["lngE7"], item["latE7"]])
        return documentlist
    def makingFieldList(self):
        for document in self.corsor :
            doclist = self.makingDocumentList(document)
            for item in doclist:
                self.lnglatlist.append(item)

class AsSimplifiedRawPath(BaseLngLatList):
    def __init__(self, corsor):
        super().__init__(corsor)
        self.segment = "activitySegment"
        self.v1 = "simplifiedRawPath"
        self.v2 = "points"

class AsWaypointPath(BaseLngLatList):
    def __init__(self, corsor):
        super().__init__(corsor)
        self.segment = "activitySegment"
        self.v1 = "waypointPath"
        self.v2 = "waypoints"

class PvSimplifiedRawPath(BaseLngLatList):
    def __init__(self, corsor):
        super().__init__(corsor)
        self.segment = "placeVisit"
        self.v1 = "simplifiedRawPath"
        self.v2 = "points"
    

if __name__ == "__main__" :
    from pymongo import MongoClient

    with MongoClient("mongodb://127.0.0.1:27017") as client:
        test_db = client.glh_db
        test_collection = test_db.glh_clct_1
        corsor = test_collection.find({"activitySegment.simplifiedRawPath": {"$exists": True}},{"activitySegment.simplifiedRawPath": 1})

    obj = AsSimplifiedRawPath(corsor)
    obj.makingFieldList()
    print(obj.lnglatlist)