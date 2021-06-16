import numpy as np

#Gathers data from results of individual datasets and saves them in result_comp directory
#The resulting files are used to perform T-test between algorithms by final_compare script

datasets = ["australian", "banknote", "breastcan",
            "diabetes", "german", "liver", "popfailures", "spambase", "wisconsin", "yeast6"]


j_file = open("./result_comp/jaccard_score.csv", 'w')
h_file = open("./result_comp/homogeneity_score.csv", 'w')
r_file = open("./result_comp/rand_score.csv", 'w')

j_file.write("Dataset,KMeans,Meanshift,DBSCAN,OPTICS\n")
h_file.write("Dataset,KMeans,Meanshift,DBSCAN,OPTICS\n")
r_file.write("Dataset,KMeans,Meanshift,DBSCAN,OPTICS\n")

for dset in datasets:

    # Load dataset

    file = open("./results/" + dset + "_results.csv")

    lines = file.readlines()

    kmeans = lines[23].split(',')
    meanshift = lines[26].split(',')
    dbscan = lines[62].split(',')
    optics = lines[65].split(',')

    j_file.write(dset + "," + kmeans[0] + "," + meanshift[0] +
                 "," + dbscan[0] + "," + optics[0] + "\n")
    h_file.write(dset + "," + kmeans[1] + "," + meanshift[1] +
                 "," + dbscan[1] + "," + optics[1] + "\n")
    r_file.write(dset + "," + kmeans[2] + "," + meanshift[2] +
                 "," + dbscan[2] + "," + optics[2] + "\n")


    file.close()


j_file.close()
h_file.close()
r_file.close()
