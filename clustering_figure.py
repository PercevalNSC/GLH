from GLHMongoDB import OPTICSConstruct
from GLH.GLHmodule.Clustering import  OPTICSTrajectoryData, geography_to_euclid
from GLH.GLHmodule.geo2 import getBoundsAt
from GLH.GLHmodule.OPTICSData import ClusterResolution

geo_distance = 0.1
min_samples = 4
center = [139.545, 35.655]
#center = [139.075, 36.376]
zoom = 14
window_size = [1536, 807]
cluster_size = 10

construct = OPTICSConstruct(min_samples)
all_trajectory_data = construct.clustering_obj
optics_trajectory_data : OPTICSTrajectoryData = construct.clustering_obj.clustering
eps = geography_to_euclid(geo_distance)
corner = getBoundsAt(center, zoom, window_size)

optics_array = optics_trajectory_data.create_optics_arrays()
optics_array.status()
optics_array.data_plot()
optics_array.reachability_plot(geo_distance)

"""
resolutions = optics_array.continuous_resolution(cluster_size)
resolution_obj = ClusterResolution(*resolutions)
resolution_obj.plot()
"""


scoped_array = optics_array.map_scope(*corner)
scoped_array.status()
scoped_array.data_plot()
scoped_array.reachability_plot(geo_distance)

"""
scoped_array.continuous_resolution(cluster_size)
"""


