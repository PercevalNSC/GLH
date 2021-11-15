from sklearn import cluster
from GLH import *
from GLH.GLHmodule import Clustering
from Setting.MongoDBSetting import MongoDBSet

def get_dbscan_point(eps, min_samples):
    std = DBSCANConstruct(eps, min_samples)
    return std.point()
def get_dbscan_polygon(eps, min_samples):
    std = DBSCANConstruct(eps, min_samples)
    return std.polygon()
def route_path():
    routepath = RoutePath(MongoDBSet().query({}))
    routepath.createRoutePath()
    return routepath.exportGeoJson()

class DBSCANConstruct():
    clustering_obj = None
    def __init__(self, eps, min_samples) -> None:
        if self.clustering_obj == None :
            as_srp_collection = MongoDBSet().assrp_query()
            pv_srp_collection = MongoDBSet().pvsrp_query()
            self.clustering_obj = AllTrajectoryData(as_srp_collection, pv_srp_collection)
            self.clustering_obj.dbscan(eps, min_samples)
    def polygon(self):
        return self.clustering_obj.dbscan_polygon()
    def point(self):
        return self.clustering_obj.dbscan_point()

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