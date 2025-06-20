# run_all.py

# Main script to run both variants of the Robust Selection Problem:
# - Min-Max (robust against worst-case costs)
# - Max-Min (robust against best-case costs)
#
# This script executes both minmax.main.py and maxmin.main.py to perform batch evaluations and store results (CSV +
# pickle).
# Make sure the structure is:
# selection_problem/
# ├── minmax/__init__.py
# ├── minmax/main.py
# ├── minmax/plot.py
# ├── minmax/exact_solution.py
# ├── minmax/primal_rounding.py
# ├── maxmin/__init__.py
# ├── maxmin/main.py
# ├── maxmin/plot.py
# ├── maxmin/exact_solution.py
# ├── maxmin/primal_rounding.py
# ├── results/
# ├── utils.py
# ├── run_all.py
#
# Adjust settings (e.g., number of runs) in the respective main files and the fixed costs in the utils file.

import subprocess

PLOT_RESULTS = True  # Set to False if you don't want to create plots

if __name__ == "__main__":
    print("Min-Max version:\n")
    subprocess.run(["python", "minmax/main.py"], check=True)

    if PLOT_RESULTS:
        subprocess.run(["python", "minmax/plot.py"], check=True)

    print("\n✅ Finished Min-Max version.\n")

    print("Max-Min version:\n")
    subprocess.run(["python", "maxmin/main.py"], check=True)

    if PLOT_RESULTS:
        subprocess.run(["python", "maxmin/plot.py"], check=True)

    print("\n✅ Finished Max-Min version.")
