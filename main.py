# main.py

# Main script to run the robust selection problem with the min-max or max-min criterion.

# Calls functions from other modules to compute the exact and heuristic solutions.
# Adjustable parameters: n (total items), p (items to select), N (scenarios), c_range (random cost range), EXPORT_CSV,
# num_runs (number of runs in loop), n_values (for multiple n values), PLOT.
# Choose between fixed or random cost vectors. If using fixed costs, define them in utils.py (get_fixed_costs).
# TODO: Notation mit Arbeit abgleichen / überprüfen

import pickle
import os
from datetime import datetime
from exact_solution import solve_exact_robust_selection  # import functions
from primal_rounding import solve_primal_rounding  # import functions
from utils import (get_fixed_costs, get_random_costs, print_costs, cost_matrix_to_dict, export_results_to_csv,
                   print_all_results_from_pkl)

# Base data TODO: Adjust as needed
CRITERION = "maxmin"  # Choose minmax or maxmin
N = 4  # Number of scenarios (discrete uncertainty sets)
c_range = 100  # Range for random costs
num_runs = 10  # Number of runs for the loop
USE_FIXED_COSTS = False  # True = use fixed costs from utils.py (align n and N with the fixed cost matrix, False =
# use random costs
n_values = [6, 10, 16, 20, 26, 30, 36, 40, 46, 50, 56, 60, 66, 70]  # List of n-values (no. of items) to evaluate
EXPORT_CSV = True  # Set True to enable CSV export
PLOT = True  # Set True to enable plotting

# Create unique results subfolder based on criterion, N, and timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
RESULT_DIR = f"results/{CRITERION}_N{N}_{timestamp}"
os.makedirs(RESULT_DIR, exist_ok=True)

