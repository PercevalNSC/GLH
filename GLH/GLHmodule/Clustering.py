# GLHmodule.Clustering.py

from math import inf
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import DBSCAN, OPTICS, cluster_optics_dbscan
from scipy.spatial import ConvexHull
import numpy as np
import heapq
import pprint

from .Plotfigure import coordinatesFigure, reachability_figure, reachability_figure_pure
from .geo2 import distance as g2distance

TOKYO_1LNG = (1.51985 + 1.85225) * 30
TOKYO_1LNG1 = 1.51985 * 60
TOKYO_1LNG2 = 1.85225 * 60

class TrajectoryData():
    def __init__(self, trajectorydata: list) -> None:
        self.trajectorydata :np.ndarray = np.array(self._removeNoise(trajectorydata))

    def _removeNoise(self, rawdata: list):
        for x in rawdata:
            if 0 in x:
                rawdata.remove(x)
        return rawdata
    def coordinates(self):
        return self.trajectorydata[:, 0:2]
    
    def dbscan(self, eps, min_samples):
        print("use old dbscan method")
        return DBSCANCoordinates(self.coordinates(), eps, min_samples)
    def optics(self, min_samples):
        print("use old optics method")
        return OPTICSCoordinates(self.coordinates(), min_samples)
    def to_dbscan(self, eps, min_samples):
        dbscan = DBSCANTrajectoryData(self.trajectorydata.tolist())
        dbscan.clustering_set(eps, min_samples)
        return dbscan
    def to_optics(self, min_samples):
        optics = OPTICSTrajectoryData(self.trajectorydata.tolist())
        optics.clustering_set(min_samples)
        return optics

    def map_scope(self, p1, p2):
        result = []
        for trajectory_set in self.trajectorydata :
            result.append(self._insinde_map(trajectory_set, p1, p2))

    def _insinde_map(self, trajectory_set, p1, p2):
        if (p1[0] < trajectory_set[0] < p2[0]) and (p1[1] < trajectory_set[1] < p2[1]) :
            return trajectory_set
        else :
            return []

class ClusteringTrajectoryData(TrajectoryData):
    def __init__(self, trajectorydata: list) -> None:
        self.trajectorydata = None
        self.clustering :ClusteringCoordinates = None
        super().__init__(trajectorydata)
    
    def clustering_set(self):
        self.clustering = None
        self.labels = None
    
    def labeled_trajectory_list(self):
        labeled_data = [[label, []] for label in range(-1, max(self.labels)+1)]
        for index, label in enumerate(self.labels):
            labeled_list :list = labeled_data[label+1][1]   # ラベルが-1スタートなのでラベルのインデックスをずらす
            labeled_list.append(self.trajectorydata[index].tolist())
        return labeled_data
    def labeled_trajectory_data(self):
        labeled_data = [[label, []] for label in range(-1, max(self.labels)+1)]
        for index, label in enumerate(self.labels):
            labeled_list :list = labeled_data[label+1][1]   # ラベルが-1スタートなのでラベルのインデックスをずらす
            labeled_list.append(self.trajectorydata[index])
        return labeled_data

    def cluster_during(self, labeled_data):
        pass
        
    def cluster_point_td(self):
        return self._label_gravity_point(self.labeled_trajectory_data())
    
    def labeled_coordinates(self):
        return self.clustering.labeled_coordinates()
    def cluster_point_coords(self):
        return self.clustering.cluster_point()
    def cluster_polygon_coords(self):
        return self.clustering.cluster_polygon()
    
    def _label_gravity_point(self, label_coordinates):
        result = []
        for l in label_coordinates:
            if l[0] == -1 :
                continue
            else:
                result.append(np.average(l[1], axis=0).tolist())
        return result

