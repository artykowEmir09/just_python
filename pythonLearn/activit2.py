from pyprover import *

# Define predicates
Human, Mortal = props("Human Mortal")

# Define the variable and individual
x, socrates = terms("x socrates")

# Premise 1: All humans are mortal
premise1 = FA(x, Human(x) >> Mortal(x))

# Premise 2: Socrates is human
premise2 = Human(socrates)

# Conclusion: Socrates is mortal
conclusion = Mortal(socrates)

# Prove the conclusion
result = proves(
    (premise1, premise2),
    conclusion
)

print("Universal Rule:", premise1)
print("Fact:", premise2)
print("Conclusion:", conclusion)
print("Proof successful:", result)