import numpy as np
from  sklearn.cluster import DBSCAN
import pprint

from libraries.MongoDBSetting import MongoDBSet
from libraries.GLH import AllTrajectoryData, GLHTrajectoryData
from libraries.Plotfigure import coordinatesFigure

class TrajectoryData():
    def __init__(self, trajectorydata: list) -> None:
        self.trajectorydata = np.array(self.removeNoise(trajectorydata))

    def removeNoise(self, rawdata: list):
        for x in rawdata:
            if 0 in x:
                rawdata.remove(x)
        return rawdata
    def coordinates(self):
        return self.trajectorydata[:, 0:2]
    
class DBSCANCoodinates():
    def __init__(self, coordinates) -> None:
        self.coordinates = coordinates
        self.clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(self.coordinates)
    def labelPoint(self):
        labelcoordinates = LabelCoordinates(self._labelCoordinates())
        return labelcoordinates.gravityPoint()
    def _labelCoordinates(self):
        labelcoordinates = []
        for i in range(-1, max(self.clustering.labels_)):
            one_label_coordinates = [list(self.coordinates[index]) for index, label in enumerate(self.clustering.labels_) if i == label]
            labelcoordinates.append([i, one_label_coordinates])              
        return labelcoordinates

    def clusteringFigure(self):
        coordinatesFigure(self.coordinates, "DBSCAN", self.clustering.labels_)
    def clusterstat(self):
        # print(self.clustering.labels_)
        print(max(self.clustering.labels_))

class LabelCoordinates():
    def __init__(self, labelcoordinates) -> None:
        self.labelcoordinates = labelcoordinates
    def gravityPoint(self):
        result = []
        for l in self.labelcoordinates:
            if l[0] == -1 :
                continue
            else:
                sum = [0.0, 0.0]
                for c in l[1]:
                    sum[0] += c[0]
                    sum[1] += c[1]
                gp = [x/len(l[1]) for x in sum]
                result.append(gp)
        return result

if __name__ == "__main__":
    eps = 0.0001
    min_samples = 4
    as_srp_collection = MongoDBSet().asSrpQuery()
    pv_srp_collection = MongoDBSet().pvSrpQuery()

    std = AllTrajectoryData(as_srp_collection, pv_srp_collection)
    print(std.dbscan(eps, min_samples))
