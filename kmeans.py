import numpy as np;
import random

"""
Calculates Minkowski distance between two vectors of equal length.
Parameters
----------
x : numpy.array
    first vector
y : numpy.array
    second vector
p : int
    p-parameter

Returns
----------
float
    Minkowski distance of order p between vectors
"""
def minkowski_distance(x, y, p):
    abs_diffs = abs(x-y)
    power = abs_diffs ** p
    _sum = np.sum(power)
    distance = _sum ** (1/p)
    return distance


"""
Divides data into clusters using k-Means algorithm

Parameters
----------
X : numpy.array
    A set of observations
K : int
    number of clusters
init_seed: int, default=0
    Seed used by RNG during initialization (default 0)
minkowski_p_param: int, default=2
    p-param to use for calculating Minkowski distance between data points (default 2 - Euclidean distance)

Returns
-------
numpy.array
    Array with labels assigned to observations
        
"""
def kMeansClustering(X, K, init_seed=0, minkowski_p_param=2):
    #initialization - randomly choose K data points as initial mean values
    random.seed(a=init_seed)

    means = np.array(random.sample(X.tolist(), K))

    labels = np.zeros(len(X))

    while True:
        previous_labels = labels[:]

        #assignment step
        for sample, (label_id, _) in zip(X, enumerate(labels)):
            distances = [minkowski_distance(sample, mean, minkowski_p_param) for mean in means]
            minimum = distances[0]

            for cluster_id, distance in enumerate(distances):
                if distance < minimum:
                    labels[label_id] = cluster_id
                    minimum = distance
                
        #update step
        for (cluster_id, _) in enumerate(means):
            samples = []
            for (sample, label) in zip(X, labels):
                if label==cluster_id :
                    samples.append(sample)
            
            means[cluster_id] = np.array(samples).mean()

        #if assignments didn't change, the algorithm has converged
        if np.array_equal(previous_labels, labels):
            return labels
