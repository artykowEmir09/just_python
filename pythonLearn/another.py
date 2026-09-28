print("=== FUTURE SELF QUIZ ===")

name = input("What is your name? ")
age = int(input("How old are you? "))

goal = input("What is your biggest goal in life? ")
career = input("What career do you want? ")
country = input("Where do you want to live in the future? ")
money = int(input("How much money would you like to earn per month? "))

print("\n=== YOUR FUTURE ===")

print("Name:", name)
print("Current age:", age)
print("Biggest goal:", goal)
print("Dream career:", career)
print("Dream country:", country)
print("Target monthly income: $", money)

if age < 25:
    print("\nYo have plenty of time to build your future.")
elif age < 35:
    print("\nThis is a great time to focus on your career and goals.")
else:
    print("\nIt is never too late to change your direction.")

if money >= 10000:
    print("You have a very ambitious financial goal.")
elif money >= 5000:
    print("You have a strong financial goal.")
else:
    print("You are starting with a realistic financial target.")

print("\nKeep working toward the person you want to become!")