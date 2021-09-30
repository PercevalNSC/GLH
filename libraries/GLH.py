from geo2 import distance as g2dist
from Caliper import gravityPointDistance


class GLHPoints():
    def __init__(self, points):
        self.points = points
    
    def pointsDifference(self):
        result = []
        for index in range(len(self.points)-1):
            result.append({"dist": self.pointsDistance(self.points[index], self.points[index+1]),
                "duration": self.pointsDuration(self.points[index], self.points[index+1])})
        
        return result

    def pointsDistance(self, point1, point2):
        coord1 = [point1["latE7"], point1["lngE7"]]
        coord2 = [point2["latE7"], point2["lngE7"]]
        return g2dist(coord1, coord2) * 1000
    def pointsDuration(self, point1, point2):
        duration = abs(point2["timestampMs"] - point1["timestampMs"] )
        return msToMinite(duration)
    
    def len(self):
        return len(self.points)
    def coordinates(self):
        return [[p["latE7"], p["lngE7"]] for p in self.points]

class GLHDocument():
    def __init__(self, document, segment):
        self.document = document
        self.segment = segment

    def trajectlyList(self, element1, element2):
        return [ [item["lngE7"], item["latE7"], item["timestampMs"]] for item in self.document[self.segment][element1][element2]]

    def trajectlyListNoTimestamp(self, element1, element2):
        return [ [item["lngE7"], item["latE7"], "NULL"] for item in self.document[self.segment][element1][element2]]

class GLHDocumentAs(GLHDocument):
    def __init__(self, document):
        segment = "activitySegment"
        super().__init__(document, segment)

class GLHDocumentPv(GLHDocument):
    def __init__(self, document):
        segment = "placeVisit"
        super().__init__(document, segment)
    
    def locationList(self):
        location = self.document[self.segment]["location"]
        duration = self.document[self.segment]["duration"]
        timestamp = int((duration["startTimestampMs"] + duration["endTimestampMs"])/2)
        return [[location["longitudeE7"], location["latitudeE7"], timestamp]]
    def locationDuration(self):
        duration = self.document[self.segment]["duration"]
        return duration["endTimestampMs"] - duration["startTimestampMs"]
    # 空間的大きさと時間のリスト、１点しか無ければ空のリスト
    def regionDuration(self):
        points = GLHPoints(self.points())
        if points.len() < 2 :
            return []

        coordinates = points.coordinates()
        if points.len() == 2 :
            dist = g2dist(coordinates[0], coordinates[1]) * 1000
        else :
            dist = gravityPointDistance(coordinates)
        
        duration = msToMinite(self.locationDuration())
        return [dist, duration]

    def points(self):
        return self.document[self.segment]["simplifiedRawPath"]["points"]

class GLHCollection():
    def __init__(self, collection, segment, element1, element2):
        self.collection = collection
        self.segment = segment
        self.element1 = element1
        self.element2 = element2
        self.trajectry_list = []
    
    def differenceList(self):
        result = []

        for doc in self.collection :
            points = GLHPoints(doc[self.segment]["simplifiedRawPath"]["points"])
            diff = points.pointsDifference()
            result.extend(diff)

        return result
    
    def trajectlyList(self):
        for document in self.collection:
            self.trajectry_list.extend(GLHDocument(document, self.segment).trajectlyList(self.element1, self.element2))   
    
    def exportJson(self):
        path = self.segment + "." + self.element1 + "." + self.element2
        return {"datatype": path, "data": self.trajectry_list}
    

    def print(self):
        for doc in self.collection:
            print(doc)
        self.collection.rewind()
    
class GLHCollectionAsSrp(GLHCollection):
    def __init__(self, collection):
        segment = "activitySegment"
        element1 = "simplifiedRawPath"
        element2 = "points"
        super().__init__(collection, segment, element1, element2)
    def trajectlyList(self):
        for document in self.collection:
            self.trajectry_list.extend(GLHDocumentAs(document).trajectlyList(self.element1, self.element2))  

class GLHCollectionAsWp(GLHCollection):
    def __init__(self, collection):
        segment = "activitySegment"
        element1 = "waypointPath"
        element2 = "waypoints"
        super().__init__(collection, segment, element1, element2)
    def trajectlyList(self):
        for document in self.collection:
            self.trajectry_list.extend(GLHDocumentAs(document).trajectlyListNoTimestamp(self.element1, self.element2))

class GLHCollectionPvSrp(GLHCollection):
    def __init__(self, collection):
            segment = "placeVisit"
            element1 = "simplifiedRawPath"
            element2 = "points"
            super().__init__(collection, segment, element1, element2)
    def trajectlyList(self):
        for document in self.collection:
            self.trajectry_list.extend(GLHDocumentPv(document).trajectlyList(self.element1, self.element2))
    def regionDurationList(self):
        region_duration_list = [[],[]]
        for doc in self.collection :
            glh_doc_pv = GLHDocumentPv(doc)
            region_duration = glh_doc_pv.regionDuration()
            if len(region_duration) == 2 :
                region_duration_list[0].append(region_duration[0])
                region_duration_list[1].append(region_duration[1])
 
        return region_duration_list


class GLHCollectionPvLoc(GLHCollection):
    def __init__(self, collection):
            segment = "placeVisit"
            element1 = "location"
            element2 = ""
            super().__init__(collection, segment, element1, element2)
    def trajectlyList(self):
        for document in self.collection:
            self.trajectry_list.extend(GLHDocumentPv(document).locationList())

def msToMinite(timeMs):
    offset = 1000 * 60
    return timeMs / offset


if __name__ == '__main__' :

    segments = ["activitySegment", "placeVisit"]
    limits= [0, 0]
    elements = ["dist", "duration"]

    from MongoDBSetting import MongoDBSet

    client = MongoDBSet()
    client.stat()
    query = {"placeVisit.simplifiedRawPath" : {"$exists": True}}
    obj = GLHCollectionPvSrp(client.query(query))
    obj.print()
    print(obj.regionDurationList())
    
