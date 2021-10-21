import matplotlib.pyplot as plt

def createFigures(distlists,timelists):
    logScatterFigure(distlists[0], timelists[0], "ActivitySegment")
    logScatterFigure(distlists[1], timelists[1], "PlaceVisit")
    logScatterFigure(distlists[0] + distlists[1], timelists[0] + timelists[1], "FullSegment")

def scatterFigure(distlist, timelist, name, xlabel = "distance[m]", ylabel = "duration[minute]"):
    savepath = "./images/"
    n = "[n = " + str(len(distlist)) + "]"
    fig = plt.figure(dpi=200)
    axis = fig.add_subplot(1, 1, 1, title = name + n, xlabel = xlabel, ylabel = ylabel)
    axis.scatter(distlist, timelist, marker=".")
    fig.savefig(savepath + name + ".png")
    print("Output: " + name + ".png")

def logScatterFigure(distlist, timelist, name, xlabel = "distance[m]", ylabel = "duration[minute]"):
    savepath = "./images/"
    n = "[n = " + str(len(distlist)) + "]"
    fig = plt.figure(dpi=200)

    axis = fig.add_subplot(1, 1, 1, title = name + n, xlabel = xlabel, ylabel = ylabel)
    axis.scatter(distlist, timelist, marker=".")
    axis.set_xscale('log')
    axis.set_yscale('log')

    fig.savefig(savepath + name + ".png")
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
