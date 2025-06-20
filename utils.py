# utils.py

# Utility functions for the robust selection problem.

# Includes generation of fixed or random cost vectors, cost printing, and conversion to dictionary format.
# To use fixed costs, define scenario-specific cost vectors in get_fixed_costs().

import random
import csv
import pickle  # TODO: Remove nach debugging

# Fixed costs
def get_fixed_costs():
    return [
        [1, 200, 30, 40, 50],  # Scenario  TODO: Adjust as needed
        [5, 25, 35, 45, 55],   # Scenario 2
    ]

# Random costs
def get_random_costs(n, N, c_range=100):
    return [ [random.randint(1, c_range) for _ in range(n)] for _ in range(N) ]

# Print costs in a readable format
def print_costs(c):
    N = len(c)
    n = len(c[0])
    for s in range(1, N + 1):
        print(f"Scenario c[{s}]:")
        for i in range(1, n + 1):
            print(f" c[{s}][{i}] = {c[s - 1][i - 1]}")

# Transform cost matrix into dictionary format: (s, i): c
def cost_matrix_to_dict(c):
    return {(s + 1, i + 1): c[s][i] for s in range(len(c)) for i in range(len(c[0]))}

# Export results to csv file
def export_results_to_csv(results, n, p, N, export_filename_prefix="results"):
    cost_headers = [f"Costs_Scenario{s + 1}_Item{i + 1}" for s in range(N) for i in range(n)]
    csv_header = [
        "n", "p", "run", "obj_exact", "obj_primal", "ratio_primal_opt",
        "x_vector_exact", "x_vector_primal_frac", "x_vector_primal_rounded"
    ] + cost_headers

    filename = f"results/{export_filename_prefix}_n_{n}_p_{p}_N_{N}.csv"
    with open(filename, mode="w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_header)
        writer.writeheader()
        for result in results:
            if result["n"] != n:
                continue
            row = {
                "n": result["n"],
                "p": result["p"],
                "run": result["run"],
                "obj_exact": result["obj_exact"],
                "obj_primal": result["obj_primal"],
                "ratio_primal_opt": result["ratio_primal_opt"],
                "x_vector_exact": str(result["x_vector_exact"]),
                "x_vector_primal_frac": str(result["x_vector_primal_frac"]),
                "x_vector_primal_rounded": str(result["x_vector_primal_rounded"]),
            }
            for i, cost in enumerate(result["flat_costs"]):
                row[cost_headers[i]] = cost
            writer.writerow(row)
    print(f"✅ CSV saved for n = {n} to {filename}")

# View all results from a .pkl file like a CSV TODO: Löschen, wenn nicht mehr benötigt
def print_all_results_from_pkl(pkl_filename="all_results.pkl"):
    with open(pkl_filename, "rb") as f:
        all_results = pickle.load(f)

    all_results.sort(key=lambda x: (x["n"], x["run"]))

    header = [
        "n", "p", "run", "obj_exact", "obj_primal", "ratio_primal_opt",
        "x_vector_exact", "x_vector_primal_frac", "x_vector_primal_rounded"
    ]
    print("; ".join(header))

    for entry in all_results:
        row = [
            str(entry["n"]),
            str(entry["p"]),
            str(entry["run"]),
            f"{entry['obj_exact']:.2f}",
            f"{entry['obj_primal']:.2f}",
            f"{entry['ratio_primal_opt']:.4f}",
            str(entry["x_vector_exact"]),
            str(entry["x_vector_primal_frac"]),
            str(entry["x_vector_primal_rounded"])
        ]
        print("; ".join(row))  # End of .pkl debugging
