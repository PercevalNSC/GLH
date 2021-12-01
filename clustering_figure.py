from GLHMongoDB import OPTICSConstruct
from GLH.GLHmodule.Plotfigure import cluster_figure
from GLH.GLHmodule.Clustering import LabeledTrajectoryData

eps = 1
min_samples = 4
obj = OPTICSConstruct(min_samples)
obj.set_eps(eps)
obj.clustering_obj.clustering.reachability_plot()
labeled_trajectory_list = obj.labeled_trajectory_data()
ltd = LabeledTrajectoryData(labeled_trajectory_list)
label_term = ltd.cluster_term()
print(label_term)
cluster_figure(label_term, "cluster_time", "time")

