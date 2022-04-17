from lib.GLHMongoDB import OPTICSConstruct
from lib.GLH.Clustering import  OPTICSTrajectoryData, geography_to_euclid
from lib.GLH.GLHmodule.geo2 import getBoundsAt
from lib.GLH.OPTICSData import ComparePixel, OPTICSArrays

geo_distance = 0.1
min_samples = 4
#center = [139.545, 35.655]
center = [139.075, 36.376]
zoom = 14
#window_size = [1536, 565]
window_size = [771, 571]
plot_size = [763, 237]
size = 50

def figure():
    construct = OPTICSConstruct(min_samples)
    optics_trajectory_data= construct.clustering_obj.clustering
    eps = geography_to_euclid(geo_distance)
    
    optics_array = optics(optics_trajectory_data)
    height1 = optics_array.max_reachability()

    scoped_array = scope(optics_array)
    resolutions = scoped_array.resolution_plot(size)
    height2 = scoped_array.max_reachability()

    compare_pixel(resolutions, height1, height2)


def optics(optics_trajectory_data : OPTICSTrajectoryData):
    optics_array = optics_trajectory_data.create_optics_arrays()
    #optics_array.status()
    #optics_array.data_plot()
    #optics_array.reachability_plot()
    # res1 = optics_array.resolution_plot(cluster_size)
    
    return optics_array

def scope(optics_array :OPTICSArrays):
    corner = getBoundsAt(center, zoom, window_size)

    scoped_array = optics_array.map_scope(*corner)
    #scoped_array.status()
    scoped_array.data_plot()
    scoped_array.reachability_plot(geo_distance)

    return scoped_array
    

def compare_pixel(resolutions, height1, height2):
    obj = ComparePixel(resolutions, height1, height2, plot_height=plot_size[1])
    obj.compare_resolution()
    obj.diff_compare_resolution()

if __name__ == "__name__" :
    figure()


