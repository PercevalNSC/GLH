import CreateGeoJSON

class BaseLngLatList :
    # Parent object of AsSimplifiedRawPath, AsWaypointPath and PvSimplifiedRawPath
    # And dummy object, it's no operation
    def __init__(self, corsor):
        self.corsor = corsor
        self.segment = ""
        self.v1 = ""
        self.v2 = ""
        self.lnglatlist = []

    def makingCollectionList(self):
        for document in self.corsor :
            doclist = self.makingDocumentList(document)
            self.lnglatlist.extend(doclist)
    def makingDocumentList(self, document):
        documentlist = []
        for item in document[self.segment][self.v1][self.v2] :
            documentlist.append([item["lngE7"], item["latE7"], item["timestampMs"]])
        return documentlist
    def makingDocumentListNotimestamp(self, document):
        documentlist = []
        for item in document[self.segment][self.v1][self.v2] :
            documentlist.append([item["lngE7"], item["latE7"], "NULL"])
        return documentlist

    def jsonBluster(self) :
        path = self.segment + "." + self.v1 + "." + self.v2
        return {"datatype": path, "data": self.lnglatlist}
    def geojsonBluster(self) :
        path = self.segment + "." + self.v1 + "." + self.v2
        geojsonObj = CreateGeoJSON.PointGeojson(path, self.lnglatlist)
        return geojsonObj.geojson
    
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
    def makingDocumentList(self, document):
        return super().makingDocumentListNotimestamp(document)

class PvSimplifiedRawPath(BaseLngLatList):
    def __init__(self, corsor):
        super().__init__(corsor)
        self.segment = "placeVisit"
        self.v1 = "simplifiedRawPath"
        self.v2 = "points"   

class PvLocation(BaseLngLatList):
    def __init__(self, corsor):
        super().__init__(corsor)
        self.segment = "placeVisit"
        self.v1 = "location"
    def makingDocumentList(self, document):
        documentlist = []
        location = document[self.segment][self.v1]
        duration = document[self.segment]["duration"]
        timestamp = int((duration["startTimestampMs"] + duration["endTimestampMs"])/2)
        documentlist.append([location["longitudeE7"], location["latitudeE7"], timestamp])
        return documentlist

class RoutePath :
    def __init__(self, corsor):
        self.corsor = corsor
        self.clctList = []

    def createRoutePath(self) : 
        for document in self.corsor :
            self.clctList.extend(self.docRoutePath(document))

    def docRoutePath(self, document):
        docList = []
        if "activitySegment" in document :
            docList.extend(self.activitySegmentPath(document["activitySegment"]))
        elif "placeVisit" in document :
            location = document["placeVisit"]["location"]
            docList.append([location["longitudeE7"], location["latitudeE7"]])
        else : 
            print("undefined Segment")
        return docList

    def activitySegmentPath(self, segment) :
        segmentList = []
        if "simplifiedRawPath" in segment :
            for point in segment["simplifiedRawPath"]["points"] :
                segmentList.append([point["lngE7"], point["latE7"]])

        return segmentList
    
    def geojsonbluster(self):
        path = "all_route_path"
        geojsonObj = CreateGeoJSON.LineGeojson(path, self.clctList)
        return geojsonObj.geojson

if __name__ == "__main__" :
    from pymongo import MongoClient

    with MongoClient("mongodb://127.0.0.1:27017") as client:
        test_db = client.glh_db
        test_collection = test_db.glh_clct_2
        corsor = test_collection.find()

    obj = RoutePath(corsor)
    obj.createRoutePath()
    print(obj.geojsonbluster())