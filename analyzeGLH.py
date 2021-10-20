import libraries.Plotfigure as pf
from libraries.MongoDBSetting import MongoDBSet
import libraries.GLH as GLH
    
# MongoDBQueryを取得して差分リストを返す
def elementList(segment, element, limit = 0):
    query = { segment + ".simplifiedRawPath" : {"$exists": True}}
    corsor = MongoDBSet().query(query, limit)
    collection = GLH.GLHCollection(corsor, segment, "", "") # differenceListはelementを使用しないのでダミーで渡す
    return  [doc[element] for doc in collection.differenceList()]

def distDurationList(segments, elements, limits):
    dist_duration_list = [[],[]]
    for index, segment in enumerate(segments):
        limit = limits[index]
        dist_duration_list[0].append(elementList(segment, elements[0], limit))
        dist_duration_list[1].append(elementList(segment, elements[1], limit))
    return dist_duration_list

def pVSRPSpread():
    collection = GLH.GLHCollectionPvSrp(MongoDBSet().pvSrpQuery())
    return collection.regionDurationList()
  
if __name__ == '__main__' :

    segments = ["activitySegment", "placeVisit"]
    limits= [0, 0]
    elements = ["dist", "duration"]

    MongoDBSet().stat()

    dist_duration_list = distDurationList(segments, elements, limits)

    pf.createFigures(*dist_duration_list)
    # fullFigure(distlists, timelists)

    region_duration_list = pVSRPSpread()
    #print(boundlyList)

    pf.logScatterFigure(*region_duration_list, "placeVisitSpread")