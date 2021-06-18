
import numpy as np
datasets = ["australian", "banknote", "breastcan",
            "diabetes", "german", "liver", "popfailures", "spambase", "wisconsin", "yeast6"]

for dset in datasets:

    scores = open("./results/" + dset + "_results.csv")
    file = open("./latex/" + dset + "_latex.txt", 'w')

    lines = scores.readlines()

    file.write("\n" + dset + "\n")
    # Kmeans scores


    file.write(
        """
\\begin{table}[h!]
\\centering
""")

    file.write("\\caption{\\label{")
    file.write("tab:{}-KMeansScores".format(dset))
    file.write("}KMeans wyniki}\n")

    file.write("""\\begin{tabular}{|l|l|l|l|}
\hline
Fold & Jaccard Score & Homogeneity Score & Rand Score \\\\ \\hline
""")

    for fold_id, line in enumerate(lines[7:12]):
        vals = line.split(',')
        file.write("{} & {} & {} & {} \\\\ \\hline \n".format(
            fold_id+1, vals[0], vals[1], vals[2]))

    file.write(
        "\\end{tabular}\n\\end{table}\n"
    )

 
    #Meanshift scores

    file.write(
        """
\\begin{table}[h!]
\\centering
""")


    file.write("\\caption{\\label{")
    file.write("tab:{}-MeanshiftScores".format(dset))
    file.write("}Meanshift wyniki}")

    file.write("""
\\begin{tabular}{|l|l|l|l|}
\hline
Fold & Jaccard Score & Homogeneity Score & Rand Score \\\\ \\hline
""")

    for fold_id, line in enumerate(lines[14:19]):
        vals = line.split(',')
        file.write("{} & {} & {} & {} \\\\ \\hline \n".format(
            fold_id+1, vals[0], vals[1], vals[2]))

    file.write(
        "\\end{tabular}\n\\end{table}\n"
    )

       # Average

    file.write(
        """
\\begin{table}[h!]
\\centering
"""
    )

    file.write("\\caption{\\label{")
    file.write("tab:{}-Average".format(dset))
    file.write("}Uśrednione wyniki (z odch. std.))}")

    file.write("""
\\begin{tabular}{|l|l|l|l|}
\hline
Algorithm & Jaccard Score & Homogeneity Score & Rand Score \\\\ \\hline
""")

    vals = lines[23].split(',')
    stds = lines[31].split(',')

    file.write("KMeans & {} ({}) & {} ({}) & {} ({}) \\\\ \\hline \n".format(
        vals[0], stds[0], vals[1], stds[1], vals[2], stds[2]))

    vals = lines[26].split(',')
    stds = lines[34].split(',')

    file.write("MeanShift & {} ({}) & {} ({}) & {} ({}) \\\\ \\hline \n".format(
        vals[0], stds[0], vals[1], stds[1], vals[2], stds[2]))

    file.write(
        "\\end{tabular}\n\\end{table}\n"
    )

    #stats

    file.write(
"""\n\\begin{table}[h!]
\\centering
""")

    file.write("\\caption{\\label{")
    file.write("tab:{}-Stats".format(dset))
    file.write("}Porównanie statystyczne KMeans i MeanShift}")

    file.write("""
\\begin{tabular}{|l|l|l|l|}
\hline
& Jaccard Score & Homogeneity Score & Rand Score \\\\ \hline
"""
    )

    jacc_vals = lines[40].split(',')
    homo_vals = lines[46].split(',')
    rand_vals = lines[52].split(',')
    
    file.write("t-statistic & {} & {} & {} \\\\ \hline\n".format(jacc_vals[0], homo_vals[0], rand_vals[0]))
    file.write("p-value & {} & {} & {} \\\\ \hline\n".format(jacc_vals[1].strip(), homo_vals[1].strip(), rand_vals[1].strip()))
    
    file.write(
        "\\end{tabular}\n\\end{table}\n"
    )

    #DBSCAN and OPTICS scores

    file.write(
"""\n\\begin{table}[h!]
\\centering
""")

    file.write("\\caption{\\label{")
    file.write("tab:{}-Optics&DBScan".format(dset))
    file.write("}Wyniki uzyskane przez DBScan i OPTICS}")

    file.write("""
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
        "\\end{tabular}\n\\end{table}\n"
    )

    #DBSCAN and OPTICS noisy %

    file.write(
"""\n\\begin{table}[h!]
\\centering
""")

    file.write("\\caption{\\label{")
    file.write("tab:{}-Noisy".format(dset))
    file.write("}Procent wzorców oznaczonych jako zaszumione przez DBScan i OPTICS}")

    file.write("""
\\begin{tabular}{|l|l|}
\hline
       & Noisy data (\%) \\\\ \hline
"""
    )

    file.write("DBSCAN & {} \\\\ \hline\n".format(lines[69].strip()))
    file.write("OPTICS & {} \\\\ \hline\n".format(lines[71].strip()))

    file.write(
        "\\end{tabular}\n\\end{table}\n"
    )

    file.close()
    scores.close()