class DBSCANTrajectoryData(ClusteringTrajectoryData):
    def __init__(self, trajectorydata: list) -> None:
        super().__init__(trajectorydata)
    def clustering_set(self, eps, min_samples):
        self.clustering :DBSCANCoordinates = DBSCANCoordinates(self.coordinates(), geography_to_euclid(eps), min_samples)
        self.labels = self.clustering.labels

class OPTICSTrajectoryData(ClusteringTrajectoryData):
    def __init__(self, trajectorydata: list) -> None:
        super().__init__(trajectorydata)
    def clustering_set(self, min_samples):
        self.clustering :OPTICSCoordinates = OPTICSCoordinates(self.coordinates(), min_samples)
    def set_eps(self, eps):
        self.clustering.optics_set_eps(geography_to_euclid(eps))
        self.labels = self.clustering.labels
    def create_optics_arrays(self):
        # 動くが対応はしてない
        return OPTICSArrays(self.trajectorydata, self.clustering.clustering.reachability_, self.clustering.clustering.ordering_)
    def reachability_plot(self):
        self.clustering.reachability_plot()


class ClusteringCoordinates():
    def __init__(self, coordinates) -> None:
        self.coordinates :np.ndarray = coordinates
        self.clustering = None
        self.labels = None
    def labeled_coordinates(self):
        labels = self.labels
        labels_coordinates = [[label, []] for label in range(-1, max(labels)+1)]
        for index, label in enumerate(labels):
            label_coordinates :list = labels_coordinates[label+1][1]
            label_coordinates.append(self.coordinates[index])
        return labels_coordinates
    def cluster_polygon(self):
        result = []
        for labelcoordinates in self.labeled_coordinates() :
            if labelcoordinates[0] == -1 :
                continue
            else:
                polygon = np.array(labelcoordinates[1])
                result.append(self.polygon_convhull(polygon))
        return result

    def polygon_convhull(self, polygon :np.ndarray):
        """
        ポリゴンの凸包を求め，座標のリストを返す
        """
        # 重複を除いて，3点に満たないときreturn
        polygon = np.unique(polygon, axis=0)
        if polygon.size < 6 :
            return []
        hull = ConvexHull(polygon)
        points = hull.points
        conv_points = points[hull.vertices]
        return conv_points.tolist()

    def cluster_point(self):
        return self._labelGravityPoint(self.labeled_coordinates())
    def _labelGravityPoint(self, labelcoordinates):
        result = []
        # TODO: labelcoordinates[1:]
        for l in labelcoordinates:
            if l[0] == -1 :
                continue
            else:
                result.append(np.average(l[1], axis=0).tolist())
        return result
    
    def gravity_point_distance(self, points :np.ndarray):
        max_dist = 0
        gravity_point = np.average(points, axis=0)

        for point in points :
            dist = g2distance(point, gravity_point) * 1000
            max_dist = max(max_dist, dist * 2)
        return [gravity_point, max_dist]

    def clusteringFigure(self):
        coordinatesFigure(self.coordinates, "Clustering", self.clustering.labels_)
    def clusterstat(self):
        # print(self.clustering.labels_)
        print(max(self.clustering.labels_))

class DBSCANCoordinates(ClusteringCoordinates):
    def __init__(self, coordinates, eps, min_samples) -> None:
        super().__init__(coordinates)
        self._clustering_construct(eps, min_samples)
    def _clustering_construct(self, eps, min_samples):
        print("Starting DBSCAN")
        self.clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(self.coordinates)
        self.labels = self.clustering.labels_

class OPTICSCoordinates(ClusteringCoordinates):
    def __init__(self, coordinates, min_samples) -> None:
        super().__init__(coordinates)
        self._clustering_construct(min_samples)
    def _clustering_construct(self, min_samples):
        print("Starting OPTICS")
        self.clustering = OPTICS(min_samples=min_samples).fit(self.coordinates)
    def optics_set_eps(self, eps):
        print("OPTICS set: eps=", eps)
        self.labels = cluster_optics_dbscan(reachability=self.clustering.reachability_,
                                   core_distances=self.clustering.core_distances_,
                                   ordering=self.clustering.ordering_, eps=eps)
    def crate_optics_arrays(self):
        return OPTICSArrays(self.coordinates, self.clustering.reachability_, self.clustering.ordering_)
    def reachability_plot(self):
        space = np.arange(len(self.coordinates))
        reachability = self.clustering.reachability_[self.clustering.ordering_]
        reachability_figure(space, reachability, "reachability_plot")

