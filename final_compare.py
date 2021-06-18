import numpy as np
from scipy.stats import ttest_rel

#Performs paired T-test between algorithms on scores from all datasets for each metric
#Saves results ro stat_compare directory

algorithms = ["KMeans", "Meanshift", "DBSCAN", "OPTICS"]
metrics = ["jaccard_score", "homogeneity_score", "rand_score"]

for metric in metrics:

    dataset = np.genfromtxt("./result_comp/" + metric + ".csv", delimiter=',')

    scores = dataset[1:, 1:].T

    alfa = .05
    t_statistic = np.zeros((len(algorithms), len(algorithms)))
    p_value = np.zeros((len(algorithms), len(algorithms)))

    advantage = np.zeros((len(algorithms), len(algorithms)))
    significance = np.zeros((len(algorithms), len(algorithms)))

    for i in range(len(algorithms)):
        for j in range(len(algorithms)):
            t_statistic[i, j], p_value[i, j] = ttest_rel(scores[i], scores[j])

    advantage[t_statistic > 0] = 1
    significance[p_value <= alfa] = 1
    better = advantage * significance

    print("Metric: " + metric)
    print(better)
    
    file = open("./stat_compare/" + metric + "_comp.csv", 'w')
    
    file.write("Advantage: \n")
    file.write("-,KMeans,Meanshift,DBSCAN,OPTICS\n")

    for i in range(len(algorithms)):
        file.write(algorithms[i] + "," + str(advantage[i])[1:-1].replace('.', ',') + "\n")

    file.write("Significance: \n")
    file.write("-,KMeans,Meanshift,DBSCAN,OPTICS\n")

    for i in range(len(algorithms)):
        file.write(algorithms[i] + "," + str(significance[i])[1:-1].replace('.', ',') + "\n")

    file.write("Better: \n")
    file.write("-,KMeans,Meanshift,DBSCAN,OPTICS\n")

    for i in range(len(algorithms)):
        file.write(algorithms[i] + "," + str(better[i])[1:-1].replace('.', ',') + "\n")

    file.close()
