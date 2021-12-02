from io import TextIOWrapper
from GLHMongoDB import *
from GLH.GLHmodule.Clustering import LabeledTrajectoryData, OPTICSArrays, OPTICSTrajectoryData
from GLH.GLHmodule.Plotfigure import cluster_figure
def test_getcollection(f :TextIOWrapper):
    print("Test: collection")
    f.write("Test: Get Collection")
    f.write("json format")
    f.write("ActivitySegment.SimplifiedRawPath: " + str(GetGLHAssrp().json()))
    f.write("ActivitySegment.WaypointPath: " + str(GetGLHAswp().json()))
    f.write("PlaceVisit.SimplifiedRawPath: " + str(GetGLHAswp().json()))
    f.write("PlaceVisit.location: " + str(GetGLHAswp().json()))

def test_clustering(f :TextIOWrapper):
    print("Test: clustering")
    f.write("Test: Clustering")
    eps = 0.01
    min_samples = 4

    f.write("Get_dbscan_point: " + str(get_dbscan_point(eps, min_samples)))
    f.write("Get_dbscan_polygon: " + str(get_dbscan_polygon(eps, min_samples)))
    f.write("Get_optics_point: "+ str(get_optics_point(eps, min_samples)))
    f.write("Get_optics_polygon: "+ str(get_optics_polygon(eps, min_samples)))

def test_optics_construct(f :TextIOWrapper):
    eps = 1
    min_samples = 4
    construct = OPTICSConstruct(min_samples)
    construct.set_eps(eps)
    all_trajectory_data = construct.clustering_obj
    optics_trajectory_data : OPTICSTrajectoryData = construct.clustering_obj.clustering

    test_optics_array(f, optics_trajectory_data.create_optics_arrays())

def test_all_trajectory_data(f :TextIOWrapper, all_trajectory_data_object :AllTrajectoryData):
    all_trajectory_data = all_trajectory_data_object

def test_OPTICS_trajectory_data(f :TextIOWrapper, optics_trajectory_data_object :OPTICSTrajectoryData):
    eps = 1
    optics_trajectory_data = optics_trajectory_data_object
    optics_trajectory_data.set_eps(eps)

    test_optics_array(f, optics_trajectory_data.create_optics_arrays())

def test_label_term(f :TextIOWrapper):
    eps = 1
    min_samples = 4
    corner = [[139.50, 35.65], [139.58, 35.67]]
    construct = OPTICSConstruct(min_samples)

    construct.set_eps(eps)
    construct.clustering_obj.clustering.reachability_plot()
    f.write(construct.clustering_obj.trajectorydata)
    labeled_trajectory_list = construct.labeled_trajectory_data()
    ltd = LabeledTrajectoryData(labeled_trajectory_list)
    label_term = ltd.cluster_term()
    f.write(label_term)
    cluster_figure(label_term, "cluster_time", "time")

def test_optics_array(f :TextIOWrapper):
    min_samples = 4
    corner = [[139.50, 35.65], [139.58, 35.67]]
    construct = OPTICSConstruct(min_samples)
    optics_array = construct.clustering_obj.clustering.create_optics_arrays()

    f.write("Init OPTICSArray\n")
    f.write(optics_array.print())
    optics_array.data_plot()
    optics_array.reachability_plot()

    optics_array.map_scope(*corner)
    f.write("Map Scoped\n")
    f.write(optics_array.print())
    optics_array.data_plot()
    optics_array.reachability_plot()

if __name__ == "__main__":
    print("Start GLH test")
    with open('GLH_test.log', 'w') as f:
        test_optics_construct(f)

        