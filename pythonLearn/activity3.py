from pyprover import *

# Define propositions
Rain, Wipers, Headlights = props(
    "Rain Wipers Headlights"
)

# Rule 1: If rain is detected, activate wipers
rule1 = Rain >> Wipers

# Rule 2: If wipers are activated, turn on headlights
rule2 = Wipers >> Headlights

# Current fact: Rain is detected
fact = Rain

# Derive the combined rule using Hypothetical Syllogism
combined_rule = proves(
    (rule1, rule2),
    Rain >> Headlights
)

# Prove that headlights must turn on
result = proves(
    (rule1, rule2, fact),
    Headlights
)

print("Rule 1:", rule1)
print("Rule 2:", rule2)
print("Current Fact:", fact)
print("Combined Rule Proven:", combined_rule)
print("Headlights Automatically Turn On:", result)