class OPTICSArrays :
    """
    Data: 要素内の3番目以降の情報を使わず，座標データだけ使用する
    """
    plot_count = 0
    def __init__(self, data :np.ndarray, reachability :np.ndarray, ordering :np.ndarray) -> None:
        self.data = data
        self.reachability = reachability
        self.ordering = ordering
        if len(ordering) == 0 :
            self.ordering = self._init_order() 
        else:
            self._ordered_data()

    def map_scope(self, p1, p2):
        # Order(2n)
        print("Map scope by", p1, p2)
        scope_data = []
        scope_reachability = []
        error_order = []
        error_reachability = []
        #flag = 0
        skipcount = 0
        order_offset = 0
        for i in range(len(self.data)):
            if skipcount > 0 :
                skipcount -= 1
                continue

            if self._is_in_map(p1, p2, self.data[i]):
                scope_data.append(self.data[i])
                scope_reachability.append(self.reachability[i])
                #flag = 0
            else :
                temp = self.not_in_map(i, p1, p2, order_offset)
                scope_data.append(temp[0])
                scope_reachability.append(temp[1])
                error_order.append(temp[2])
                error_reachability.append(temp[3])
                skipcount = temp[4]
                order_offset += skipcount
                
        return ScopedOPTICSArrays(scope_data, scope_reachability,[], error_order, error_reachability)
    
    # マップにない区間のデータの処理．更新したskipcountを返す．
    def not_in_map(self, start_index, p1, p2, order_offset):
        """
        return [dammy_data, dammy_reachability, error_order, error_reachability, skipcount]
        """
        i = start_index
        maxreachability = 0
        # is_in_mapがTrueになるまでiを進める．その間の最大のreachabilityをとる．
        for i in range(start_index, len(self.data), 1):
            if self._is_in_map(p1, p2, self.data[i]) :
                break
            else :
                maxreachability = max(maxreachability, self.reachability[i])
    
        skipcount = i - start_index - 1
        #print("i:", i, "index:", start_index, skipcount)
        return [np.zeros(3), 0, self.ordering[start_index] - order_offset, maxreachability, skipcount]


    def clustering_boundary(self):
        boundly = []
        for i in range(len(self.reachability)-1):
            if self.reachability[i] > self.reachability[i-1] :
                boundly.append(self.reachability[i])
        return boundly


    def reachability_plot(self, eps = 0):
        if self._consistency() :
            reachability_figure_pure(self.ordering, self.reachability, "reachability_in_OPTICSArrays" + str(OPTICSArrays.plot_count), eps)
            OPTICSArrays.plot_count += 1
        else:
            print("consistency fail in reachabilityplot")
            self.status()

    def data_plot(self):
        #scatterFigure(self.coordinates[:,0], self.coordinates[:, 1], "Data_Plot" + str(OPTICSArrays.plot_count), "Longtitude", "Latitude")
        name = "Data_Plot" + str(OPTICSArrays.plot_count)
        coordinatesFigure(self._remove_noise(self.data), name, 'b' )
        OPTICSArrays.plot_count += 1

    def reachability_resolution(self, cluster_n :int) -> int:
        # print(heapq.nlargest(3, reachability))
        largest_boundary = heapq.nlargest(cluster_n+1, self.clustering_boundary())
        #print(largest_boundary)
        if largest_boundary[0] == inf :
            return largest_boundary[1] - largest_boundary[-1]
        else :
            return largest_boundary[0] - largest_boundary[-2]
    
    def continuous_resolution_print(self, cluster_n :int):
        for i in range(2, cluster_n+1, 1):
            print("i:",i,"resolution:", self.reachability_resolution(i))
        
        

    def status(self):
        print("Data:", self.data, "len:", len(self.data))
        print("Reachability:", self.reachability, "len:", len(self.reachability))
        print("Ordering:", self.ordering, "len:", len(self.ordering))

    def print(self):
        return "Data:" + str(self.data) + "\nReachability:" + str(self.reachability) + "\nOrdering:" +  str(self.ordering)

    def _remove_noise(self, data):
        temp = []
        for d in data:
            if d[0] != 0 or d[1] != 0:
                temp.append(d)
        return temp

    def _consistency(self):
        if len(self.data) == len(self.reachability) and len(self.data) == len(self.ordering):
            return True
        else :
            return False

    def _is_in_map(self, p1, p2, cp):
        if (cp[0] < p1[0]) | (p2[0] < cp[0]) | (cp[1] < p1[1]) | (p2[1] < cp[1]):
            return False
        else :
            return True

    def _init_order(self):
        return np.array(list(range(len(self.reachability))))
    
    def _ordered_data(self):
        print("Ordering Data")
        self.data = self._ordered_list(self.data, self.ordering)
        self.reachability = self._ordered_list(self.reachability, self.ordering)
        self.ordering = self._init_order()

    def _ordered_list(self, target_list, order_list):
        if len(target_list) != len(order_list):
            print("Invaild length: target and order list")
            return target_list
        result = list(range(len(order_list)))
        for index, order in enumerate(order_list):
            result[order] = target_list[index]
        return result
    
    def _pure_data(self):
        return np.zeros(len(self.data))

    # remove_index break data consistency. after used, do _init_order()
    def _remove_index(self, index :int):
        self.data = np.delete(self.data, index, 0)
        self.reachability = np.delete(self.reachability, index, 0)

