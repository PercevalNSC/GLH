from GLHMongoDB import *

if __name__ == "__main__":
    print("Start GLH test")
    with open('GLH_test.log', 'w') as f:
        print("Test: collection")
        f.write("Test: Get Collection")
        f.write("json format")
        f.write("ActivitySegment.SimplifiedRawPath: " + str(GetGLHAssrp().json()))
        f.write("ActivitySegment.WaypointPath: " + str(GetGLHAswp().json()))
        f.write("PlaceVisit.SimplifiedRawPath: " + str(GetGLHAswp().json()))
        f.write("PlaceVisit.location: " + str(GetGLHAswp().json()))


        print("Test: clustering")
        f.write("Test: Clustering")
        eps = 0.01
        min_samples = 4

        f.write("Get_dbscan_point: " + str(get_dbscan_point(eps, min_samples)))
        f.write("Get_dbscan_polygon: " + str(get_dbscan_polygon(eps, min_samples)))
        f.write("Get_optics_point: "+ str(get_optics_point(eps, min_samples)))
        f.write("Get_optics_polygon: "+ str(get_optics_polygon(eps, min_samples)))