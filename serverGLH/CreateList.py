class CreateGeojson() :
    def __init__(self,name, list):
        self.geojson = {
            "type": "FeatureCollection",
            "name": name,
            "crs": {
                "type": "name",
                "properties": {
                    "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
                }
            },
            "features": self.makingFeature(list)
        }
    
    def makingFeature(self, list):
        features = []
        neko = 0
        for coordinates in list :
            feature = {
                "type": "Feature",
                "properties": {
                    "description": "neko: " + str(neko),
                    "timestamp" : 0
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": coordinates
                }
            }
            features.append(feature)
            neko += 1
        return features
        
class BaseLngLatList :
    # Parent object of AsSimplifiedRawPath, AsWaypointPath and PvSimplifiedRawPath
    # And dummy object, it's no operation
    def __init__(self, corsor):
        self.corsor = corsor
        self.segment = ""
        self.v1 = ""
        self.v2 = ""
        self.lnglatlist = []
    def makingFieldList(self):
        for document in self.corsor :
            doclist = self.makingDocumentList(document)
            for item in doclist:
                self.lnglatlist.append(item)
    def makingDocumentList(self, document):
        documentlist = []
        for item in document[self.segment][self.v1][self.v2] :
            documentlist.append([item["lngE7"], item["latE7"]])
        return documentlist
    def jsonBluster(self) :
        path = self.segment + "." + self.v1 + "." + self.v2
        return {"datatype": path, "data": self.lnglatlist}
    def geojsonBluster(self) :
        path = self.segment + "." + self.v1 + "." + self.v2
        geojsonObj = CreateGeojson(path, self.lnglatlist)
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

class PvSimplifiedRawPath(BaseLngLatList):
    def __init__(self, corsor):
        super().__init__(corsor)
        self.segment = "placeVisit"
        self.v1 = "simplifiedRawPath"
        self.v2 = "points"   

class PvCoordinate(BaseLngLatList):
    def __init__(self, corsor):
        super().__init__(corsor)
        self.segment = "placeVisit"
        self.v1 = "location"
    def makingDocumentList(self, document):
        documentlist = []
        item = document[self.segment][self.v1]
        documentlist.append([item["longitudeE7"], item["latitudeE7"]])
        return documentlist

if __name__ == "__main__" :
    from pymongo import MongoClient

    with MongoClient("mongodb://127.0.0.1:27017") as client:
        test_db = client.glh_db
        test_collection = test_db.glh_clct_2
        corsor = test_collection.find({"placeVisit.location": {"$exists": True}},{"placeVisit.location": 1})

    obj = PvCoordinate(corsor)
    obj.makingFieldList()
    print(obj.jsonBluster())