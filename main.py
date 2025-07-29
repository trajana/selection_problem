# main.py

# Main script to run the robust selection problem with the min-max or max-min criterion.

# Calls functions from other modules to compute the exact and heuristic solutions.
# Adjustable parameters: n (total items), p (items to select), k (scenarios), c_range (random cost range), EXPORT_CSV,
# num_runs (number of runs in loop), n_values (for multiple n values), PLOT.
# Choose between fixed or random cost vectors. If using fixed costs, define them in utils.py (get_fixed_costs).
# TODO: Notation mit Arbeit abgleichen / überprüfen

import pickle
import math  # For rounding calculations
import os
from datetime import datetime
from exact_solution_minmax import solve_exact_robust_selection_minmax
from exact_solution_maxmin import solve_exact_robust_selection_maxmin
from primal_rounding_minmax import solve_primal_rounding_minmax
from primal_rounding_maxmin import solve_primal_rounding_maxmin
from utils import (get_fixed_costs, get_random_costs, print_costs, cost_matrix_to_dict,
                   print_all_results_from_pkl)

ALGORITHM_DISPATCH = {
    "primal_minmax": {
        "algorithm": "Primal Rounding",
        "type": "minmax",
        "function": solve_primal_rounding_minmax
    },
    "primal_maxmin": {
        "algorithm": "Primal Rounding",
        "type": "maxmin",
        "function": solve_primal_rounding_maxmin
    },
    # todo: Add future algorithms
}

# Base data TODO: Adjust as needed
ALGORITHMS = ["primal_maxmin"]  # Choose all approximation algorithms that should be run. Available:
# "primal_minmax", "primal_maxmin"
var_param = "n"  # x-axis for the plot, can be "n" or "k" or "p"
if var_param == "n":
    var_values = [2, 4, 6, 8, 10, 12, 14]
    #[2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70]
    fixed_k = 2
    fixed_p = None  # p = n//2, so no need to set it explicitly
elif var_param == "k":
    fixed_n = 20
    var_values = [1, 2, 5, 10, 20, 30, 50, 70, 100]
    fixed_p = fixed_n // 2
elif var_param == "p":
    fixed_n = 70
    fixed_k = 5
    var_values = list(range(2, fixed_n, 2))  # p in steps of 2 from 2 to n-2
c_range = 100  # Range for random costs
num_runs = 100  # Number of runs for the loop
USE_FIXED_COSTS = False  # True = use fixed costs from utils.py (align n and k with the fixed cost matrix, False =
# use random costs
PLOT = True  # Set True to enable plotting

