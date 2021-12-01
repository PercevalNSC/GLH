from GLH import *
from GLH.GLHmodule.Clustering import OPTICSCoordinates
from Setting.MongoDBSetting import MongoDBSet

"""
Assemble GLHLibrary and MongoDBquery, and Management clustring.
"""

def get_dbscan_point(eps, min_samples):
    std = DBSCANConstruct(eps, min_samples)
    return std.point()
def get_dbscan_polygon(eps, min_samples):
    std = DBSCANConstruct(eps, min_samples)
    return std.polygon()
def get_optics_point(eps, min_samples):
    std = OPTICSConstruct(min_samples)
    std.set_eps(eps)
    return std.point()
def get_optics_polygon(eps, min_samples):
    std = OPTICSConstruct(min_samples)
    std.set_eps(eps)
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
            self.set_dbscan(eps, min_samples)
    def set_dbscan(self, eps, min_samples):
        self.clustering_obj.dbscan(eps, min_samples)
    def polygon(self):
        return self.clustering_obj.cluster_polygon()
    def point(self):
        return self.clustering_obj.cluster_point()
class OPTICSConstruct():
    clustering_obj = None
    min_samples = None
    def __init__(self, min_samples) -> None:
        if OPTICSConstruct.clustering_obj == None :
            as_srp_collection = MongoDBSet().assrp_query()
            pv_srp_collection = MongoDBSet().pvsrp_query()
            OPTICSConstruct.clustering_obj = AllTrajectoryData(as_srp_collection, pv_srp_collection)
            self.set_optics(min_samples)
        else:
            if OPTICSConstruct.min_samples != min_samples :
                self.set_optics(min_samples)
            else:
                pass

    def set_optics(self, min_samples):
        OPTICSConstruct.min_samples = min_samples
        OPTICSConstruct.clustering_obj.optics(min_samples)
    def set_eps(self, eps):
        OPTICSConstruct.clustering_obj.optics_set_eps(eps)
    def labeled_trajectory_data(self):
        return OPTICSConstruct.clustering_obj.labeled_trajectory_data()
    def polygon(self):
        return OPTICSConstruct.clustering_obj.cluster_polygon()
    def point(self):
        return OPTICSConstruct.clustering_obj.cluster_point()

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