class ScopedOPTICSArrays(OPTICSArrays):
    def __init__(self, data: np.ndarray, reachability: np.ndarray, ordering: np.ndarray, error_order=np.array([]), error_reachability=np.array([])) -> None:
        super().__init__(data, reachability, ordering)
        self.error_order = error_order
        self.error_reachability = error_reachability
    
    def reachability_plot(self, eps = 0):
        if self._consistency() :
            reachability_figure(self.ordering, self.reachability, self.error_order, self.error_reachability, "reachability_in_OPTICSArrays" + str(OPTICSArrays.plot_count), eps)
            OPTICSArrays.plot_count += 1
        else:
            print("consistency fail in reachabilityplot")
            self.status()


class KNNFindPoint :
    def __init__(self, datasets :list, points: list, size :int = 5) -> None:
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


class LabeledTrajectoryData():
    def __init__(self, labeled_trajectory_data) -> None:
        self.labeled_trajectory_data = labeled_trajectory_data
    
    def cluster_term(self) -> list:
        label_term = []
        for cluster_trajectory_data in self.labeled_trajectory_data :
            label = cluster_trajectory_data[0]
            trajectory_data = cluster_trajectory_data[1]
            term = self._trajectory_data_term(trajectory_data)
            label_term.append([label, term])
        return label_term
    
    def _trajectory_data_term(self, trajectory_data):
        timestamp_min_max = [trajectory_data[0][2], trajectory_data[0][2]]
        for trajectory_set in trajectory_data :
            timestamp_min_max[0] = min(timestamp_min_max[0], trajectory_set[2])
            timestamp_min_max[1] = max(timestamp_min_max[1], trajectory_set[2])
        return timestamp_min_max[1] - timestamp_min_max[0]

def euclid_to_geography(euclid_dist):
    return euclid_dist * TOKYO_1LNG #(km)

def geography_to_euclid(geography_dist):
    # input (km)
    return geography_dist / TOKYO_1LNG
