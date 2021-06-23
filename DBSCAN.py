import numpy as np
import collections
import matplotlib.pyplot as plt
import queue
import scipy.io as spio

# Define label for differnt point group
NOISE = 0
UNASSIGNED = 0
core = -1
edge = -2


# function to find all neigbor points in radius
def neighbor_points(data, pointId, radius):
    points = []
    for i in range(len(data)):
        # Euclidian distance using L2 Norm
        # if np.linalg.norm([(i[0]-i[1]) for i in zip(data[i], data[pointId])])<=radius:
        if np.linalg.norm(np.array(data[i]) - np.array(data[pointId])) <= radius:
            points.append(i)
    return points


# DB Scan algorithom
def dbscan(data, Eps, MinPt):
    # initilize all pointlable to unassign
    pointlabel = [UNASSIGNED] * len(data)
    pointcount = []
    # initilize list for core/noncore point
    corepoint = []
    noncore = []

    # Find all neigbor for all point
    for i in range(len(data)):
        pointcount.append(neighbor_points(train, i, Eps))

    # Find all core point, edgepoint and noise
    for i in range(len(pointcount)):
        if (len(pointcount[i]) >= MinPt):
            pointlabel[i] = core
            corepoint.append(i)
        else:
            noncore.append(i)

    for i in noncore:
        for j in pointcount[i]:
            if j in corepoint:
                pointlabel[i] = edge

                break

    # start assigning point to luster
    cl = 1
    # Using a Queue to put all neigbor core point in queue and find neigboir's neigbor
    for i in range(len(pointlabel)):
        q = queue.Queue()
        if (pointlabel[i] == core):
            pointlabel[i] = cl
            for x in pointcount[i]:
                if (pointlabel[x] == core):
                    q.put(x)
                    pointlabel[x] = cl
                elif (pointlabel[x] == edge):
                    pointlabel[x] = cl
            # Stop when all point in Queue has been checked
            while not q.empty():
                neighbors = pointcount[q.get()]
                for y in neighbors:
                    if (pointlabel[y] == core):
                        pointlabel[y] = cl
                        q.put(y)
                    if (pointlabel[y] == edge):
                        pointlabel[y] = cl
            cl = cl + 1  # move to next cluster

    return pointlabel, cl


# Function to plot final result
def plotRes(data, clusterRes, clusterNum):
    nPoints = len(data)
    scatterColors = ['black', 'green', 'brown', 'red', 'purple', 'orange', 'yellow']
    for i in range(clusterNum):
        if (i == 0):
            # Plot all noise point as blue
            color = 'blue'
        else:
            color = scatterColors[i % len(scatterColors)]
        x1 = [];
        y1 = []
        for j in range(nPoints):
            if clusterRes[j] == i:
                x1.append(data[j, 0])
                y1.append(data[j, 1])
        plt.scatter(x1, y1, c=color, alpha=1, marker='.')


# Load Data
# raw = spio.loadmat('DBSCAN.mat')
# train = raw['Points']
train = [[ 0, 10, 20 ],
        [ 0, 11, 21 ],
        [ 0, 12, 20 ],
        [ 20, 33, 59 ],
        [ 21, 32, 56 ],
        [ 59, 77, 101 ],
        [ 58, 79, 100 ],
        [ 58, 76, 102 ],
        [ 300, 70, 20 ],
        [ 500, 300, 202],
        [ 500, 302, 204 ]]


# Set EPS and Minpoint
epss = [5, 10]
minptss = [3, 2]
# Find ALl cluster, outliers in different setting and print resultsw
for eps in epss:
    for minpts in minptss:
        print('Set eps = ' + str(eps) + ', Minpoints = ' + str(minpts))
        pointlabel, cl = dbscan(train, eps, minpts)
        plotRes(train, pointlabel, cl)
        plt.show()
        print('number of cluster found: ' + str(cl - 1))
        counter = collections.Counter(pointlabel)
        print(counter)
        outliers = pointlabel.count(0)
        print('numbrer of outliers found: ' + str(outliers) + '\n')