from Setting.MongoDBSetting import MongoDBSet
from GLH.GLH import AllTrajectoryData

if __name__ == "__main__":
    eps = 0.01
    min_samples = 4
    as_srp_collection = MongoDBSet().assrp_query()
    pv_srp_collection = MongoDBSet().pvsrp_query()

    std = AllTrajectoryData(as_srp_collection, pv_srp_collection)
    print(std.dbscan(eps, min_samples))
