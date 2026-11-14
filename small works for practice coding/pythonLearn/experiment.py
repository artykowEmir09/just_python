from pyprover import *

ConflictingMeeting, CannotSchedule = props(
    "ConflictingMeeting CannotSchedule"
)

# Premises
premise1 = ConflictingMeeting >> CannotSchedule
premise2 = ConflictingMeeting

# Conclusion
conclusion = CannotSchedule

# Verify using Modus Ponens
result = proves(
    (premise1, premise2),
    conclusion
)

print("Premise 1:", premise1)
print("Premise 2:", premise2)
print("Conclusion:", conclusion)
print("Is the conclusion proven?", result)