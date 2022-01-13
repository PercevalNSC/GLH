import numpy as np
import heapq
from math import inf

from GLH.GLHmodule.Plotfigure import reachability_figure, out_reachability_figure, ordered_coordinate_figure, resolution_plot
from GLH.GLHmodule.geo3 import euclid_to_geography

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

    def reachability_plot(self, eps = 0):
        if self._consistency() :
            print("Reachability Plot ...")
            space = list(range(len(self.reachability)))
            reachability_figure(space, self.reachability, "reachability_in_OPTICSArrays" + str(OPTICSArrays.plot_count), eps)
            OPTICSArrays.plot_count += 1
        else:
            print("consistency fail in reachabilityplot")
            self.status()
    
    def data_plot(self):
        print("Data Plot ...")
        name = "Data_Plot" + str(OPTICSArrays.plot_count)
        #coordinatesFigure(self._remove_noise(self.data), name, 'b' )
        ordered_coordinate_figure(self._remove_noise(self.data), name)
        OPTICSArrays.plot_count += 1

    def reachability_resolution(self, cluster_n :int) -> int:
        # print(heapq.nlargest(3, reachability))
        largest_boundary = self._max_include_inf_list(self._clustering_boundary(), cluster_n)
        return largest_boundary[0] - largest_boundary[-1]
    
    def continuous_resolution(self, cluster_ns :int):
        result = [[], []]
        for i in range(2, cluster_ns+1, 1):
            resolution = self.reachability_resolution(i)
            result[0].append(i)
            result[1].append(resolution)
        return result
           
    def status(self):
        """ Print instance value. """
        print("Data:", self.data, "len:", len(self.data))
        print("Reachability:", self.reachability, "len:", len(self.reachability))
        print("Ordering:", self.ordering, "len:", len(self.ordering))

    def print(self):
        """ Return string about instance value. """
        return "Data:" + str(self.data) + "\nReachability:" + str(self.reachability) + "\nOrdering:" +  str(self.ordering)

    def _max_include_inf_list(self, inflist :list, n :int):
        largest = heapq.nlargest(n+1, inflist)
        if largest[0] == inf :
            return largest[1:]
        else :
            return largest[:-1]

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

    def _is_in_map(self, p1, p2, cp) -> bool:
        """ When cp is in rectangle constructed p1 and p2, return True """
        if (cp[0] < p1[0]) | (p2[0] < cp[0]) | (cp[1] < p1[1]) | (p2[1] < cp[1]):
            return False
        else :
            return True

    def _init_order(self):
        return np.array(list(range(len(self.reachability))))

    def _ordered_list(self, target_list, order_list):
        """ Order target_list by order_list.

        return ordered_target_list
        """
        if len(target_list) != len(order_list):
            print("Invaild length: target and order list")
            return target_list
        ordered_list = []
        for order in order_list :
            ordered_list.append(target_list[order])
        return np.array(ordered_list)

    def _not_in_map(self, start_index, p1, p2):
        """ Find continuous list not being in map.
        Return [maxreachability, skipcount].
        maxreachability: max reachability in map-out list,
        skipcount: length of map-out list
        """
        i = start_index
        maxreachability = 0
        # Increament i until self.data[i] is in map
        for i in range(start_index, len(self.data), 1):
            if self._is_in_map(p1, p2, self.data[i]) :
                break
            else :
                maxreachability = max(maxreachability, self.reachability[i])
    
        skipcount = i - start_index - 1
        return [maxreachability, skipcount]

    def _geography_reachability(self, euclid_reachability):
        """ Convert euclid distance to geographic distance in reachability. """
        return [euclid_to_geography(euclid_reach) for euclid_reach in euclid_reachability]

    def _clustering_boundary(self):
        """ Return clustring boundary list. """
        return self._boundary_detection(self.reachability)
    
    def _boundary_detection(self, reachability):
        boundary_list = []
        if reachability[0] >= reachability[1] :
            boundary_list.append(reachability[0])
        if reachability[-1] >= reachability[-2] :
            boundary_list.append(reachability[-1])
        
        flag  = False
        for i in range(1, len(reachability)-1, 1):
            if flag :
                if reachability[i] > reachability[i+1] :
                    boundary_list.append(reachability[i])
                    flag = False
                elif reachability[i] < reachability[i+1]:
                    flag = False
                # reachability[i] == reachability[i+1] : flag = True
                continue

            if (reachability[i-1] < reachability[i]):
                if reachability[i] > reachability[i+1] :
                    boundary_list.append(reachability[i])
                elif reachability[i] == reachability[i+1] :
                    flag = True
                continue
        return boundary_list
    
    def to_dict_list(self):
        dict_list = []
        for i in range(len(self.reachability)):
            one_dict = {"data": self.data[i].tolist(), "reachability": self.reachability[i].item(), "order": self.ordering[i].item()}
            dict_list.append(one_dict)
        return dict_list

class ScopedOPTICSArrays(OPTICSArrays):
    def __init__(self, data: list, reachability: list, ordering: list, error_order: list, error_reachability: list) -> None:
        super().__init__(data, reachability, ordering)
        self.out_order = error_order
        self.out_reachability = error_reachability
    
    def resize_out_reachability(self, out_reachability, reachability):
        """ Limit out_reachability height. """
        maxreach = self._max_include_inf_list(reachability, 1)[0]
        maxreach += maxreach * 0.01
        resized_out_reachability = [maxreach if out_reach > maxreach else out_reach for out_reach in out_reachability]
        return resized_out_reachability

    def merge_reachability(self, reachability :list, out_reachability :list):
        """ Merge reachability and out_reachability. """
        merge_reach = reachability.copy()
        out_indexes = self._search_reachability_index(self.ordering, self.out_order)
        for index, out_index in enumerate(out_indexes) :
            merge_reach[out_index] = out_reachability[index]
        return merge_reach
    
    # Override
    def reachability_plot(self, eps = 0):
        if self._consistency() :
            print("Reachability Plot ...")
            space = list(range(len(self.reachability)))
            out_space = self._search_reachability_index(self.ordering, self.out_order)
            out_reach = self.out_reachability
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

    def _clustering_boundary(self):
        """ Return clustring boundary list. """
        resize = self.resize_out_reachability(self.out_reachability, self.reachability)
        reachability = self.merge_reachability(self.reachability, resize)
        return self._boundary_detection(reachability)


class ClusterResolution():
    plot_count = 0
    def __init__(self, clusters, resolutions) -> None:
        self.clusters = clusters
        self.resolutions = resolutions
    
    def plot(self):
        resolution_plot(self.clusters, self.resolutions, "Resoution Plot " + str(ClusterResolution.plot_count))
        ClusterResolution.plot_count += 1
    
    def print(self):
        for i in range(len(self.clusters)):
            print("i:", self.clusters[i], "resolution:", self.resolutions[i])
