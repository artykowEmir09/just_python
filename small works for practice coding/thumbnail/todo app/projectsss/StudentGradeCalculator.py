print("===== Student Grade Calculator =====")

name = input("Enter your name: ")

math = float(input("Enter Math grade: "))
python = float(input("Enter Python grade: "))
english = float(input("Enter English grade: "))

average = (math + python + english) / 3

print("\n===== Result =====")
print(f"Student: {name}")
print(f"Average: {average:.2f}")

if average >= 90:
    print("Grade: A")
elif average >= 80:
    print("Grade: B")
elif average >= 70:
    print("Grade: C")
elif average >= 60:
    print("Grade: D")
else:
    print("Grade: F")