
import numpy as np
datasets = ["australian", "banknote", "breastcan",
            "diabetes", "german", "liver", "popfailures", "spambase", "wisconsin", "yeast6"]

for dset in datasets:

    scores = open("./results/" + dset + "_results.csv")
    file = open("./latex/" + dset + "_latex.txt", 'w')

    lines = scores.readlines()

    file.write("\n" + dset + "\n")
    # Kmeans scores
    file.write("\nKmean scores\n")

    file.write(
        """
\\begin{table}[]
\\begin{tabular}{|l|l|l|l|}
\hline
Fold & Jaccard Score & Homogeneity Score & Rand Score \\\\ \\hline
""")

    for fold_id, line in enumerate(lines[7:12]):
        vals = line.split(',')
        file.write("{} & {} & {} & {} \\\\ \\hline \n".format(
            fold_id+1, vals[0], vals[1], vals[2]))

    file.write(
        """\end{tabular}
\end{table}
"""
    )

    # KMeans avg

    file.write("\nKmeans average\n")

    file.write(
        """
\\begin{table}[]
\\begin{tabular}{|l|l|l|}
\hline
Jaccard Score & Homogeneity Score & Rand Score \\\\ \\hline
""")

    vals = lines[23].split(',')
    stds = lines[31].split(',')

    file.write("{} ({}) & {} ({}) & {} ({}) \\\\ \\hline \n".format(
        vals[0], stds[0], vals[1], stds[1], vals[2], stds[2]))

    file.write(
        """\end{tabular}
\end{table}
"""
    )

    #Meanshift scores

    file.write("\nMeanshift scores\n")

    file.write(
        """
\\begin{table}[]
\\begin{tabular}{|l|l|l|l|}
\hline
Fold & Jaccard Score & Homogeneity Score & Rand Score \\\\ \\hline
""")

    for fold_id, line in enumerate(lines[14:19]):
        vals = line.split(',')
        file.write("{} & {} & {} & {} \\\\ \\hline \n".format(
            fold_id+1, vals[0], vals[1], vals[2]))

    file.write(
        """\end{tabular}
\end{table}
"""
    )

    # Meanshift avg

    file.write("\nMeanshift average\n")

    file.write(
        """
\\begin{table}[]
\\begin{tabular}{|l|l|l|}
\hline
Jaccard Score & Homogeneity Score & Rand Score \\\\ \\hline
""")

    vals = lines[26].split(',')
    stds = lines[34].split(',')

    file.write("{} ({}) & {} ({}) & {} ({}) \\\\ \\hline \n".format(
        vals[0], stds[0], vals[1], stds[1], vals[2], stds[2]))

    file.write(
        """\end{tabular}
\end{table}
"""
    )

    #Jaccard stats

    file.write("\nJaccard score statistics\n")
    file.write(
"""\\begin{table}[]
\\begin{tabular}{|l|l|}
\hline
t-statistic & p-value \\\\ \hline
"""
    )

    vals = lines[40].split(',')

    file.write("{} & {} \\\\ \hline\n".format(vals[0], vals[1].strip()))
    file.write(
"""\end{tabular}
\end{table}
"""
    )

    #Homogeneity stats

    file.write("\nHomogeneity score statistics\n")
    file.write(
"""\\begin{table}[]
\\begin{tabular}{|l|l|}
\hline
t-statistic & p-value \\\\ \hline
"""
    )

    vals = lines[46].split(',')

    file.write("{} & {} \\\\ \hline\n".format(vals[0], vals[1].strip()))
    file.write(
"""\end{tabular}
\end{table}
"""
    )

    #Rand stats

    file.write("\nRand score statistics\n")
    file.write(
"""\\begin{table}[]
\\begin{tabular}{|l|l|}
\hline
t-statistic & p-value \\\\ \hline
"""
    )

    vals = lines[52].split(',')

    file.write("{} & {} \\\\ \hline\n".format(vals[0], vals[1].strip()))
    file.write(
"""\end{tabular}
\end{table}
"""
    )

    #DBSCAN and OPTICS scores

    file.write("\nDBSCAN and OPTICS scores\n")
    file.write(
"""\\begin{table}[]
\\begin{tabular}{|l|l|l|l|}
\hline
Score  & Jaccard Score & Homogeneity Score & Rand Score \\\\ \hline
"""
    )

    dbscan_vals = lines[62].split(",")
    optics_vals = lines[65].split(",")
    file.write("DBSCAN & {} & {} & {} \\\\ \hline\n".format(dbscan_vals[0],dbscan_vals[1],dbscan_vals[2]))
    file.write("OPTICS & {} & {} & {} \\\\ \hline\n".format(optics_vals[0],optics_vals[1],optics_vals[2]))

    file.write(
"""\end{tabular}
\end{table}
"""
    )

    #DBSCAN and OPTICS noisy %

    file.write("\nDBSCAN and OPTICS scores\n")
    file.write(
"""\\begin{table}[]
\\begin{tabular}{|l|l|}
\hline
       & Noisy data (\%) \\\\ \hline
"""
    )

    file.write("DBSCAN & {} \\\\ \hline\n".format(lines[69].strip()))
    file.write("OPTICS & {} \\\\ \hline\n".format(lines[71].strip()))

    file.write(
"""\end{tabular}
\end{table}
"""
    )

    file.close()
    scores.close()
