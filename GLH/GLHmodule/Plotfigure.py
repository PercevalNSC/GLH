import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
from math import inf
import heapq

SAVEPATH= "./images/"
FIGURE_DPI = 1600

def createFigures(distlists,timelists):
    logScatterFigure(distlists[0], timelists[0], "ActivitySegment")
    logScatterFigure(distlists[1], timelists[1], "PlaceVisit")
    logScatterFigure(distlists[0] + distlists[1], timelists[0] + timelists[1], "FullSegment")

def scatterFigure(distlist, timelist, name, xlabel = "distance[m]", ylabel = "duration[minute]"):
    n = "[n = " + str(len(distlist)) + "]"
    fig = plt.figure(dpi=FIGURE_DPI)
    axis = fig.add_subplot(1, 1, 1, title = name + n, xlabel = xlabel, ylabel = ylabel)
    axis.scatter(distlist, timelist, marker=".", s=1)
    fig.savefig(SAVEPATH + name + ".png")
    print("Output: " + name + ".png")

def logScatterFigure(distlist, timelist, name, xlabel = "distance[m]", ylabel = "duration[minute]"):
    n = "[n = " + str(len(distlist)) + "]"
    fig = plt.figure(dpi=FIGURE_DPI)

    axis = fig.add_subplot(1, 1, 1, title = name + n, xlabel = xlabel, ylabel = ylabel)
    axis.scatter(distlist, timelist, marker=".")
    axis.set_xscale('log')
    axis.set_yscale('log')

    fig.savefig(SAVEPATH + name + ".png")
    print("Output: " + name + ".png")

def fullFigure(distlists,timelists):
    fig = plt.figure()

    fullax = fig.add_subplot(1, 2, 1, title = "Full", xlabel = "distance[km]", ylabel = "duration[minute]")
    fullax.scatter(distlists[0] + distlists[1], timelists[0] + timelists[1], marker=".")
    asax = fig.add_subplot(2, 2, 2, title = "ActivitySegment")
    asax.scatter(distlists[0], timelists[0], marker=".")
    pvax = fig.add_subplot(2, 2, 4, title = "PlaceVisit")
    pvax.scatter(distlists[1],timelists[1], marker=".")
    
    fig.tight_layout()
    fig.savefig("./images/difference.png")

def coordinatesFigure(coordinates, name, color="r"):
    x = [r[0] for r in coordinates]
    y = [r[1] for r in coordinates]
    xlabel = "longitude"
    ylabel = "latitude"
    fig = plt.figure(dpi=FIGURE_DPI)
    axis = fig.add_subplot(1,1,1, title=name, xlabel=xlabel, ylabel=ylabel)
    axis.get_xaxis().get_major_formatter().set_useOffset(False)
    axis.get_yaxis().get_major_formatter().set_useOffset(False)
    axis.scatter(x, y, s=1, c=color)
    fig.savefig(SAVEPATH + name + ".png")
    print("Output: " + name + ".png")

def cluster_figure(cluster_data, name = "No title", ylabel = "No ylabel"):
    cl_data = np.array(cluster_data)
    fig = plt.figure(dpi = FIGURE_DPI)
    ax = fig.add_subplot(1,1,1, title = name, xlabel = "cluster label", ylabel = ylabel)
    ax.get_xaxis().set_major_locator(ticker.MaxNLocator(integer=True))
    ax.scatter(cl_data[:, 0], cl_data[:, 1])
    fig.show()
    fig.savefig(SAVEPATH + name + ".png")

def reachability_figure(space, reachability, error_order, name, eps = 0, xlabel = "space", ylabel = "reachability"):
    n_label = "[n = " + str(len(space)) + "]"
    fig = plt.figure(dpi=FIGURE_DPI)
    axis = fig.add_subplot(1, 1, 1, title = name + n_label, xlabel = xlabel, ylabel = ylabel)
    axis.bar(space, reachability, label = "reachability", width = 1.0)
    if eps != 0 :
        axis.hlines(eps, 0, space[-1], "g", label="eps="+str(eps))
    largetst_reach = heapq.nlargest(2, reachability)
    if largetst_reach[0] == inf :
        maxreach = largetst_reach[1] * 0.5
    else :
        maxreach = largetst_reach[0] * 0.5
    maxreach_list = [maxreach for i in range(len(error_order))]
    axis.bar(error_order, maxreach_list, label = "error_order", width = 0.5, color = "red")
    axis.legend(loc='center left')
    fig.show()
    fig.savefig(SAVEPATH + name + ".png")
    print("Output: " + name + ".png")
