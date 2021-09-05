from pymongo import MongoClient
import matplotlib.pyplot as plt


def listDifference(points):
    assert len(points) > 0, "points is None"
    return list(map((lambda x: x - points[0]), points))[1:]

def pointsDifference(points):
    result = points
    indexes = ["latE7", "lngE7", "timestampMs"]

    for index in indexes:
        diff = result[0][index]
        for p in result:
            p[index] = p[index] - diff
     
    return result[1:]

def differenceList(segment):
    result = []

    query = { segment + ".simplifiedRawPath" : {"$exists": True}}
    for doc in queryMongodb(query):
        points = doc[segment]["simplifiedRawPath"]["points"]
        diff = pointsDifference(points)
        result.extend(diff)

    return result

def docDistance(doc):
    return (doc["latE7"]**2 + doc["lngE7"]**2)
def docDuration(doc):
    offset = 1000 * 60 # convert to minite
    return doc["timestampMs"] / offset


def queryMongodb(query):
    with MongoClient("mongodb://127.0.0.1:27017") as client:
        glh_db = client.glh_db
        glh_clct = glh_db.glh_clct_2
        return glh_clct.find(query)
    
def createFigures(distlists,timelists):
    createFigure(distlists[0], timelists[0], "ActivitySegment")
    createFigure(distlists[1], timelists[1], "PlaceVisit")
    createFigure(distlists[0] + distlists[1], timelists[0] + timelists[1], "FullSegment")

def createFigure(distlist, timelist, name, xlabel = "distance[]", ylabel = "duration[minite]"):
    savepath = "./images/"
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, title = name, xlabel = xlabel, ylabel = ylabel)
    ax.scatter(distlist, timelist, marker=".")
    fig.savefig(savepath + name + ".png")

def fullFigure(distlists,timelists):
    fig = plt.figure()

    # full | As
    # full | Pv
    fullax = fig.add_subplot(1, 2, 1, title = "Full", xlabel = "distance[]", ylabel = "duration[minite]")
    fullax.scatter(distlists[0] + distlists[1], timelists[0] + timelists[1], marker=".")
    asax = fig.add_subplot(2, 2, 2, title = "ActivitySegment")
    asax.scatter(distlists[0], timelists[0], marker=".")
    pvax = fig.add_subplot(2, 2, 4, title = "PlaceVisit")
    pvax.scatter(distlists[1],timelists[1], marker=".")
    
    fig.tight_layout()
    fig.savefig("difference.png")

if __name__ == '__main__' :

    segment = ["activitySegment", "placeVisit"]
    distlists = []
    timelists = []

    for seg in segment:
        distlist = []
        timelist = []

        for doc in differenceList(seg) :
            distlist.append(docDistance(doc))
            timelist.append(docDuration(doc))

        # print([docDistance(doc) for doc in difflist])
        
        distlists.append(distlist)
        timelists.append(timelist)

    createFigures(distlists, timelists)
