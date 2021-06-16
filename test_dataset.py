from scipy.stats import ttest_rel
import numpy as np
from sklearn.base import clone
from sklearn.metrics import jaccard_score, rand_score, homogeneity_score
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.cluster import MeanShift, DBSCAN, OPTICS
from kmeans import KMeans

#Tests the clustering algorithms on each dataset and generates a report for each dataset.
#Saves results in result directory

def writearr(file, arr):
    line = ""
    for val in arr:
        line = line + "{:.3f}".format(val) + ","
    line = line + '\n'
    file.write(line)

datasets = ["australian", "banknote", "breastcan",
            "diabetes", "german", "liver", "popfailures", "spambase", "wisconsin", "yeast6"]


for dset in datasets:

    # Load dataset

    dataset = np.genfromtxt("./datasets/" + dset + ".csv", delimiter=',')

    X = dataset[:, :-1]
    y = dataset[:, -1].astype(int)

    classes_count = np.bincount(y)

    print("Now processing dataset: " + dset)

    #Kmeans and Meanshift - Stratifiedkfold

    n_splits = 5
    metric_count = 3

    algorithms_kfold = {
        'KMeans': KMeans(2, init_seed=1410),
        'MeanShift': MeanShift(),
    }

    scores_kfold = {
        'KMeans': np.zeros((n_splits, metric_count)),
        'MeanShift': np.zeros((n_splits, metric_count)),
    }

    scores_kfold_avg = {
        'KMeans': np.array(3),
        'MeanShift': np.array(3),
    }

    orphaned_kfold = {
        'KMeans': 0,
        'MeanShift': 0,
    }

    kf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=1410)

    for fold_id, (train, test) in enumerate(kf.split(X, y)):
        for algorithm in algorithms_kfold:
            X_train, X_test = X[train], X[test]
            _y_train, y_test = y[train], y[test]

            alg = clone(algorithms_kfold[algorithm])
            alg.fit(X_train)

            prediction = alg.predict(X_test)

            score_j = jaccard_score(y_test, prediction, average='macro')
            score_h = homogeneity_score(y_test, prediction)
            score_r = rand_score(y_test, prediction)

            scores_kfold[algorithm][fold_id, 0] = score_j
            scores_kfold[algorithm][fold_id, 1] = score_h
            scores_kfold[algorithm][fold_id, 2] = score_r

            orphaned_kfold[algorithm] += np.count_nonzero(prediction == -1)

    for algorithm in algorithms_kfold:
        scores_kfold_avg[algorithm] = (np.mean(
            scores_kfold[algorithm], axis=0), np.std(scores_kfold[algorithm], axis=0))


    # Comparison of KMeans and Meanshift

    metrics = ["Jaccard score", "Homogeneity score", "Rand score"]

    tests = {
        "Jaccard score": None,
        "Homogeneity score": None,
        "Rand Score": None
    }

    for i, metric in enumerate(tests):
        alfa = .05
        t_statistic = 0
        p_value = 0

        sc_kmeans = scores_kfold['KMeans'][:, i]
        sc_meansh = scores_kfold['MeanShift'][:, i]

        t_statistic, p_value = ttest_rel(sc_kmeans, sc_meansh)

        if t_statistic > 0:
            better = "Kmeans"
        else:
            better = "MeanShift"

        significant = p_value < alfa

        tests[metric] = (t_statistic, p_value, better, significant)

    # DBSCAN and OPTICS

    algorithms = {
        'DBSCAN': DBSCAN(),
        'OPTICS': OPTICS(),
    }

    scores = {
        'DBSCAN': np.zeros(3),
        'OPTICS': np.zeros(3),
    }

    noisy = {
        'DBSCAN': 0,
        'OPTICS': 0,
    }

    noisy_percent = {
        'DBSCAN': 0,
        'OPTICS': 0,
    }


    for algorithm in algorithms:
        alg = clone(algorithms[algorithm])
        prediction = alg.fit_predict(X)

        score_j = jaccard_score(y, prediction, average='macro')
        score_h = homogeneity_score(y, prediction)
        score_r = rand_score(y, prediction)

        scores[algorithm][0] = score_j
        scores[algorithm][1] = score_h
        scores[algorithm][2] = score_r

        noisy[algorithm] = np.count_nonzero(prediction == -1)
        noisy_percent[algorithm] = (
            np.count_nonzero(prediction == -1) / len(X)) * 100


    file = open("./results/"+dset+"_results.csv", 'w')

    file.write("Sample count: \n")
    file.write("0, 1\n")
    file.write(str(classes_count[0]) + "," + str(classes_count[1]) + "\n")

    file.write("\nScores:\n")

    for clf in scores_kfold:
        file.write(clf+'\n')
        file.write("Jaccard Score,Homogeneity Score,Rand Score\n")
        for fold in scores_kfold[clf]:
            writearr(file, fold)


    file.write("\nAverage\n")
    for clf in scores_kfold_avg:
        file.write(clf+'\n')
        file.write("Jaccard Score,Homogeneity Score,Rand Score\n")
        arr = scores_kfold_avg[clf][0]
        writearr(file, arr)

    file.write("\nStandard deviation\n")
    for clf in scores_kfold_avg:
        file.write(clf+'\n')
        file.write("Jaccard Score,Homogeneity Score,Rand Score\n")
        arr = scores_kfold_avg[clf][1]
        writearr(file, arr)

    file.write("\nKMeans and Meanshift Comparison\n")
    for test in tests:
        file.write("\n" + test + "\n")
        file.write("t-statistic, p-value\n")
        test = tests[test]
        file.write("{:.3f}".format(test[0]) + "," + "{:.3f}".format(test[1]) + "\n")
        file.write("Better, Significant\n")
        file.write(str(test[2]) + "," + str(test[3]) + "\n")


    file.write("\nSamples marked as orphaned by Meanshift\n")
    file.write(str(orphaned_kfold['MeanShift']) + "\n")

    file.write("\nScores for OPTICS and DBSCAN\n")
    for clf in scores:
        file.write(clf+'\n')
        file.write("Jaccard Score,Homogeneity Score,Rand Score\n")
        writearr(file, scores[clf])

    file.write("\nOPTICS and DBSCAN noisy samples(in %)\n")
    for clf in scores:
        file.write(clf+'\n')
        file.write("{:.3f}".format(noisy_percent[clf]) + "\n")


    file.close()
