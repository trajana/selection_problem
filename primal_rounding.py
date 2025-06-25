# primal_rounding.py

# Using Primal Rounding to approximate the Robust Selection Problem with discrete uncertainty and the min-max criterion.

# Description: There are n items with cost c[s,i]. The goal is to pick exactly p items such that the wost-case cost is
# minimized. The problem is formulated as a Mixed Integer Linear Program using the epigraph-reformulation. The
# x-Variable is then relaxed to a continuous variable and the solution is rounded to a feasible solution.

import gurobipy as gp
from gurobipy import GRB


def solve_primal_rounding(costs, n, p, N, criterion):  # function
    try:

        # Create optimization model
        m = gp.Model("primal_rounding_robust_selection")

        # Create variables
        x = m.addVars(range(1, n + 1), vtype=GRB.CONTINUOUS, lb=0, ub=1, name="x")  # Binary variable for selection
        z = m.addVar()  # Continuous variable for the worst-case cost

        # Set objective
        if criterion == "minmax":
            m.setObjective(z, GRB.MINIMIZE)
        elif criterion == "maxmin":
            m.setObjective(z, GRB.MAXIMIZE)

        # Add constraints
        m.addConstr(gp.quicksum(x[i] for i in range(1, n + 1)) == p, name="select_p_items")  # Select exactly p

        if criterion == "minmax":
            m.addConstrs(
                (gp.quicksum(costs[s, i] * x[i] for i in range(1, n + 1)) <= z for s in range(1, N + 1)),
                name="worst_case_cost")
        elif criterion == "maxmin":
            m.addConstrs(
                (gp.quicksum(costs[s, i] * x[i] for i in range(1, n + 1)) >= z for s in range(1, N + 1)),
                name="best_case_cost")
        else:
            raise ValueError(f"Invalid criterion: {criterion}")

        # Optimize model
        m.optimize()

        # Relaxed x-values
        x_val_primal_frac = {i: x[i].X for i in range(1, n + 1)}
        selected_items_primal = sorted(x_val_primal_frac.items(), key=lambda item: item[1], reverse=True)[:p]  # Select
        # top p items
        selected_indices_primal = [i for i, _ in selected_items_primal]  # Get indices of selected items
        x_val_primal_rounded = {i: (1 if i in selected_indices_primal else 0) for i in range(1, n + 1)}  # Binary vector

        # Post-solution checks and debug prints TODO: Danach wieder rausnehmen
        print("\n---Relaxed x-values (fractional):---")
        for i in range(1, n + 1):
            print(f"x[{i}] = {x_val_primal_frac[i]:.4f}")
        print("\n---Relaxed x-values (binary):---")
        for i in range(1, n + 1):
            print(f"x[{i}] = {x_val_primal_rounded[i]}")  # TODO: End of debug prints

        # Compute worst-case cost of rounded solution (results)
        if criterion == "minmax":
            obj_val_primal = max(
                sum(costs[s, i] for i in range(1, n + 1) if x_val_primal_rounded[i] == 1)
                for s in range(1, N + 1))  # Computes the maximum cost across all scenarios for the rounded solution
        else:
            obj_val_primal = min(
                sum(costs[s, i] for i in range(1, n + 1) if x_val_primal_rounded[i] == 1)
                for s in range(1, N + 1))  # Computes the minimum cost across all scenarios for the rounded solution

        # Debugging worst case cost  # TODO: Danach wieder rausnehmen
        print("\n--- Scenario costs (rounded solution): ---")
        scenario_costs = []
        for s in range(1, N + 1):
            cost_s = sum(costs[s, i] for i in range(1, n + 1) if x_val_primal_rounded[i] == 1)
            scenario_costs.append(cost_s)
            print(f"Scenario {s}: total cost = {cost_s}")
        print(f"\nMax scenario cost (should match obj_val_primal): {max(scenario_costs)}")
        print(f"Returned objective value (obj_val_primal): {obj_val_primal}")  # TODO: End of debug prints

        return obj_val_primal, x_val_primal_frac, x_val_primal_rounded

    # Error handling
    except gp.GurobiError as e:
        print(f"Error code {e.errno}: {e}")

    except AttributeError:
        print("Encountered an attribute error")
