import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
import matplotlib as mpl
mpl.rcParams['agg.path.chunksize'] = 10000

SAVEPATH= "./images/"
FIGURE_DPI = 200
FIGURE_SIZE =[8, 4.5]

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

def ordered_coordinate_figure(coordinates, name, point_color = "r", line_color = "b"):
    x = [r[0] for r in coordinates]
    y = [r[1] for r in coordinates]
    xlabel = "longitude"
    ylabel = "latitude"
    fig = plt.figure(dpi=FIGURE_DPI)
    axis = fig.add_subplot(1,1,1, title=name, xlabel=xlabel, ylabel=ylabel)
    axis.get_xaxis().get_major_formatter().set_useOffset(False)
    axis.get_yaxis().get_major_formatter().set_useOffset(False)
    axis.scatter(x, y, c=point_color, s=2)
    axis.plot(x, y, c=line_color, lw=1)
    fig.savefig(SAVEPATH + name + ".png")
    print("Output: " + name + ".png")

def cluster_figure(cluster_data, name = "No title", ylabel = "No ylabel"):
    cl_data = np.array(cluster_data)
    fig = plt.figure(dpi = FIGURE_DPI)
    ax = fig.add_subplot(1,1,1, title = name, xlabel = "cluster label", ylabel = ylabel)
    ax.get_xaxis().set_major_locator(ticker.MaxNLocator(integer=True))
    ax.scatter(cl_data[:, 0], cl_data[:, 1])
    fig.savefig(SAVEPATH + name + ".png")

def reachability_figure(space, reachability, name, eps = 0, xlabel = "order", ylabel = "reachability[km]"):
    n_label = "[n = " + str(len(space)) + "]"
    fig = plt.figure(figsize=FIGURE_SIZE, dpi=FIGURE_DPI)
    axis = fig.add_subplot(1, 1, 1, title = name + n_label, xlabel = xlabel, ylabel = ylabel)
    axis.set_ylim([0, 40])

    axis.bar(space, reachability, label = "reachability", width = 1.0)
    _add_eps_line(axis, eps, 0, space[-1])

    #axis.legend(loc='center left')
    fig.savefig(SAVEPATH + name + ".png")
    print("Output: " + name + ".png")

def out_reachability_figure(space, reachability, out_space, out_reachability, name, eps = 0, xlabel = "order", ylabel = "reachability[km]"):
    n_label = "[n = " + str(len(space)) + "]"
    fig = plt.figure(figsize=FIGURE_SIZE, dpi=FIGURE_DPI)
    axis = fig.add_subplot(1, 1, 1, title = name + n_label, xlabel = xlabel, ylabel = ylabel)
    axis.set_ylim([0, max(reachability)*1.05])

    axis.bar(space, reachability, label = "reachability", width=1.0)
    #_add_eps_line(axis, eps, 0, space[-1])
    axis.bar(out_space, out_reachability, label = "out_data", color='red', alpha = 0.4, width = 1.0)

    #axis.legend(loc='center left')
    fig.savefig(SAVEPATH + name + ".png")
    print("Output: " + name + ".png")

def _add_eps_line(axis, eps, min, max):
    if eps != 0 :
        axis.hlines(eps, min, max, "g", label="eps="+str(eps))

def resolution_plot(cluster_numbers, resolutions, name = ""):
    xlabel = "number of cluster"
    ylabel = "resolution"
    fig = plt.figure(figsize=FIGURE_SIZE, dpi=FIGURE_DPI)
    axis = fig.add_subplot(1, 1, 1, title = name, xlabel = xlabel, ylabel = ylabel)
    axis.plot(cluster_numbers, resolutions, label="resolution")
    fig.savefig(SAVEPATH + name + ".png")
    print("Output: " + name + ".png")

def compare_resolution_plot(res1, res2, name = "") :
    cluster_numbers = list(range(1, len(res1)+1, 1))
    xlabel = "point order"
    ylabel = "pixel[px]"
    fig = plt.figure(figsize=FIGURE_SIZE, dpi=FIGURE_DPI)
    axis = fig.add_subplot(1, 1, 1, title = name, xlabel = xlabel, ylabel = ylabel)
    axis.plot(cluster_numbers, res1, label="resolution")
    axis.plot(cluster_numbers, res2, label="resolution")
    fig.savefig(SAVEPATH + name + ".png")
    print("Output: " + name + ".png")

def fig_output(fig :plt.Figure, name :str):
    fig.savefig(SAVEPATH + name + ".png")
    print("Output: " + name + ".png")
    fig.clf()
    fig.close()