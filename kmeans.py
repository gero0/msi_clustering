import numpy as np
import random

from sklearn.base import BaseEstimator

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


class KMeans(BaseEstimator):
    """
    Implementation of KMeans clustering algorithm

    Parameters
    ----------
    K : int
        number of clusters
    init_seed: int, default=0
        Seed used by RNG during initialization (default 0)
    p_param: int, default=2
        p-param to use for calculating Minkowski distance between data points (default 2 - Euclidean distance)
    """

    def __init__(self, K, init_seed=0, p_param=2):
        self.K = K
        self.init_seed = init_seed
        self.p_param = p_param

    """
    Divides data into clusters using k-Means algorithm. Calculates centroids.

    Parameters
    ----------
    X : numpy.array
        A set of observations

    Returns
    -------
    numpy.array
        Array with labels assigned to observations
            
    """

    def fit(self, X):
        # initialization - randomly choose K data points as initial mean values
        random.seed(a=self.init_seed)

        self.means = np.array(random.sample(X.tolist(), self.K))

        labels = np.zeros(len(X))

        while True:
            previous_labels = labels[:]

            # assignment step
            for sample, (label_id, _) in zip(X, enumerate(labels)):
                distances = [minkowski_distance(
                    sample, mean, self.p_param) for mean in self.means]
                minimum = distances[0]

                for cluster_id, distance in enumerate(distances):
                    if distance < minimum:
                        labels[label_id] = cluster_id
                        minimum = distance

            # update step
            for (cluster_id, _) in enumerate(self.means):
                samples = []
                for (sample, label) in zip(X, labels):
                    if label == cluster_id:
                        samples.append(sample)

                self.means[cluster_id] = np.array(samples).mean(axis=0)

            # if assignments didn't change, the algorithm has converged
            if np.array_equal(previous_labels, labels):
                return labels

    """
    Returns centroids calculated by fit method

    Returns
    -------
    numpy.array
        Array with centroids
            
    """

    def get_centroids(self):
        return self.means

    """
    Assign samples to classes based on centroids calculated by fit method.

    Parameters
    ----------
    X : numpy.array
        A set of observations

    Returns
    -------
    numpy.array
        Array with labels assigned to observations
            
    """

    def predict(self, X):
        labels = np.zeros(len(X))

        for sample, (label_id, _) in zip(X, enumerate(labels)):
            distances = [minkowski_distance(
                sample, mean, self.p_param) for mean in self.means]
            minimum = distances[0]

            for cluster_id, distance in enumerate(distances):
                if distance < minimum:
                    labels[label_id] = cluster_id
                    minimum = distance
        
        return labels
