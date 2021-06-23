import random, math
import numpy as np

class Kmeans:
    def __init__(self,k):
        """
        Class constructor to initialize values
        :param k:
        """
        self.k=k

    def euclidean(self, pairs):
        """
        Computes & returns euclidean distance between pairs of points
        :param pairs:
        :return: float
        """
        return math.sqrt(sum([math.pow(x[0]-x[1],2) for x in pairs]))

    def initialize_centroids(self,dataset):
        """
        Method to initialize centroids
        """
        centroids=[]
        for i in range(self.k):
            index = random.randint(0,len(dataset)-1)
            centroids.append(dataset[index])
        return centroids

    def find_nearest_centroid(self, centroids, datapoint, func_):
        """
        finds nearest centroid and resturns distance and cluster assignment
        :param centroids:
        :param dataset:
        :return: least distance to centroid and cluster id
        """
        distances = []
        distances = list(map(func_, [list(zip(datapoint, centroid)) for centroid in centroids]))
        # print(distances)
        min_distance = min(distances)
        return min_distance, distances.index(min_distance)

    def update_centroids(self, centroids, dataset, assignments):
        """
        Recomputes cluster centroids
        :param centroids:
        :param dataset:
        :param distances:
        :return: list
        """

        updated_centroids = [centroid for centroid in centroids]
        for centroid, datapoints in assignments.items():
            for point in datapoints:
                updated_centroids[centroid] = list(map(lambda x:x[0]+x[1],list(zip(updated_centroids[centroid],dataset[point]))))
            updated_centroids[centroid] = list(map(lambda x: float(x)/float(len(datapoints)+1),updated_centroids[centroid]))
        return updated_centroids




    def dokmeans(self, dist_func, dataset, n_iter=0):
        """Driver method within class to perform kmeans"""
        centroids = self.initialize_centroids(dataset)
        distances={i:0 for i in range(len(dataset))}
        for i in range(n_iter):
            assignments = {i: [] for i in range(self.k)}
            for i in range(len(dataset)):
                distance, centroid = self.find_nearest_centroid(centroids,dataset[i], dist_func)
                distances[i] = distance
                assignments[centroid].append(i)
            # print("distance:",distances)
            # print("Assignments:",assignments)
            centroids = self.update_centroids(centroids, dataset,assignments)
            # print("updated centroids:",centroids)
            sse = pow(sum([dist for dist in distances.values()]),2)

            print("sse",sse)
        sse = pow(sum([dist for dist in distances.values()]), 2)
        print("final sse:",sse)
        return sse, assignments






def main(k, dist_func, dataset):
    """
    Driver method to perform kmeans
    :param k:
    :param dist_func:
    :param dataset:
    :return:
    """
    k = 3
    kms = Kmeans(k)
    if dist_func=='euclidean':
        func_ = kms.euclidean
    sse, assignments = kms.dokmeans(func_,dataset,5)
    print("final cluster assignments of 100 datapoints:\n", assignments)




def load_dataset(N,k):
    """
    Creates random data with N datapoints and k dimensionality drawn from a uniform distribution with mean 0
    & standard deviation 1
    :param N: integer
    :param k: ineger
    :return: list of lists
    """
    dataset = np.random.rand(N,k).tolist()
    return dataset




if __name__=="__main__":
    dataset = load_dataset(100,3)
    main(3,'euclidean',dataset)