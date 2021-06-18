# msi_clustering
Comparing clustering algorihms in binary clustering problems.

# Usage
run test_dataset.py, then generate_compare.py and finally final_compare.py

# Description of scripts

test_dataset.py - performs testing of clustering algorithms on each dataset. Saves results to csv files in results directory.

generate_compare.py - uses data from resuls dir to create three csv files containing tables with scores from each dataset - one for each metric. Saves results in result_comp directory.

final-compare.py - Performs statistical comparison of algorithms for each metric using files in result_comp directory. Saves results in stat_compare directory.

generate_latex.py - Generates LateX tables from data in results directory.
