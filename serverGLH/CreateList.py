class DocumentLngLatList :
    # 1つのドキュメントについて緯度経度のリストを返す
    def __init__(self, document):
        self.document = document
    
    def docAsSrpList(self):
        return self.makingList("activitySegment" , "simplifiedRawPath", "points")
    def docAsWpPList(self):
        return self.makingList("activitySegment", "waypointPath", "waypoints")
    def docPvSrpList(self):
        return self.makingList("placeVisit", "simplifiedRawPath", "points")
    
    def makingList(self,segment, value1, value2):
        lnglatlist = []
        for item in self.document[segment][value1][value2] :
            lnglatlist.append([item["lngE7"], item["latE7"]])
        return lnglatlist

class MakingLngLatList :
    # １つのコレクションに対し、ドキュメントの緯度経度リストから緯度経度リストを作成する
    def __init__(self, collection):
        self.collection = collection
    def clctAsSrpList(self):
        lnglatlists = []
        for document in self.collection:
            dllObj = DocumentLngLatList(document)
            dll = dllObj.docAsSrpList()
            for i in dll:
                lnglatlists.append(i)
        return lnglatlists

if __name__ == "__main__" :
    test_item = {'_id': '60e1141eeb127c56412ef5b5', 'activitySegment': {'simplifiedRawPath': {'points': [{'latE7': 35.6657028, 'lngE7': 139.5432739, 'timestampMs': 1525071569400, 'accuracyMeters': 20}, {'latE7': 35.6597595, 'lngE7': 139.5408325, 'timestampMs': 1525071815400, 'accuracyMeters': 11}, {'latE7': 35.6570778, 'lngE7': 139.5430298, 'timestampMs': 1525071940700, 'accuracyMeters': 22}]}}}

    test_list = DocumentLngLatList(test_item)
    list = test_list.docAsSrpList()

    print(test_list)