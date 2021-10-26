import numpy as np
from  sklearn.cluster import DBSCAN
import seaborn as sns
import matplotlib.pyplot as plt

from libraries.MongoDBSetting import MongoDBSet
from libraries.GLH import GLHTrajectoryData

if __name__ == "__main__":
    as_srp_collection = MongoDBSet().asSrpQuery()
    pv_srp_collection = MongoDBSet().pvSrpQuery()

    dataobj = GLHTrajectoryData()
    trajectrydata = dataobj.allTrajectryData(as_srp_collection, pv_srp_collection)
    dataobj.exportFigure()

    trajectrydata = np.array(trajectrydata)
    coordinates = trajectrydata[:,0:2]
    
    eps = 0.001
    min_samples = 4
    dbscan = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(coordinates)
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.scatter(coordinates[:,0], coordinates[:,1], c=dbscan)
    fig.show()
    fig.savefig("dbscan")
    print(dbscan)