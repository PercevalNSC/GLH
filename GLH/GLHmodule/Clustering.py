from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import DBSCAN
from scipy.spatial import ConvexHull
import numpy as np
import pprint

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
    def label_polygon(self):
        result = []
        for labelcoordinates in self.labeledCoordinates() :
            if labelcoordinates[0] == -1 :
                continue
            else:
                polygon = np.array(labelcoordinates[1])
                result.append(self.polygon_convhull(polygon))
        return result

    def polygon_convhull(self, polygon):
        polygon = np.unique(polygon, axis=0)
        if polygon.size < 6 :
            return []
        print(polygon)
        hull = ConvexHull(polygon)
        points = hull.points
        conv_points = points[hull.vertices]
        return conv_points.tolist()

    def labelPoint(self):
        return self._labelGravityPoint(self.labeledCoordinates())
    def labeledCoordinates(self):
        labeled_coords = [[label, []] for label in range(-1, max(self.clustering.labels_)+1)]
        for index, label in enumerate(self.clustering.labels_):
            labeled_coords[label+1][1].append(self.coordinates[index])
        return labeled_coords
    def _labelGravityPoint(self, labelcoordinates):
        result = []
        # TODO: labelcoordinates[1:]
        for l in labelcoordinates:
            if l[0] == -1 :
                continue
            else:
                result.append(np.average(l[1], axis=0).tolist())
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

