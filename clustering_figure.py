from GLHMongoDB import OPTICSConstruct
from GLH.GLHmodule.Clustering import LabeledTrajectoryData, OPTICSTrajectoryData, geography_to_euclid
from GLH.GLHmodule.geo2 import getBoundsAt

geo_distance = 0.1
min_samples = 4
center = [139.545, 35.655]
zoom = 7
window_size = [1536, 807]
cluster_size = 10

construct = OPTICSConstruct(min_samples)
all_trajectory_data = construct.clustering_obj
optics_trajectory_data : OPTICSTrajectoryData = construct.clustering_obj.clustering
eps = geography_to_euclid(geo_distance)
corner = getBoundsAt(center, zoom, window_size)


optics_array = optics_trajectory_data.create_optics_arrays()
optics_array.data_plot()
optics_array.reachability_plot(eps)
optics_array.continuous_resolution_print(cluster_size)
scoped_array = optics_array.map_scope(*corner)
scoped_array.data_plot()
scoped_array.reachability_plot(eps)
scoped_array.continuous_resolution_print(cluster_size)
"""
construct.set_eps(eps)
construct.clustering_obj.clustering.reachability_plot()
print(construct.clustering_obj.trajectorydata)
labeled_trajectory_list = construct.labeled_trajectory_data()
ltd = LabeledTrajectoryData(labeled_trajectory_list)
label_term = ltd.cluster_term()
print(label_term)
cluster_figure(label_term, "cluster_time", "time")
"""


