from GLHMongoDB import OPTICSConstruct
from GLH.GLHmodule.Plotfigure import cluster_figure
from GLH.GLHmodule.Clustering import LabeledTrajectoryData, OPTICSTrajectoryData, geography_to_euclid

eps = geography_to_euclid(1)
min_samples = 4
corner = [[139.50, 35.65], [139.58, 35.67]]
construct = OPTICSConstruct(min_samples)
all_trajectory_data = construct.clustering_obj
optics_trajectory_data : OPTICSTrajectoryData = construct.clustering_obj.clustering

optics_array = optics_trajectory_data.create_optics_arrays()
optics_array.data_plot()
optics_array.reachability_plot(eps)
optics_array.map_scope(*corner)
optics_array.data_plot()
optics_array.reachability_plot(eps)

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


