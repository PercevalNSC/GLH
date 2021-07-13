class DocumentLatLngList :
    # 1つのドキュメントについて緯度経度のリストを返す
    def __init__(self, document):
        self.document = document
    
    def asAspList(self):
        latlnglist = []
        for item in self.document["activitySegment"]["simplifiedRawPath"]["points"] :
            latlnglist.append([item["lngE7"], item["latE7"]])
        return latlnglist
    def asWpPList(self):
        latlnglist = []
        for item in self.document["activitySegment"]["waypointPath"]["waypoints"] :
            latlnglist.append([item["lngE7"], item["latE7"]])
        return latlnglist

class MakingLatLngList :
    # １つのコレクションに対し、ドキュメントのリストから緯度経度リストを作成する
    def __init__(self, collection):
        self.collection = collection
        self.latlnglists = []
    def makinglist(self):
        for document in self.collection:
            dllobj = DocumentLatLngList(document)
            dll = dllobj.asAspList()
            for i in dll:
                self.latlnglists.append(i)

if __name__ == "__main__" :
    test_item = {'_id': '60e1141eeb127c56412ef5b5', 'activitySegment': {'simplifiedRawPath': {'points': [{'latE7': 35.6657028, 'lngE7': 139.5432739, 'timestampMs': 1525071569400, 'accuracyMeters': 20}, {'latE7': 35.6597595, 'lngE7': 139.5408325, 'timestampMs': 1525071815400, 'accuracyMeters': 11}, {'latE7': 35.6570778, 'lngE7': 139.5430298, 'timestampMs': 1525071940700, 'accuracyMeters': 22}]}}}

    test_list = DocumentLatLngList(test_item)