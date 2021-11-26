from GLHMongoDB import OPTICSConstruct
from GLH.GLHmodule.Plotfigure import cluster_figure



eps = 0.0001
min_samples = 4
obj = OPTICSConstruct(min_samples)
obj.set_eps(eps)
labeled_trajectory_list = obj.labeled_trajectory_data()
label_time = []
for label_trajectory_data in labeled_trajectory_list :
    during = [label_trajectory_data[1][0][2], label_trajectory_data[1][0][2]]
    for trajectory_set in label_trajectory_data[1] :
        during[0] = min(during[0], trajectory_set[2])
        during[1] = max(during[1], trajectory_set[2])
    during_time = during[1] - during[0]
    label_time.append([label_trajectory_data[0], during_time])
print(label_time)
cluster_figure(label_time, "cluster_time", "time")

