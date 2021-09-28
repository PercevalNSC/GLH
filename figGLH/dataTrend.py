import matplotlib.pyplot as plt
from geo2 import distance as g2dist
from caliper import rotating_calipers, gravityPointDistance
from mongodbSet import MongoDBSet


class GLHPoints():
    def __init__(self, points):
        self.points = points
    
    def pointsDifference(self):
        result = []
        for index in range(len(self.points)-1):
            result.append({"dist": self.docDistance(self.points[index], self.points[index+1]),
                "duration": self.docDuration(self.points[index], self.points[index+1])})
        
        return result

    def docDistance(self, doc1, doc2):
        coord1 = [doc1["latE7"], doc1["lngE7"]]
        coord2 = [doc2["latE7"], doc2["lngE7"]]
        return g2dist(coord1, coord2) * 1000
    def docDuration(self, doc1, doc2):
        duration = abs(doc2["timestampMs"] - doc1["timestampMs"] )
        return msToMinite(duration)
    
    def len(self):
        return len(self.points)
    def coordinates(self):
        return [[p["latE7"], p["lngE7"]] for p in self.points]

class GLHCollection():
    def __init__(self, collection, segment = ""):
        self.segment = segment
        self.collection = collection
    
    def differenceList(self):
        result = []

        for doc in self.collection :
            points = GLHPoints(doc[self.segment]["simplifiedRawPath"]["points"])
            diff = points.pointsDifference()
            result.extend(diff)

        return result
    
    def print(self):
        for doc in self.collection:
            print(doc)
    
class GLHCollectionAs(GLHCollection):
    def __init__(self, collection, segment = "activitySegment"):
        super().__init__(collection, segment)

class GLHCollectionPv(GLHCollection):
    def __init__(self, collection, segment = "placeVisit"):
        super().__init__(collection, segment)
    
    def regionDurationList(self):
        region_duration_list = [[],[]]
        for doc in self.collection :
            points = GLHPoints(doc[self.segment]["simplifiedRawPath"]["points"])
            if points.len() < 2 :
                continue

            coordinates = points.coordinates()
            if points.len() == 2 :
                dist = g2dist(coordinates[0], coordinates[1]) * 1000
            else :
                dist = gravityPointDistance(coordinates)
            
            duration = msToMinite(self.locateDuration(doc))
            if duration < 8 :
                print(doc)
            region_duration_list[0].append(dist)
            region_duration_list[1].append(duration)

        return region_duration_list

    def locateDuration(self, doc):
        return doc["placeVisit"]["duration"]["endTimestampMs"] - doc["placeVisit"]["duration"]["startTimestampMs"]
    
    

def msToMinite(timeMs):
    offset = 1000 * 60
    return timeMs / offset

# MongoDBQueryを取得して差分リストを返す
def elementList(segment, element, limit = 0):
    query = { segment + ".simplifiedRawPath" : {"$exists": True}}
    corsor = MongoDBSet().queryMongodb(query, limit)
    collection = GLHCollection(corsor, segment)
    return  [doc[element] for doc in collection.differenceList()]

def distDurationList(segments, elements, limits):
    dist_duration_list = [[],[]]
    for index, segment in enumerate(segments):
        limit = limits[index]
        dist_duration_list[0].append(elementList(segment, elements[0], limit))
        dist_duration_list[1].append(elementList(segment, elements[1], limit))
    return dist_duration_list

def pVSRPSpread():
    query = { "placeVisit.simplifiedRawPath" : {"$exists": True}}
    collection = GLHCollectionPv(MongoDBSet().queryMongodb(query))
    return collection.regionDurationList()

def createFigures(distlists,timelists):
    logScatterFigure(distlists[0], timelists[0], "ActivitySegment")
    logScatterFigure(distlists[1], timelists[1], "PlaceVisit")
    logScatterFigure(distlists[0] + distlists[1], timelists[0] + timelists[1], "FullSegment")

def scatterFigure(distlist, timelist, name, xlabel = "distance[m]", ylabel = "duration[minute]"):
    savepath = "./images/"
    n = "[n = " + str(len(distlist)) + "]"
    fig = plt.figure(dpi=200)
    axis = fig.add_subplot(1, 1, 1, title = name + n, xlabel = xlabel, ylabel = ylabel)
    axis.scatter(distlist, timelist, marker=".")
    fig.savefig(savepath + name + ".png")
    print("Output: " + name + ".png")

def logScatterFigure(distlist, timelist, name, xlabel = "distance[m]", ylabel = "duration[minute]"):
    savepath = "./images/"
    n = "[n = " + str(len(distlist)) + "]"
    fig = plt.figure(dpi=200)

    axis = fig.add_subplot(1, 1, 1, title = name + n, xlabel = xlabel, ylabel = ylabel)
    axis.scatter(distlist, timelist, marker=".")
    axis.set_xscale('log')
    axis.set_yscale('log')

    fig.savefig(savepath + name + ".png")
    print("Output: " + name + ".png")

def fullFigure(distlists,timelists):
    fig = plt.figure()

    fullax = fig.add_subplot(1, 2, 1, title = "Full", xlabel = "distance[km]", ylabel = "duration[minute]")
    fullax.scatter(distlists[0] + distlists[1], timelists[0] + timelists[1], marker=".")
    asax = fig.add_subplot(2, 2, 2, title = "ActivitySegment")
    asax.scatter(distlists[0], timelists[0], marker=".")
    pvax = fig.add_subplot(2, 2, 4, title = "PlaceVisit")
    pvax.scatter(distlists[1],timelists[1], marker=".")
    
    fig.tight_layout()
    fig.savefig("./images/difference.png")
    
if __name__ == '__main__' :

    segments = ["activitySegment", "placeVisit"]
    limits= [0, 0]
    elements = ["dist", "duration"]

    MongoDBSet().stat()

    dist_duration_list = distDurationList(segments, elements, limits)

    createFigures(*dist_duration_list)
    # fullFigure(distlists, timelists)

    region_duration_list = pVSRPSpread()
    #print(boundlyList)

    logScatterFigure(*region_duration_list, "placeVisitSpread")