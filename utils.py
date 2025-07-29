# utils.py

# Utility functions for the robust selection problem.

# Includes generation of fixed or random cost vectors, cost printing, and conversion to dictionary format.
# To use fixed costs, define scenario-specific cost vectors in get_fixed_costs().

import random
import pandas as pd
import pickle  # TODO: Remove nach debugging


# Fixed costs
def get_fixed_costs(n=None, k=None):
    fixed_costs = [
        [5, 4, 3, 6],  # Scenario  TODO: Adjust as needed
        [3, 6, 3, 2]   # Scenario 2
    ]

    if k is not None and k != len(fixed_costs):
        raise ValueError(f"k = {k}, but fixed costs have {len(fixed_costs)} rows")
    if n is not None and n != len(fixed_costs[0]):
        raise ValueError(f"n = {n}, but fixed costs have {len(fixed_costs[0])} columns")

    return fixed_costs


# Random costs
def get_random_costs(n, k, c_range=100):
    return [[random.randint(1, c_range) for _ in range(n)] for _ in range(k)]


# Print costs in a readable format
def print_costs(c):
    k = len(c)
    n = len(c[0])
    for s in range(1, k + 1):
        print(f"Scenario c[{s}]:")
        for i in range(1, n + 1):
            print(f" c[{s}][{i}] = {c[s - 1][i - 1]}")


# Transform cost matrix into dictionary format: (s, i): c
def cost_matrix_to_dict(c):
    return {(s + 1, i + 1): c[s][i] for s in range(len(c)) for i in range(len(c[0]))}


# View all results from a .pkl in a table TODO: Löschen, wenn nicht mehr benötigt
def print_all_results_from_pkl(pkl_path):
    with open(pkl_path, "rb") as f:
        all_results = pickle.load(f)
    # Convert the list of dictionaries into a pandas DataFrame for tabular display
    df = pd.DataFrame(all_results)
    # Configure pandas to show all columns and unlimited width in the console output
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    # Print the DataFrame without the row index
    print(df.to_string(index=False))


def build_chunks_with_fill(sorted_x_vals, p):
    def chunk_into_p(lst, p):
        return [lst[i:i + p] for i in range(0, len(lst), p)]

    chunks = chunk_into_p(sorted_x_vals, p)

    if len(chunks[-1]) < p:
        remainder = chunks.pop()
        remaining_slots = p - len(remainder)

        used_items = set(remainder)
        pool = [item for chunk in chunks for item in chunk if item not in used_items]

        if len(pool) >= remaining_slots:
            remainder += random.sample(pool, remaining_slots)
        else:
            raise ValueError("Not enough items to fill the final block.")

        chunks.append(remainder)

    return chunks


def minimum_profit(block, costs, k):
    block_indices = [i for i, _ in block]
    return min(sum(costs[s, i] for i in block_indices) for s in range(1, k + 1))