if __name__ == "__main__":
    # Create unique results subfolder based on algorithm, k, and timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    RESULT_DIR = f"results/{var_param}_{timestamp}"
    os.makedirs(RESULT_DIR, exist_ok=True)

    for algorithm in ALGORITHMS:
        algo_info = ALGORITHM_DISPATCH.get(algorithm)
        if not algo_info:
            print(f"Unknown algorithm '{algorithm}', skipping.")
            continue

        criterion = algo_info["type"]
        solve_function = algo_info["function"]

        algo_result_dir = os.path.join(RESULT_DIR, algorithm)
        os.makedirs(algo_result_dir, exist_ok=True)

        all_results = []

        for a in var_values:
            if var_param == "n":
                n = a
                p = n // 2 if fixed_p is None else fixed_p
                k = fixed_k
            elif var_param == "k":
                n = fixed_n
                p = fixed_p
                k = a
            elif var_param == "p":
                n = fixed_n
                p = a
                k = fixed_k

            print(f"\n=== Running experiments for n = {n}, p = {p}, k = {k} ===")

            for run in range(num_runs):
                print(f"\n=== Running {algorithm} ({criterion}) for run {run + 1} ===")

                # Choose cost type
                if USE_FIXED_COSTS:
                    c = get_fixed_costs(n, k)
                else:
                    c = get_random_costs(n, k, c_range)

                # Print costs
                print("--- Cost matrix ---")
                print_costs(c)
                costs = cost_matrix_to_dict(c)  # Convert costs to a dictionary with keys (s, i)
                print("--- Cost dictionary ---")
                print(costs)
                # For CSV export, flatten the costs
                flat_costs = [costs[(s + 1, i + 1)] for s in range(k) for i in range(n)]

                # Exact problem
                if criterion == "minmax":
                    print("\n--- Exact robust solution Min-Max ---")
                    obj_val_exact_minmax, x_val_exact_minmax = solve_exact_robust_selection_minmax(costs, n, p, k)
                    obj_val_exact = obj_val_exact_minmax
                    x_vector_exact = [1 if val > 0.5 else 0 for val in x_val_exact_minmax]  # Rundungsabweichung bei
                    # binären Variablen abfangen
                    print(f"Selected items (exact): {x_vector_exact}")
                    print(f"Objective value: {obj_val_exact:.2f}")
                elif criterion == "maxmin":
                    print("\n--- Exact robust solution Max-Min ---")
                    obj_val_exact_maxmin, x_val_exact_maxmin = solve_exact_robust_selection_maxmin(costs, n, p, k)
                    obj_val_exact = obj_val_exact_maxmin
                    x_vector_exact = [1 if val > 0.5 else 0 for val in x_val_exact_maxmin]

                result = solve_function(costs, n, p, k)

                if algorithm == "primal_minmax":
                    print("\n--- Primal Rounding Min-Max ---")
                    obj_val_primal, x_val_primal_frac, x_vector_primal_rounded, obj_val_primal_lp, tau = result
                    x_vector_primal_frac = [round(val, 2) for val in x_val_primal_frac]
                    fractional_count = sum(1 for val in x_val_primal_frac if 0.0001 < val < 0.9999)
                    fractional_ratio = fractional_count / n  # TODO: Evtl. rausnehmen
                    print(f"Fractional values: {x_vector_primal_frac}")
                    print(f"Fractional variables: {fractional_count} out of {n} ({fractional_ratio:.2%})")
                    print(f"Selected items (rounded): {x_vector_primal_rounded}")
                    print(f"Objective value: {obj_val_primal:.2f}")

                    # Ratio of primal to exact objective value
                    ratio_primal_opt = obj_val_primal / obj_val_exact if obj_val_exact != 0 else 0
                    # Integrality gap and rounding gap calculations
                    integrality_gap_primal = obj_val_exact / obj_val_primal_lp if obj_val_primal_lp != 0 else 0
                    rounding_gap_primal = obj_val_primal / obj_val_primal_lp if obj_val_primal_lp != 0 else 0
                    # Approximation guarantee
                    approximation_guarantee = min(k, n - p + 1)
                    a_posteriori_bound = 1 / tau if tau > 0 else float('inf')
                    opt_lp_div_alg = obj_val_primal / obj_val_primal_lp if obj_val_primal != 0 else float('inf')
                    print(f"Approximation ratio: {ratio_primal_opt:.2f}")
                    print(f"Integrality gap: {integrality_gap_primal:.2f}")
                    print(f"Rounding gap (rounded / LP): {rounding_gap_primal:.2f}")
                    print(f"Approximation guarantee: min(k, n - p + 1) = {approximation_guarantee}")
                    print(f"A-posteriori bound: ALG ≤ (1/τ) · OPT → 1/τ = {a_posteriori_bound:.2f}")

                    # Store results
                    all_results.append({
                        "algorithm": algorithm,
                        "varying_param": a,
                        "n": n,
                        "p": p,
                        "k": k,
                        "run": run + 1,
                        "obj_exact": obj_val_exact,
                        "obj_primal_lp": obj_val_primal_lp,
                        "obj_primal": obj_val_primal,
                        "ratio_primal_opt": ratio_primal_opt,
                        "tau": tau,
                        "a_posteriori_bound": a_posteriori_bound,
                        "opt_lp_div_alg": opt_lp_div_alg,
                        "approximation_guarantee": approximation_guarantee,
                        "integrality_gap": integrality_gap_primal,
                        "rounding_gap": rounding_gap_primal,
                        "fractional_count": fractional_count,
                        "fractional_ratio": fractional_ratio,
                        "x_vector_exact": x_vector_exact,
                        "x_vector_primal_frac": x_vector_primal_frac,
                        "x_vector_primal_rounded": x_vector_primal_rounded,
                        "flat_costs": flat_costs
                    })

                elif algorithm == "primal_maxmin":
                    print("\n--- Primal Rounding Max-Min ---")
                    (obj_val_primal, x_vector_primal_rounded, obj_val_primal_lp, x_val_primal_frac, sorted_x_vals) = result
                    print(f"Fractional values: {x_val_primal_frac}")
                    print(f"Selected items (rounded): {x_vector_primal_rounded}")
                    print(f"Objective value: {obj_val_primal:.2f}")
                    print(f"LP objective (upper bound): {obj_val_primal_lp:.2f}")

                    # Ratio of primal to exact objective value
                    ratio_primal_opt = obj_val_primal / obj_val_exact if obj_val_exact != 0 else 0
                    integrality_gap_primal = obj_val_exact / obj_val_primal_lp if obj_val_primal_lp != 0 else 0
                    rounding_gap_primal = obj_val_primal / obj_val_primal_lp if obj_val_primal_lp != 0 else 0
                    print(f"Approximation ratio: {ratio_primal_opt:.2f}")
                    print(f"Integrality gap: {integrality_gap_primal:.2f}")
                    print(f"Rounding gap (rounded / LP): {rounding_gap_primal:.2f}")
                    # Approximation guarantee
                    r = math.ceil(len(sorted_x_vals) / p)
                    approximation_guarantee = 1 / r
                    print(f"Approximation guarantee: {approximation_guarantee:.3f} (r = {r:.2f})")

                    # Store results
                    all_results.append({
                        "algorithm": algorithm,
                        "varying_param": a,
                        "n": n,
                        "p": p,
                        "k": k,
                        "run": run + 1,
                        "obj_exact": obj_val_exact,
                        "obj_primal_lp": obj_val_primal_lp,
                        "obj_primal": obj_val_primal,
                        "ratio_primal_opt": ratio_primal_opt,
                        "integrality_gap": integrality_gap_primal,
                        "rounding_gap": rounding_gap_primal,
                        "x_vector_exact": x_vector_exact,
                        "x_vector_primal_frac": x_val_primal_frac,
                        "x_vector_primal_rounded": x_vector_primal_rounded,
                        "flat_costs": flat_costs,
                    })

        # Save results as pickle file
        with open(os.path.join(algo_result_dir, f"all_results_{criterion.lower()}.pkl"), "wb") as f:
            pickle.dump(all_results, f)
        print(f"Results for {algorithm} saved in {algo_result_dir} ")

        # View all results from a .pkl file like a CSV TODO: Löschen, wenn nicht mehr benötigt (auch in utils.py)
        print_all_results_from_pkl(os.path.join(algo_result_dir, f"all_results_{criterion.lower()}.pkl"))

        # Optional: Plot results
        if PLOT:
            from plot import (plot_primal_rounding_only, plot_approximation_ratios_primal, plot_integrality_gap_primal,
                              plot_rounding_gap_primal, plot_fractional_variable_count)

            if algorithm == "primal_minmax":
                plot_primal_rounding_only(all_results, num_runs, var_param, output_dir=algo_result_dir)
                plot_approximation_ratios_primal(all_results, num_runs, k, output_dir=algo_result_dir)
                plot_integrality_gap_primal(all_results, num_runs, k, output_dir=algo_result_dir)
                plot_rounding_gap_primal(all_results, num_runs, k, output_dir=algo_result_dir)
                plot_fractional_variable_count(all_results, num_runs, k, output_dir=algo_result_dir)

            elif algorithm == "primal_maxmin":
                # hier Code für MAX-MIN hinzufügen
                pass
