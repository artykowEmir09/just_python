name = input("Enter your name: ")
age = int(input("Enter your age: "))
university = input("Enter your university: ")

print("\n--- Student Information ---")
print("Name:", name)
print("Age:", age)
print("University:", university)

if age >= 18:
    print("You are an adult.")
else:
    print("You are under 18.")