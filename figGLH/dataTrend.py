from pymongo import MongoClient
import matplotlib.pyplot as plt
from geo2 import distance as g2dist 

def pointsDifference(points):
    result = []

    for index in range(len(points)-1):
        result.append({"dist": docDistance(points[index], points[index+1]),
            "duration": docDuration(points[index], points[index+1])})
        
    return result

def docDistance(doc1, doc2):
    coord1 = [doc1["latE7"], doc1["lngE7"]]
    coord2 = [doc2["latE7"], doc2["lngE7"]]
    return g2dist(coord1, coord2)
def docDuration(doc1, doc2):
    offset = 1000 * 60 # convert to minite]
    duration = abs(doc2["timestampMs"] - doc1["timestampMs"] )
    return duration / offset

def differenceList(segment):
    result = []
    query = { segment + ".simplifiedRawPath" : {"$exists": True}}
    for doc in queryMongodb(query):
        points = doc[segment]["simplifiedRawPath"]["points"]
        diff = pointsDifference(points)
        result.extend(diff)

    return result

def elementList(segment, element):
    result = []
    for doc in differenceList(segment) :
        result.append(doc[element])
    return result

def queryMongodb(query):
    with MongoClient("mongodb://127.0.0.1:27017") as client:
        glh_db = client.glh_db
        glh_clct = glh_db.glh_clct_2
        return glh_clct.find(query)
    
def createFigures(distlists,timelists):
    createFigure(distlists[0], timelists[0], "ActivitySegment")
    createFigure(distlists[1], timelists[1], "PlaceVisit")
    createFigure(distlists[0] + distlists[1], timelists[0] + timelists[1], "FullSegment")

def createFigure(distlist, timelist, name, xlabel = "distance[km]", ylabel = "duration[minite]"):
    savepath = "./images/"
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, title = name, xlabel = xlabel, ylabel = ylabel)
    ax.scatter(distlist, timelist, marker=".")
    fig.savefig(savepath + name + ".png")

def fullFigure(distlists,timelists):
    fig = plt.figure()

    # full | As
    # full | Pv
    fullax = fig.add_subplot(1, 2, 1, title = "Full", xlabel = "distance[km]", ylabel = "duration[minite]")
    fullax.scatter(distlists[0] + distlists[1], timelists[0] + timelists[1], marker=".")
    asax = fig.add_subplot(2, 2, 2, title = "ActivitySegment")
    asax.scatter(distlists[0], timelists[0], marker=".")
    pvax = fig.add_subplot(2, 2, 4, title = "PlaceVisit")
    pvax.scatter(distlists[1],timelists[1], marker=".")
    
    fig.tight_layout()
    fig.savefig("./images/difference.png")

    
if __name__ == '__main__' :

    segment = ["activitySegment", "placeVisit"]
    element = ["dist", "duration"]
    distlists = []
    timelists = []

    for seg in segment:

        distlists.append(elementList(seg, element[0]))
        timelists.append(elementList(seg, element[1]))

    # createFigures(distlists, timelists)
    fullFigure(distlists, timelists)