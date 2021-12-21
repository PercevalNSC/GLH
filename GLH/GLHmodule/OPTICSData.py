import numpy as np
from sklearn import cluster
from .Plotfigure import reachability_figure, out_reachability_figure, ordered_coordinate_figure, resolution_plot
import heapq
from math import inf

from .geo3 import euclid_to_geography

class OPTICSArrays :
    """
    Data: 要素内の3番目以降の情報を使わず，座標データだけ使用する
    """
    plot_count = 0
    def __init__(self, data: list, reachability: list, ordering: list) -> None:
        if max(ordering) == len(ordering)-1:
            print("OPTICSArray: Ordering mode")
            self.data = self._ordered_list(data, ordering)
            self.reachability = self._geography_reachability(self._ordered_list(reachability, ordering))
            #self.ordering = self._init_order()
            self.ordering = self._init_order()
        else :
            print("OPTICSArray: Pre-ordered mode")
            self.data = data
            self.reachability = reachability
            self.ordering = ordering

    def map_scope(self, p1, p2):
        # Order(2n)
        print("Map scope by", p1, p2)
        scope_data = []
        scope_reachability = []
        scope_order = []
        error_order = []
        error_reachability = []
        skipcount = 0
        for i in range(len(self.data)):
            #print("data:", self.data[i], "skipcount:", skipcount)
            if skipcount > 0 :
                skipcount -= 1
                continue

            if self._is_in_map(p1, p2, self.data[i]):
                scope_data.append(self.data[i])
                scope_reachability.append(self.reachability[i])
                
            else :
                maxreach, skipcount = self._not_in_map(i, p1, p2)
                scope_data.append(np.zeros(3))
                scope_reachability.append(0)
                error_order.append(self.ordering[i])
                error_reachability.append(maxreach)
            scope_order.append(self.ordering[i])
                
        return ScopedOPTICSArrays(scope_data, scope_reachability, scope_order, error_order, error_reachability)
    
    # マップにない区間のデータの処理．更新したskipcountを返す．
    def _not_in_map(self, start_index, p1, p2):
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
        return [maxreachability, skipcount]


    def clustering_boundary(self):
        boundly = []
        for i in range(len(self.reachability)-1):
            if self.reachability[i] > self.reachability[i-1] :
                boundly.append(self.reachability[i])
        return boundly

    def reachability_plot(self, eps = 0):
        if self._consistency() :
            print("Reachability Plot")
            space = list(range(len(self.reachability)))
            reachability_figure(space, self.reachability, "reachability_in_OPTICSArrays" + str(OPTICSArrays.plot_count), eps)
            OPTICSArrays.plot_count += 1
        else:
            print("consistency fail in reachabilityplot")
            self.status()
    
    def _geography_reachability(self, euclid_reachability):
        return [euclid_to_geography(euclid_reach) for euclid_reach in euclid_reachability]

    def data_plot(self):
        print("Data Plot ...")
        name = "Data_Plot" + str(OPTICSArrays.plot_count)
        #coordinatesFigure(self._remove_noise(self.data), name, 'b' )
        ordered_coordinate_figure(self._remove_noise(self.data), name)
        OPTICSArrays.plot_count += 1

    def reachability_resolution(self, cluster_n :int) -> int:
        # print(heapq.nlargest(3, reachability))
        largest_boundary = heapq.nlargest(cluster_n+1, self.clustering_boundary())
        #print(largest_boundary)
        if largest_boundary[0] == inf :
            return largest_boundary[1] - largest_boundary[-1]
        else :
            return largest_boundary[0] - largest_boundary[-2]
    
    def continuous_resolution(self, cluster_ns :int):
        result = [[], []]
        for i in range(2, cluster_ns+1, 1):
            resolution = self.reachability_resolution(i)
            result[0].append(i)
            result[1].append(resolution)
        return result
           
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

    def _ordered_list(self, target_list, order_list):
        if len(target_list) != len(order_list):
            print("Invaild length: target and order list")
            return target_list
        result = []
        for order in order_list :
            result.append(target_list[order])
        return np.array(result)

    def _pure_data(self):
        return np.zeros(len(self.data))

    # remove_index break data consistency. after used, do _init_order()
    def _remove_index(self, index :int):
        self.data = np.delete(self.data, index, 0)
        self.reachability = np.delete(self.reachability, index, 0)

class ScopedOPTICSArrays(OPTICSArrays):
    def __init__(self, data: list, reachability: list, ordering: list, error_order: list, error_reachability: list) -> None:
        super().__init__(data, reachability, ordering)
        self.out_order = error_order
        self.out_reachability = error_reachability
    
    def resize_out_reachability(self, out_reachability, reachability):
        maxreach = max(reachability)
        result = [maxreach if out_reach > maxreach else out_reach for out_reach in out_reachability]
        return result

    # Override
    def reachability_plot(self, eps = 0):
        if self._consistency() :
            print("Reachability Plot ...")
            space = list(range(len(self.reachability)))
            out_space = self._search_reachability_index(self.ordering, self.out_order)
            out_reach = self.resize_out_reachability(self.out_reachability, self.reachability)
            out_reachability_figure(space, self.reachability, out_space, out_reach, "reachability_in_OPTICSArrays" + str(OPTICSArrays.plot_count), eps)
            OPTICSArrays.plot_count += 1
        else:
            print("consistency fail in reachabilityplot")
            self.status()

    def _search_reachability_index(self, order_list: list, out_order_list :list) -> list:
        result = []
        for out_order in out_order_list :
            index = order_list.index(out_order)
            result.append(index)
        return result
    
    def status(self):
        super().status()
        print("Out ordering:", self.out_order, "len:", len(self.out_order))
        print("Out reachability:", self.out_reachability, "len:", len(self.out_reachability))
    
    def _consistency(self):
        if len(self.data) == len(self.reachability):
            return True
        else :
            return False

class ClusterResolution():
    def __init__(self, clusters, resolutions) -> None:
        self.clusters = clusters
        self.resolutions = resolutions
    
    def plot(self):
        resolution_plot(self.clusters, self.resolutions, "Resoution Plot")
    
    def print(self):
        for i in range(len(self.clusters)):
            print("i:", self.clusters[i], "resolution:", self.resolutions[i])