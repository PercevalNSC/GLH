import numpy as np
import heapq
from math import inf, isinf

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
            self.datalist = self._ordered_list(data, ordering)
            self.reachability = self._geography_reachability(self._ordered_list(reachability, ordering))
            self.ordering = self._init_order()
        else :
            print("OPTICSArray: Pre-ordered mode")
            self.datalist = data
            self.reachability = reachability
            self.ordering = ordering

    def map_scope(self, p1, p2):
        # Order(2n)
        print("Map scope by", p1, p2)
        scope_data = []
        scope_reachability = []
        scope_order = []
        error_order = []
        maxreach = 0
        for i, data in enumerate(self.datalist) :
            if self._is_in_map(p1, p2, data):
                if maxreach != 0 :
                    scope_data.append(np.zeros(3))
                    scope_reachability.append(maxreach)
                    scope_order.append(self.ordering[i-1])
                    error_order.append(self.ordering[i-1])
                scope_data.append(data)
                scope_reachability.append(self.reachability[i])
                scope_order.append(self.ordering[i])
                maxreach = 0
            else :
                if self.reachability[i] != inf :
                    maxreach = max(maxreach, self.reachability[i])
                if i == len(self.datalist)-1 :
                    scope_data.append(np.zeros(3))
                    scope_reachability.append(maxreach)
                    scope_order.append(self.ordering[i])
                    error_order.append(self.ordering[i])
        return ScopedOPTICSArrays(scope_data, scope_reachability, scope_order, error_order)

    def _is_in_map(self, p1, p2, data) -> bool:
        """ When cp is in rectangle constructed p1 and p2, return True """
        if (data[0] < p1[0]) | (p2[0] < data[0]) | (data[1] < p1[1]) | (p2[1] < data[1]):
            return False
        else :
            return True

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
        ordered_coordinate_figure(self._remove_noise(self.datalist), name)
        OPTICSArrays.plot_count += 1

    def resolution_plot(self, size :int) -> int:
        # print(heapq.nlargest(3, reachability))
        obj = ClusterResolution(self.reachability)
        return obj.resolution_plot(size)
           
    def status(self):
        """ Print instance value. """
        print("Data:", self.datalist, "len:", len(self.datalist))
        print("Reachability:", self.reachability, "len:", len(self.reachability))
        print("Ordering:", self.ordering, "len:", len(self.ordering))

    def print(self):
        """ Return string about instance value. """
        return "Data:" + str(self.datalist) + "\nReachability:" + str(self.reachability) + "\nOrdering:" +  str(self.ordering)

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
            else :
                print("errordata:", d)
        return temp

    def _consistency(self):
        if len(self.datalist) == len(self.reachability) and len(self.datalist) == len(self.ordering):
            return True
        else :
            return False


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

    def _geography_reachability(self, euclid_reachability):
        """ Convert euclid distance to geographic distance in reachability. """
        return [euclid_to_geography(euclid_reach) for euclid_reach in euclid_reachability]
    
    def to_dict_list(self):
        dict_list = []
        for i in range(len(self.reachability)):
            one_dict = {"data": self.datalist[i].tolist(), "reachability": self.reachability[i].item(), "order": self.ordering[i].item()}
            dict_list.append(one_dict)
        return dict_list

