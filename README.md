# README.md

# Approximation Algorithms for the Robust Selection Problem

This repository provides a modular Python implementation for solving the **Robust Selection Problem** under discrete 
uncertainty using a variety of **approximation algorithms**.

SELECTION PROBLEM: The goal is to select exactly `p` items out of `n`, such that performance is robust across multiple 
cost scenarios.

The current implementation supports:

- **Exact solution**
- **Primal Rounding**
- Two robust criteria:
  - **Min-Max**
  - **Max-Min**

---

## Project Structure

<pre>selection_problem/
├── minmax/ # Min-Max experiments
│ ├── main.py
│ ├── exact_solution.py
│ ├── primal_rounding.py
│ ├── plot.py
│ └── init.py
├── maxmin/ # Max-Min experiments
│ ├── main.py
│ ├── exact_solution.py
│ ├── primal_rounding.py
│ ├── plot.py
│ └── init.py
├── utils.py
├── run_all.py # Runs all experiments and generates plots
├── results/ # Stores result files
├── requirements.txt
└── README.md</pre>

---

## Running the Code

To run all experiments (both Min-Max and Max-Min variants) and generate result files and plots:

python run_all.py

This script will:
 - Execute both minmax/main.py and maxmin/main.py 
 - Generate .pkl and .csv result files 
 - Optionally generate plots (if PLOT_RESULTS = True in run_all.py)

You can change the following settings in the respective main.py files:
 - n, p: number of items and selection size 
 - N: number of cost scenarios 
 - c_range: range of random costs 
 - EXPORT_CSV: whether to save results as CSV 
 - RUN_LOOP: whether to run multiple repetitions 
 - num_runs: number of repetitions (if RUN_LOOP = True)
 - n_values: list of n-values to test

You can switch between fixed and random cost matrices in both main.py files: Activate get_fixed_costs() or 
c = get_random_costs(n, N, c_range)
To define your own fixed cost matrix, modify the get_fixed_costs() function in utils.py. The  matrix should be of size 
n x N.

If you run the main scripts directly (without run_all.py), you can generate the corresponding plots separately:

python minmax/plot.py
python maxmin/plot.py

Note: To generate plots, make sure to first run the corresponding main.py script with RUN_LOOP = True, which creates the 
necessary .pkl result file.

# Dependencies

Install required packages via:

pip install -r requirements.txt

Also install Gurobi Optimizer and activate a license. 

# Notes

Code written in Python 3.12

# Contact

Author: Trajana Erlenberg
