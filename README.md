# README.md

# Approximation Algorithms for the Robust Selection Problem

This repository provides a modular Python implementation for solving the **Robust Selection Problem** under discrete 
uncertainty using a variety of **approximation algorithms**.

## Problem Description

SELECTION PROBLEM: The goal is to select exactly `p` items out of `n`, such that performance is robust across `k`
scenarios.

## Features

The current implementation supports:

- **Exact solution**
- **Primal Rounding** for two robust criteria:
  - **Min-Max**
  - **Max-Min**

## Project Structure

<pre>selection_problem/
├── main.py
├── exact_solution.py
├── primal_rounding.py
├── primal_rounding_maxmin.py
├── plot.py
├── utils.py
├── results/ # Stores result files
├── requirements.txt
└── README.md</pre>

## Running the Code

To run experiments for either the Min-Max or Max-Min criterion, open main.py and set the criterion at the top:

CRITERION = "minmax"  # or "maxmin"

Then, execute the script:

python main.py

This will:
- Run the experiment loop for the selected criterion
  - Generate result files:
  .pkl (for plots)
  .csv (if EXPORT_CSV = True)
- Automatically create a plot (if PLOT = True)

You can change the following settings (in main.py):
- CRITERION: "minmax" or "maxmin"
- n_values: list of item counts (n) to evaluate
- p = n // 2: number of items to select (calculated automatically)
- k: number of cost scenarios
- c_range: range of random costs (if not using fixed costs)
- USE_FIXED_COSTS: set to True to use predefined costs from utils.py
  - To define your own fixed cost matrix, modify the get_fixed_costs() function in utils.py. 
    The  matrix should be of size n x k.
- num_runs: how many repetitions to run for each setting
- EXPORT_CSV: whether to save .csv result files
- PLOT: whether to generate the plots in plot.py at the end

# Dependencies

Install required packages via:

pip install -r requirements.txt

Also install Gurobi Optimizer and activate a license. 

# Notes

Code written in Python 3.12

# Contact

Author: Trajana Erlenberg
