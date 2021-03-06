# GLHMongoDB.py
"""
Assemble GLHLibrary and MongoDBquery, and Management clustring.
"""

from .GLH import *
from .GLH.GLHmodule.geo2 import getBoundsAt
from .GLH.GLHmodule.GeoJSON import PolygonGeojson
from .MongoDBSetting import GLHDB, ReachabilityDB

def get_reachability():
    return ReachabilityDB().reachability_json()


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
    routepath = RoutePath(GLHDB().query({}))
    routepath._create_route_path()
    return routepath.geojson()

def get_viewport(center, zoom, width, height):
    corner = getBoundsAt(center, zoom, [width, height])
    # corner = [[139.53727523803707, 35.6487230630116], [139.55272476196285, 35.66127644371278]]
    polygon = [corner[0],[corner[0][0], corner[1][1]], corner[1], [corner[1][0], corner[0][1]], corner[0]]
    view_port_geojson = PolygonGeojson("view_port", [polygon])
    return view_port_geojson.geojson

class DBSCANConstruct():
    """
    get all trajectory data and create DBSCAN object, set eps and min_samples
    """
    clustering_obj = None
    def __init__(self, eps, min_samples) -> None:
        if self.clustering_obj == None :
            as_srp_collection = GLHDB().assrp_query()
            pv_srp_collection = GLHDB().pvsrp_query()
            DBSCANConstruct.clustering_obj = AllTrajectoryData(as_srp_collection, pv_srp_collection)
            self.set_dbscan(eps, min_samples)
    def set_dbscan(self, eps, min_samples):
        DBSCANConstruct.clustering_obj.dbscan(eps, min_samples)
    def polygon(self):
        return DBSCANConstruct.clustering_obj.cluster_polygon()
    def point(self):
        return DBSCANConstruct.clustering_obj.cluster_point()
class OPTICSConstruct():
    """
    get all trajectory data and create OPTICS object, set min_samples
    eps is set after constructer through set_eps(eps)
    """
    clustering_obj = None
    min_samples = None
    def __init__(self, min_samples) -> None:
        if OPTICSConstruct.clustering_obj == None :
            as_srp_collection = GLHDB().assrp_query()
            pv_srp_collection = GLHDB().pvsrp_query()
            OPTICSConstruct.clustering_obj = AllTrajectoryData(as_srp_collection, pv_srp_collection)
            self.set_optics(min_samples)
        else:
            if OPTICSConstruct.min_samples != min_samples :
                self.set_optics(min_samples)
            else:
                pass

    def set_optics(self, min_samples) -> None:
        OPTICSConstruct.min_samples = min_samples
        OPTICSConstruct.clustering_obj.optics(min_samples)
    def set_eps(self, eps) -> None:
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
        self.collection.trajectory_data()
        return self.collection.exportJson()
    def geojson(self):
        self.collection.trajectory_data()
        return self.collection.exportGeoJson()

class GetGLHAssrp(GetGLHCollection):
    def __init__(self) -> None:
        super().__init__()
    def _get_collection(self):
        return GLHCollectionAsSrp(GLHDB().assrp_query())

class GetGLHAswp(GetGLHCollection):
    def __init__(self) -> None:
        super().__init__()
    def _get_collection(self):
        return GLHCollectionAsWp(GLHDB().aswp_query())

class GetGLHPvsrp(GetGLHCollection):
    def __init__(self) -> None:
        super().__init__()
    def _get_collection(self):
        return GLHCollectionPvSrp(GLHDB().pvsrp_query())

class GetGLHPvloc(GetGLHCollection):
    def __init__(self) -> None:
        super().__init__()
    def _get_collection(self):
        return GLHCollectionPvLoc(GLHDB().pvlocation_query())
