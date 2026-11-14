from pyprover import *

Human, Mortal = props("Human Mortal")
x, socrates = terms("x socrates")

# Premise 1: All humans are mortal
premise1 = FA(x, Human(x) >> Mortal(x))

# Premise 2: Socrates is human
premise2 = Human(socrates)

# Conclusion: Socrates is mortal
conclusion = Mortal(socrates)

# Verify the conclusion
result = proves(
    (premise1, premise2),
    conclusion
)

print("Premise 1:", premise1)
print("Premise 2:", premise2)
print("Conclusion:", conclusion)
print("Is the conclusion proven?", result)