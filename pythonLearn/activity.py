from pyprover import *

# Define propositions
ConflictingMeeting, CannotSchedule = props(
    "ConflictingMeeting CannotSchedule"
)

# Premise 1: If there is a meeting conflict,
# the event cannot be scheduled.
premise1 = ConflictingMeeting >> CannotSchedule

# Premise 2: There is a meeting conflict.
premise2 = ConflictingMeeting

# Conclusion
conclusion = CannotSchedule

# Apply Modus Ponens
result = proves(
    (premise1, premise2),
    conclusion
)

print("Premise 1:", premise1)
print("Premise 2:", premise2)
print("Conclusion:", conclusion)
print("Proof successful:", result)