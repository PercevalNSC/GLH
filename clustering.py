from Setting.MongoDBSetting import MongoDBSet
from GLH.GLH import AllTrajectoryData

if __name__ == "__main__":
    eps = 0.01
    min_samples = 4
    as_srp_collection = MongoDBSet().assrp_query()
    pv_srp_collection = MongoDBSet().pvsrp_query()

    atd = AllTrajectoryData(as_srp_collection, pv_srp_collection)
    atd.dbscan(eps, min_samples)
    print(atd.clustering.labeled_trajectory_data())
    print(atd.clustering.labeled_coordinates())
    print(atd.clustering.cluster_point_td())
    print(atd.clustering.cluster_point_coords())

