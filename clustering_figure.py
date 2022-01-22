from GLHMongoDB import OPTICSConstruct
from GLH.Clustering import  OPTICSTrajectoryData, geography_to_euclid
from GLH.GLHmodule.geo2 import getBoundsAt
from GLH.OPTICSData import CompareResolution, ComparePixel

geo_distance = 0.1
min_samples = 4
#center = [139.545, 35.655]
center = [139.075, 36.376]
zoom = 14
#window_size = [1536, 565]
window_size = [771, 571]
plot_size = [763, 237]
size = 50

construct = OPTICSConstruct(min_samples)
all_trajectory_data = construct.clustering_obj
optics_trajectory_data : OPTICSTrajectoryData = construct.clustering_obj.clustering
eps = geography_to_euclid(geo_distance)
corner = getBoundsAt(center, zoom, window_size)

optics_array = optics_trajectory_data.create_optics_arrays()
#optics_array.status()
optics_array.data_plot()
optics_array.reachability_plot()
# res1 = optics_array.resolution_plot(cluster_size)
height1 = optics_array.max_reachability()
"""

"""


scoped_array = optics_array.map_scope(*corner)
#scoped_array.status()
scoped_array.data_plot()
scoped_array.reachability_plot(geo_distance)
resolutions = scoped_array.resolution_plot(size)
height2 = scoped_array.max_reachability()

obj = ComparePixel(resolutions, height1, height2, plot_height=plot_size[1])
obj.compare_resolution()
obj.diff_compare_resolution()
    

"""

"""


