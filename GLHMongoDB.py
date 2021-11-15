from GLH import *
from Setting.MongoDBSetting import MongoDBSet


def get_dbscan_point(eps, min_samples):
    as_srp_collection = MongoDBSet().assrp_query()
    pv_srp_collection = MongoDBSet().pvsrp_query()
    std = AllTrajectoryData(as_srp_collection, pv_srp_collection)
    return std.dbscan_point(eps, min_samples)
def get_dbscan_polygon(eps, min_samples):
    as_srp_collection = MongoDBSet().assrp_query()
    pv_srp_collection = MongoDBSet().pvsrp_query()
    std = AllTrajectoryData(as_srp_collection, pv_srp_collection)
    return std.dbscan_polygon(eps, min_samples)
def route_path():
    routepath = RoutePath(MongoDBSet().query({}))
    routepath.createRoutePath()
    return routepath.exportGeoJson()

class GetGLHCollection():
    def __init__(self) -> None:
        self.collection :GLHCollection = self._get_collection()
    
    def _get_collection(self):
        pass
    def json(self):
        self.collection.trajectoryList()
        return self.collection.exportJson()
    def geojson(self):
        self.collection.trajectoryList()
        return self.collection.exportGeoJson()

class GetGLHAssrp(GetGLHCollection):
    def __init__(self) -> None:
        super().__init__()
    def _get_collection(self):
        return GLHCollectionAsSrp(MongoDBSet().assrp_query())

class GetGLHAswp(GetGLHCollection):
    def __init__(self) -> None:
        super().__init__()
    def _get_collection(self):
        return GLHCollectionAsWp(MongoDBSet().aswp_query())

class GetGLHPvsrp(GetGLHCollection):
    def __init__(self) -> None:
        super().__init__()
    def _get_collection(self):
        return GLHCollectionPvSrp(MongoDBSet().pvsrp_query())

class GetGLHPvloc(GetGLHCollection):
    def __init__(self) -> None:
        super().__init__()
    def _get_collection(self):
        return GLHCollectionPvLoc(MongoDBSet().pvlocation_query())

if __name__=="__main__":
    print("neko")