if __name__ == "__main__":
    all_results = []

    for n in n_values:
        p = n // 2
        print(f"\n=== Running experiments for n = {n}, p = {p} ===")

        for run in range(num_runs):
            print(f"\n--- Run {run + 1} ---")

            # Choose cost type
            if USE_FIXED_COSTS:
                c = get_fixed_costs(n, N)
            else:
                c = get_random_costs(n, N, c_range)

            # Print costs
            # print("--- Raw cost matrix in main.py ---")  #TODO: Überprüft - rausnehmen
            # for row in c:  #TODO: Überprüft - rausnehmen
            #    print(row)  #TODO: Überprüft - rausnehmen
            print("--- Cost matrix ---")
            print_costs(c)
            costs = cost_matrix_to_dict(c)  # Convert costs to a dictionary with keys (s, i)
            print("--- Cost dictionary ---")
            print(costs)
            # For CSV export, flatten the costs
            flat_costs = [costs[(s + 1, i + 1)] for s in range(N) for i in range(n)]

            print("\n--- Exact robust solution ---")
            obj_val_exact, x_val_exact = solve_exact_robust_selection(costs, n, p, N, criterion=CRITERION)
            # print("\n--- Debug 1 ---")  # TODO: Überprüft - rausnehmen
            # print(obj_val_exact, x_val_exact)   # TODO: Überprüft - rausnehmen
            x_vector_exact = [1 if val > 0.5 else 0 for val in x_val_exact]  # Rundungsabweichung bei binären Variablen abfangen
            # print("\n--- Debug 3 ---")  # TODO: Überprüft  - rausnehmen
            # print(x_val_exact, x_vector_exact)  # TODO: Überprüft  - rausnehmen
            print(f"Selected items (exact): {x_vector_exact}")
            print(f"Objective value: {obj_val_exact:.2f}")

            print("\n--- Primal Rounding ---")
            obj_val_primal, x_val_primal_frac, x_vector_primal_rounded, obj_val_primal_lp = (
                solve_primal_rounding(costs, n, p, N, criterion=CRITERION))
            # print("\n--- Debug 1 ---")  # TODO: Überprüft  - rausnehmen
            # print(x_val_primal_frac, x_val_primal_rounded)  # TODO: Überprüft  - rausnehmen
            # print("\n--- Debug 2 ---") # TODO: Überprüft  - rausnehmen
            # print(f"Number of selected items: {sum(x_val_primal_rounded.values())} (should be {p})")  # TODO: Überprüft  - rausnehmen (sollte == p sein)
            x_vector_primal_frac = [round(val, 2) for val in x_val_primal_frac]
            # print("\n--- Debug 3 ---")  # TODO: Überprüft  - rausnehmen
            # print(x_val_primal_rounded, x_vector_primal_rounded)  # TODO: Überprüft  - rausnehmen
            fractional_count = sum(1 for val in x_val_primal_frac if 0.0001 < val < 0.9999)
            fractional_ratio = fractional_count / n  # TODO: Evtl. rausnehmen
            print(f"Fractional values: {x_vector_primal_frac}")
            print(f"Fractional variables: {fractional_count} out of {n} ({fractional_ratio:.2%})")
            print(f"Selected items (rounded): {x_vector_primal_rounded}")
            print(f"Objective value: {obj_val_primal:.2f}")

            # Ratio of primal to exact objective value
            ratio_primal_opt = obj_val_primal / obj_val_exact if obj_val_exact != 0 else 0
            integrality_gap_primal = obj_val_primal_lp / obj_val_exact if obj_val_exact != 0 else 0
            rounding_gap_primal = obj_val_primal / obj_val_primal_lp if obj_val_primal_lp != 0 else 0
            print(f"Approximation ratio: {ratio_primal_opt:.2f}")
            print(f"Integrality gap (LP / OPT): {integrality_gap_primal:.2f}")
            print(f"Rounding gap (rounded / LP): {rounding_gap_primal:.2f}")

            print("\n--- Summary ---")
            print("\nExact robust solution:")
            print(f"Selected items: {x_vector_exact}")
            print(f"Objective value: {obj_val_exact:.2f}")
            print("\nPrimal Rounding:")
            print(f"Fractional values: {x_vector_primal_frac}")
            print(f"Selected items: {x_vector_primal_rounded}")
            print(f"Objective value: {obj_val_primal:.2f}")
            print(f"Ratio of primal rounding to OPT: {ratio_primal_opt:.2f}")

            # Store results
            all_results.append({
                "n": n,
                "p": p,
                "run": run + 1,
                "obj_exact": obj_val_exact,
                "obj_primal_lp": obj_val_primal_lp,
                "obj_primal": obj_val_primal,
                "ratio_primal_opt": ratio_primal_opt,
                "integrality_gap": integrality_gap_primal,
                "rounding_gap": rounding_gap_primal,
                "fractional_count": fractional_count,
                "fractional_ratio": fractional_ratio,
                "x_vector_exact": x_vector_exact,
                "x_vector_primal_frac": x_vector_primal_frac,
                "x_vector_primal_rounded": x_vector_primal_rounded,
                "flat_costs": flat_costs
            })

        # Optional: Also export as CSV
        if EXPORT_CSV:
            export_results_to_csv(all_results, n, p, N, export_filename_prefix=f"{RESULT_DIR}/results_{CRITERION}")

    # Save results as pickle file
    with open(f"{RESULT_DIR}/all_results_{CRITERION}.pkl", "wb") as f:
        pickle.dump(all_results, f)
    print(f"\n✅ All results saved to all_results_{CRITERION}.pkl")

    # View all results from a .pkl file like a CSV TODO: Löschen, wenn nicht mehr benötigt (auch in utils.py &
    # from utils import)
    print_all_results_from_pkl(f"{RESULT_DIR}/all_results_{CRITERION}.pkl")

    # Optional: Plot results
    if PLOT:
        from plot import (plot_approximation_ratios_primal, plot_gaps_primal, plot_histogram_of_xvals)
        plot_approximation_ratios_primal(CRITERION, num_runs, N, output_dir=RESULT_DIR)
        plot_gaps_primal(CRITERION, num_runs, N, output_dir=RESULT_DIR)

        # Histogram
        n_to_xvals = {}
        n_to_max_frac_count = {}
        for entry in all_results:
            n = entry["n"]
            xvals = entry["x_vector_primal_frac"]
            frac_count = entry["fractional_count"]
            n_to_xvals.setdefault(n, []).extend(xvals)
            n_to_max_frac_count[n] = max(n_to_max_frac_count.get(n, 0), frac_count)
        plot_histogram_of_xvals(n_to_xvals, output_dir=RESULT_DIR, n_to_max_frac_count=n_to_max_frac_count)

pn_ratios = set(entry["p"] / entry["n"] for entry in all_results)
print(f"p/n values in results: {pn_ratios}")