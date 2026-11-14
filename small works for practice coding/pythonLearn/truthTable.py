import pandas as pd
from itertools import product

# Generate all possible truth-value combinations
combinations = list(product([True, False], repeat=3))

# Store the results
data = []

for P, Q, R in combinations:

    # Expression 1: P OR (NOT Q AND R)
    expr1 = P or ((not Q) and R)

    # Expression 2: (P implies Q) AND NOT R
    expr2 = ((not P) or Q) and (not R)

    data.append({
        "P": P,
        "Q": Q,
        "R": R,
        "Expression 1": expr1,
        "Expression 2": expr2
    })

# Create the truth table
df = pd.DataFrame(data)

print("Truth Table:")
print(df.to_string(index=False))