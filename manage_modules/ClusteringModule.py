# ClusteringModule.py

from lib.GLHMongoDB import OPTICSConstruct
from lib.GLH.Clustering import OPTICSTrajectoryData
from lib.MongoDBSetting import ReachabilityDB


def init_clustering(min_samples = 4):
    data_construction = OPTICSConstruct(min_samples)
    optics_trajectory_data : OPTICSTrajectoryData = data_construction.clustering_obj.clustering

    optics_array = optics_trajectory_data.create_optics_arrays()
    return optics_array

def clustering_and_store_reachability(min_samples = 4) :
    reach_db = ReachabilityDB()

    optics_array = init_clustering(min_samples)
    dicted_data = optics_array.to_dict_list()
    reach_db.insertmany(dicted_data)
