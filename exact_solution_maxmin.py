# exact_solution_maxmin.py

# Robust Selection Problem with discrete uncertainty and using the Max-Min criterion.

# Description: There are n items with costs c[s,i]. Note that costs in the Max-Min variant become profits. For easier
# execution the variable name will remain costs in the code.  The goal is to pick exactly p items such that the
# wost-case profit is maximized. The problem is formulated as a Mixed Integer Linear Program using the
# epigraph-reformulation.

import gurobipy as gp
from gurobipy import GRB


def solve_exact_robust_selection_maxmin(costs, n, p, k):  # function
    try:

        # Create optimization model
        m = gp.Model("exact_robust_selection")

        # Create variables
        x = m.addVars(range(1, n + 1), vtype=GRB.BINARY, name="x")  # Binary variable for selection
        z = m.addVar()  # Continuous variable for the worst-case profit

        # Set objective
        m.setObjective(z, GRB.MAXIMIZE)

        # Add constraints
        m.addConstr(gp.quicksum(x[i] for i in range(1, n + 1)) == p, name="select_p_items")  # Select exactly p

        m.addConstrs(
            (gp.quicksum(costs[s, i] * x[i] for i in range(1, n + 1)) >= z for s in range(1, k + 1)),
            name="worst_case_profit")  # Worst-case profit constraints

        # Optimize model
        m.optimize()

        # Post-solution checks and debug prints TODO: Danach wieder rausnehmen
        print("\n--- Debug: Selected item count ---")
        print(sum(x[i].X for i in range(1, n + 1)))  # sollte gleich p sein

        print("\n--- Debug: Scenario costs ---")
        for s in range(1, k + 1):
            profit_s = sum(costs[s, i] * x[i].X for i in range(1, n + 1))
            print(f"Scenario {s}: total profit = {profit_s}")  # TODO: Alle cost_s ≤ z

        print(f"Min scenario profit (z) = {m.ObjVal}")  # TODO: Wert von z Muss gleich dem kleinsten profit_s sein
        # TODO: End of debug prints

        # Print results
        x_val_exact_maxmin = [x[i].X for i in range(1, n + 1)]
        obj_val_exact_maxmin = m.ObjVal  # Wert von z
        return obj_val_exact_maxmin, x_val_exact_maxmin

        # Error handling
    except gp.GurobiError as e:
        print(f"Error code {e.errno}: {e}")

    except AttributeError:
        print("Encountered an attribute error")
