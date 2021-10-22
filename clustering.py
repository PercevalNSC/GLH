import numpy as np
from  sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

from libraries.MongoDBSetting import MongoDBSet
from libraries.GLH import GLHTrajectoryData
from libraries.Plotfigure import coordinatesFigure

class TrajectoryData():
    def __init__(self, trajectorydata: list) -> None:
        self.trajectorydata = np.array(trajectorydata)
    
    def coordinates(self):
        return self.trajectorydata[:, 0:2]
    def dbscan(self, seteps, set_min_samples):
        print(seteps, set_min_samples)
        self.clusteringobj = DBSCAN(eps=seteps, min_samples=set_min_samples).fit(self.coordinates())
    def clusteringfigure(self):
        coordinatesFigure(self.coordinates(), "DBSCAN", self.clusteringobj.labels_)

if __name__ == "__main__":
    eps = 0.001
    min_samples = 4
    as_srp_collection = MongoDBSet().asSrpQuery()
    pv_srp_collection = MongoDBSet().pvSrpQuery()

    dataobj = GLHTrajectoryData()
    dataobj.allTrajectryData(as_srp_collection, pv_srp_collection)
    dataobj.exportFigure()

    trajectrydata = TrajectoryData(dataobj.trajetorydata)
    trajectrydata.dbscan(eps, min_samples)
    trajectrydata.clusteringfigure()