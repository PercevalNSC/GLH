from GLHMongoDB import OPTICSConstruct
from GLH.GLHmodule.Plotfigure import cluster_figure
from GLH.GLHmodule.Clustering import LabeledTrajectoryData

eps = 1
min_samples = 4
p1 = []
obj = OPTICSConstruct(min_samples)
obj.set_eps(eps)
obj.clustering_obj.clustering.reachability_plot()
print(obj.clustering_obj.trajectorydata)
print(obj.clustering_obj.map_scope(p1, p2))
labeled_trajectory_list = obj.labeled_trajectory_data()
ltd = LabeledTrajectoryData(labeled_trajectory_list)
label_term = ltd.cluster_term()
print(label_term)
cluster_figure(label_term, "cluster_time", "time")