class ScopedOPTICSArrays(OPTICSArrays):
    def __init__(self, data: list, reachability: list, ordering: list, out_order: list) -> None:
        super().__init__(data, reachability, ordering)
        self.out_ordering = out_order
    
    def resized_reachability(self):
        """ Limit out_reachability height. """
        maxreach = self._max_include_inf_list(self._pure_reachability(), 1)[0]
        print("max_pure_reachability:", maxreach)
        maxreach += maxreach * 0.01
        return  [self._compare_out_reachability(maxreach, reach) for reach in self.reachability]
    
    def _compare_out_reachability(self, maxreach, reach):
        return 0 if reach > maxreach else reach 
    
    def _out_index_list(self) -> list:
        """ Map out_ordering to ordering index """
        return [self.ordering.index(out_order) for out_order in self.out_ordering]
    
    def _out_reachability(self) -> list:
        """ reachability list of representative point  """
        return [self.reachability[out_order] for out_order in self._out_index_list()]
    
    def _pure_reachability(self):
        result = self.reachability.copy()
        for index in self._out_index_list():
            result[index] = 0
        return result

    def _pure_height(self) -> float:
        pure_reachability = self._pure_reachability()
        maxreach = heapq.nlargest(2, pure_reachability)
        if isinf(maxreach[0]) :
            return maxreach[1]
        else : 
            return maxreach[0]

    # Override
    def reachability_plot(self, eps = 0):
        if self._consistency() :
            print("Reachability Plot ...")
            space = list(range(len(self.reachability)))
            reachability = self._pure_reachability()
            out_space = self._out_index_list()
            out_reach = self._out_reachability()
            out_reachability_figure(space, reachability, out_space, out_reach, "reachability_in_OPTICSArrays" + str(OPTICSArrays.plot_count), eps)
            OPTICSArrays.plot_count += 1
        else:
            print("consistency fail in reachabilityplot")
            self.status()
    
    def resolution_plot(self, size: int):
        obj = ScopeClusterResolution(self.reachability, self._pure_height())
        return obj.resolution_plot(size)


    def status(self):
        super().status()
        print("Out ordering:", self.out_ordering, "len:", len(self.out_ordering))
    
    def _consistency(self):
        if len(self.datalist) == len(self.reachability):
            return True
        else :
            return False
    
    

class ClusterResolution():
    plot_count = 0
    def __init__(self, reachability):
        self.reachability = self._init_reachability(reachability)
    
    def _init_reachability(self, reachability :list):
        init_reachability = reachability.copy()
        if isinf(init_reachability[0]) :
            init_reachability[0] = 0
        return init_reachability

    def resolution_plot(self, size: int):
        print("Resolution Plot...")
        maxreach = self._max_reachability()
        resolution_list = [res / maxreach for res in self.reachability_resolution(size)]
        print("max_reachability:", maxreach)
        resolution_label = range(1, len(resolution_list)+1, 1)
        self.resolution_status(resolution_list)
        resolution_plot(resolution_label, resolution_list, "Resoution Plot " + str(ClusterResolution.plot_count))
        ClusterResolution.plot_count += 1
        return resolution_list
    
    def _max_reachability(self):
        return max(self.reachability)

    def reachability_resolution(self, size: int) :
        boundary_list = self.pick_boundary()
        boundary_list.sort(reverse=True)
        #print(boundary_list)
        if size > len(boundary_list)-1 :
            size = len(boundary_list)-1
            print("Waring: reachability resoluion is given too large size, limited:", size)
        resolution_list = []
        for i in range(size) :
            resolution_list.append(boundary_list[i] - boundary_list[i+1])
        return resolution_list

    def pick_boundary(self):
        boundary_list = [] 
        boundary_height = 0
        if self.reachability[0] > self.reachability[1] :
            boundary_list.append(self.reachability[0])
        for i in range(1, len(self.reachability)-1, 1) :
            if self.reachability[i-1] < self.reachability[i] :
                boundary_height = self.reachability[i]
            elif self.reachability[i] < self.reachability[i+1] :
                if boundary_height != 0 :
                    boundary_list.append(boundary_height)
                    boundary_height = 0
            else :
                continue
        if self.reachability[-2] < self.reachability[-1] :
            boundary_list.append(self.reachability[-1])
        return boundary_list
    
    def resolution_status(self, resolution_list) -> None:
        for i, res in enumerate(resolution_list) :
            print("i:", i+1, "resolution:", res)

class ScopeClusterResolution(ClusterResolution):
    def __init__(self, reachability, pure_height):
        self.pure_height = pure_height
        super().__init__(reachability)
    
    #Override

    def _init_reachability(self, reachability: list):
        init_reachability = [0 if reach > self.pure_height else reach for reach in reachability]
        return init_reachability
    
    def _max_reachability(self):
        print("pure_height:", self.pure_height)
        return self.pure_height * 1.01