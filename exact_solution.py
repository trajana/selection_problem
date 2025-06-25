# exact_solution.py

# Robust Selection Problem with discrete uncertainty and using the min-max criterion.

# Description: There are n items with cost c[s,i]. The goal is to pick exactly p items such that the wost-case cost is
# minimized. The problem is formulated as a Mixed Integer Linear Program using the epigraph-reformulation.

import gurobipy as gp
from gurobipy import GRB

def solve_exact_robust_selection(costs, n, p, N, criterion):  # function
    try:

        # Create optimization model
        m = gp.Model("exact_robust_selection")

        # Create variables
        x = m.addVars(range(1, n + 1), vtype=GRB.BINARY, name="x")  # Binary variable for selection
        z = m.addVar()  # Continuous variable for the worst-case cost

        # Set objective
        if criterion == "minmax":
            m.setObjective(z, GRB.MINIMIZE)
        elif criterion == "maxmin":
            m.setObjective(z, GRB.MAXIMIZE)

        # Add constraints
        m.addConstr(gp.quicksum(x[i] for i in range(1, n + 1)) == p, name="select_p_items")  # Select exactly

        if criterion == "minmax":
            m.addConstrs(
                (gp.quicksum(costs[s, i] * x[i] for i in range(1, n + 1)) <= z for s in range(1, N + 1)),
                name="worst_case_cost")  # Worst-case cost constraints
        elif criterion == "maxmin":
            m.addConstrs(
                (gp.quicksum(costs[s, i] * x[i] for i in range(1, n + 1)) >= z for s in range(1, N + 1)),
                name="best_case_cost")  # Best-case cost constraints
        else:
            raise ValueError(f"Invalid criterion: {criterion}")

        # Optimize model
        m.optimize()

        # Post-solution checks and debug prints TODO: Danach wieder rausnehmen
        print("\n--- Debug: Selected item count ---")
        print(sum(x[i].X for i in range(1, n + 1)))  # sollte gleich p sein

        print("\n--- Debug: Scenario costs ---")
        for s in range(1, N + 1):
            cost_s = sum(costs[s, i] * x[i].X for i in range(1, n + 1))
            print(f"Scenario {s}: total cost = {cost_s}")  #TODO: Alle cost_s ≤ z

        print(f"Max scenario cost (z) = {m.ObjVal}")  # TODO: Wert von z Muss gleich dem höchsten cost_s sein
        # TODO: End of debug prints

        # Print results
        x_val_exact = {i: x[i].X for i in range(1, n + 1)}
        obj_val_exact = m.ObjVal # Wert von z
        return obj_val_exact, x_val_exact

        # Error handling
    except gp.GurobiError as e:
        print(f"Error code {e.errno}: {e}")

    except AttributeError:
        print("Encountered an attribute error")
