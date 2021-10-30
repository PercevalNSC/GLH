from .geo2 import distance as g2dist
from .Caliper import gravityPointDistance
from .GeoJSON import PointGeojson, LineGeojson
from .Plotfigure import coordinatesFigure
import pprint
from sklearn.cluster import DBSCAN
import numpy as np

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

    def trajectoryList(self, element1, element2):
        return [ [item["lngE7"], item["latE7"], item["timestampMs"]] for item in self.document[self.segment][element1][element2]]

    def trajectryListNoTimestamp(self, element1, element2):
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
        if ("longitudeE7" in location) & ("latitudeE7" in location):
            return [[location["longitudeE7"], location["latitudeE7"], timestamp]]
        else:
            return []

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
    
    def trajectoryList(self):
        for document in self.collection:
            self.trajectry_list.extend(GLHDocument(document, self.segment).trajectoryList(self.element1, self.element2))   
    
    def exportJson(self):
        path = self.segment + "." + self.element1 + "." + self.element2
        return {"datatype": path, "data": self.trajectry_list}
    def exportGeoJson(self):
        path = self.segment + "." + self.element1 + "." + self.element2
        geojsonObj = PointGeojson(path, self.trajectry_list)
        return geojsonObj.geojson

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
    def trajectoryList(self):
        for document in self.collection:
            self.trajectry_list.extend(GLHDocumentAs(document).trajectoryList(self.element1, self.element2))
        return self.trajectry_list

class GLHCollectionAsWp(GLHCollection):
    def __init__(self, collection):
        segment = "activitySegment"
        element1 = "waypointPath"
        element2 = "waypoints"
        super().__init__(collection, segment, element1, element2)
    def trajectoryList(self):
        for document in self.collection:
            self.trajectry_list.extend(GLHDocumentAs(document).trajectryListNoTimestamp(self.element1, self.element2))

class GLHCollectionPvSrp(GLHCollection):
    def __init__(self, collection):
        segment = "placeVisit"
        element1 = "simplifiedRawPath"
        element2 = "points"
        super().__init__(collection, segment, element1, element2)
    def trajectoryList(self):
        for document in self.collection:
            self.trajectry_list.extend(GLHDocumentPv(document).trajectoryList(self.element1, self.element2))
        return self.trajectry_list
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
    def trajectoryList(self):
        for document in self.collection:
            self.trajectry_list.extend(GLHDocumentPv(document).locationList())

class RoutePath :
    def __init__(self, corsor):
        self.collection = corsor
        self.route_path = []

    def createRoutePath(self) : 
        for document in self.collection :
            self.route_path.extend(self.docRoutePath(document))

    def docRoutePath(self, document):
        docList = []
        if "activitySegment" in document :
            docList.extend(self.activitySegmentPath(document["activitySegment"]))
        elif "placeVisit" in document :
            docList.append(self.placeVisitPath(document["placeVisit"]))
        else : 
            print("undefined Segment")
        return docList

    def activitySegmentPath(self, segment) :
        if "simplifiedRawPath" in segment :
            return [[point["lngE7"], point["latE7"]] for point in segment["simplifiedRawPath"]["points"]]
        else:
            return [[]]
    
    def placeVisitPath(self, segment):
        location = segment["location"]
        if ("longitudeE7" in location) & ("latitudeE7" in location):
            return [location["longitudeE7"], location["latitudeE7"]]
        else:
            return []
    
    def exportGeoJson(self):
        path = "all_route_path"
        geojsonObj = LineGeojson(path, self.route_path)
        return geojsonObj.geojson

class GLHTrajectoryData():
    def __init__(self, collection) -> None:
        self.glhtrajectorydata : TrajectoryData = self._trajectorydataCostructor(collection)

    def _trajectorydataCostructor(self, collection):
        return TrajectoryData([])
    
    def dbscan(self, eps, min_samples):
        self.clustering = self.glhtrajectorydata.dbscan(eps, min_samples)
        path = "ClusterPoint"
        geojsonObj = LineGeojson(path, self.clustering.labelPoint())
        return geojsonObj.geojson
    
    def exportGeojson(self):
        coordinates = [x[:2] for x in self.glhtrajectorydata]
        path = "trajectry_data"
        geojsonObj = LineGeojson(path, coordinates)
        return geojsonObj.geojson
    def exportFigure(self):
        coordinatesFigure(self.glhtrajectorydata, "clustering")
    def print(self):
        pprint.pprint(self.glhtrajectorydata)

class ASTrajectoryData(GLHTrajectoryData):
    def __init__(self, collection) -> None:
        super().__init__(collection)
    
    def _trajectorydataCostructor(self, collection):
        return TrajectoryData(GLHCollectionAsSrp(collection).trajectoryList())

class PVTrajectoryData(GLHTrajectoryData):
    def __init__(self, collection) -> None:
        super().__init__(collection)
    
    def _trajectorydataCostructor(self, collection):
        return TrajectoryData(GLHCollectionPvSrp(collection).trajectoryList())

class AllTrajectoryData(GLHTrajectoryData):
    def __init__(self, collection1, collection2) -> None:
        self.glhtrajectorydata = self._trajectorydataCostructor(collection1, collection2)
    def _trajectorydataCostructor(self, assrp_collection,pvsrp_collection):
        assrp_trajectorydata = ASTrajectoryData(assrp_collection).glhtrajectorydata.trajectorydata.tolist()
        pvsrp_trajectorydata = PVTrajectoryData(pvsrp_collection).glhtrajectorydata.trajectorydata.tolist()
        trajectorydata = assrp_trajectorydata + pvsrp_trajectorydata
        return TrajectoryData(sorted(trajectorydata, key=lambda x: x[2]))

class TrajectoryData():
    def __init__(self, trajectorydata: list) -> None:
        self.trajectorydata : np.ndarray = np.array(self.removeNoise(trajectorydata))

    def removeNoise(self, rawdata: list):
        for x in rawdata:
            if 0 in x:
                rawdata.remove(x)
        return rawdata
    def coordinates(self):
        return self.trajectorydata[:, 0:2]
    
    def dbscan(self, eps, min_samples):
        return DBSCANCoodinates(self.coordinates(), eps, min_samples)

    
class DBSCANCoodinates():
    def __init__(self, coordinates, eps, min_samples) -> None:
        self.coordinates = coordinates
        self.clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(self.coordinates)
    def labelPoint(self):
        return self._labelGravityPoint(self.labelCoordinates())
    def labelCoordinates(self):
        labelcoordinates = []
        for i in range(-1, max(self.clustering.labels_)):
            one_label_coordinates = [list(self.coordinates[index]) for index, label in enumerate(self.clustering.labels_) if i == label]
            labelcoordinates.append([i, one_label_coordinates])              
        return labelcoordinates
    def _labelGravityPoint(self, labelcoordinates):
        result = []
        for l in labelcoordinates:
            if l[0] == -1 :
                continue
            else:
                sum = [0.0, 0.0]
                for c in l[1]:
                    sum[0] += c[0]
                    sum[1] += c[1]
                gp = [x/len(l[1]) for x in sum]
                result.append(gp)
        return result

    def clusteringFigure(self):
        coordinatesFigure(self.coordinates, "DBSCAN", self.clustering.labels_)
    def clusterstat(self):
        # print(self.clustering.labels_)
        print(max(self.clustering.labels_))

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
    
