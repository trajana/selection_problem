# primal_rounding_maxmin.py

# Using Primal Rounding to approximate the Robust Selection Problem with discrete uncertainty and the max-min criterion.

# Description: There are n items with cost c[s,i]. Note that costs in the Max-Min variant become profits. For easier
# # execution the variable name will remain costs in the code. The goal is to pick exactly p items such that the
# wost-case profit is maximized. The problem is formulated as a Mixed Integer Linear Program using the
# epigraph-reformulation. The x-Variable is then relaxed to a continuous variable and the solution is rounded to a
# feasible solution.

import gurobipy as gp
from gurobipy import GRB
import random
from utils import build_chunks_with_fill, minimum_profit

def solve_primal_rounding_maxmin(costs, n, p, k): # function
    try:
        # Create optimization model
        m = gp.Model("primal_rounding_robust_selection_maxmin")

        # Create variables
        x = m.addVars(range(1, n + 1), vtype=GRB.CONTINUOUS, lb=0, ub=1, name="x")  # Binary variable for selection
        z = m.addVar()  # Continuous variable for the worst-case profit

        # Set objective
        m.setObjective(z, GRB.MAXIMIZE)

        # Add constraints
        m.addConstr(gp.quicksum(x[i] for i in range(1, n + 1)) == p, name="select_p_items")  # Select exactly p

        m.addConstrs(
            (gp.quicksum(costs[s, i] * x[i] for i in range(1, n + 1)) >= z for s in range(1, k + 1)),
            name="best_case_profit"
        )

        # Optimize model
        m.optimize()
        obj_val_primal_lp = m.ObjVal

        # Approximation procedure
        # Relaxed x-values
        x_val_primal_frac = [x[i].X for i in range(1, n + 1)]
        indexed_x_vals = list(enumerate(x_val_primal_frac, start=1))
        filtered_vals = [pair for pair in indexed_x_vals if pair[1] > 0.0]  # Filter out zero values
        sorted_x_vals = sorted(filtered_vals, key=lambda pair: pair[1], reverse=True)
        x_vector_primal_rounded = [0] * n  # Initialize binary vector

        # Create blocks of items (with length p)
        chunks = build_chunks_with_fill(sorted_x_vals, p)

        # Calculate minimum profit for each block and choose the best block (maximizing the minimum profit)
        best_block = max(chunks, key=lambda block: minimum_profit(block, costs, k))
        selected_indices = [i for i, _ in best_block]  # Get indices of selected items
        obj_val_primal = minimum_profit(best_block, costs, k)
        for i in selected_indices:
            x_vector_primal_rounded[i - 1] = 1  # Set selected items to 1 in the binary vector

        # Post-solution checks and debug prints TODO: Danach wieder rausnehmen
        print("Best block (rounded solution):", [i for i, _ in best_block])
        print("Worst-case profit of selected block:", obj_val_primal)
        print("Rounded primal solution vector:", x_vector_primal_rounded)
        # Todo End of debugging

        return obj_val_primal, x_vector_primal_rounded, obj_val_primal_lp, x_val_primal_frac, sorted_x_vals

    except gp.GurobiError as e:
        print(f"Gurobi Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
