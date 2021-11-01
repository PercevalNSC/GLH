from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import DBSCAN
import numpy as np

from .Plotfigure import coordinatesFigure

class TrajectoryData():
    def __init__(self, trajectorydata: list) -> None:
        self.trajectorydata : np.ndarray = np.array(self.removeNoise(trajectorydata))

    def removeNoise(self, rawdata: list):
        for x in rawdata:
            if 0 in x:
                rawdata.remove(x)
        return rawdata
    def coordinates(self):
        return self.trajectorydata[:, 0:2]
    
    def dbscan(self, eps, min_samples):
        return DBSCANCoodinates(self.coordinates(), eps, min_samples)

class DBSCANCoodinates():
    def __init__(self, coordinates, eps, min_samples) -> None:
        self.coordinates :np.ndarray = coordinates
        self.clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(self.coordinates)
    def labelPoint(self):
        return self._labelGravityPoint(self.labeledCoordinates())
    def labeledCoordinates(self):          
        return [[i, self._specificLabelCoodinates(i)] for i in range(-1, max(self.clustering.labels_))]
    def _labelGravityPoint(self, labelcoordinates):
        result = []
        for l in labelcoordinates:
            if l[0] == -1 :
                continue
            else:
                print(l[1])
                print(np.average(l[1], axis=0).tolist())
                result.extend(np.average(l[1], axis=0).tolist())
        return result
    
    def _specificLabelCoodinates(self, slabel):
        return [[self.coordinates[index]] for index, label in enumerate(self.clustering.labels_) if slabel == label]

    def clusteringFigure(self):
        coordinatesFigure(self.coordinates, "DBSCAN", self.clustering.labels_)
    def clusterstat(self):
        # print(self.clustering.labels_)
        print(max(self.clustering.labels_))


class KNNFindPoint :
    def __init__(self, datasets :list, points: list, size : int = 5) -> None:
        self.datasets = np.array(datasets)
        self.points = np.array(points)
        self.model = self._construct_model(size)
    def _construct_model(self, size):
        knn_model = NearestNeighbors(n_neighbors=size).fit(self.datasets)
        return knn_model.kneighbors(self.points)
    def nearest_neightbors_list(self):
        return [self._nearest_neighbors(indices) for indices in self.model[1]]
    def _nearest_neighbors(self, indices):
        return [list(self.datasets[index]) for index in indices]

