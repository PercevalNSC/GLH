from GLHMongoDB import OPTICSConstruct
from GLH.Clustering import OPTICSTrajectoryData
from Setting.MongoDBSetting import GLHDB



min_samples = 4

construct = OPTICSConstruct(min_samples)
all_trajectory_data = construct.clustering_obj
optics_trajectory_data : OPTICSTrajectoryData = construct.clustering_obj.clustering
mongodb = GLHDB("glh_reach", "data2")

optics_array = optics_trajectory_data.create_optics_arrays()
optics_array.status()
dicted_data = optics_array.to_dict_list()
#print(dicted_data)
mongodb.insertmany(dicted_data)
"""
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

"""


