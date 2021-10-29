from libraries.MongoDBSetting import MongoDBSet
from libraries.GLH import AllTrajectoryData

if __name__ == "__main__":
    eps = 0.01
    min_samples = 4
    as_srp_collection = MongoDBSet().asSrpQuery()
    pv_srp_collection = MongoDBSet().pvSrpQuery()

    std = AllTrajectoryData(as_srp_collection, pv_srp_collection)
    print(std.dbscan(eps, min_samples))
