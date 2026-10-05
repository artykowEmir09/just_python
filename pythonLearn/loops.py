# numbers = []

# for x in range(5):
#     number = int(input("Enter a number: "))
#     numbers.append(number)

# print(numbers)
numbers = []

amount = int(input("How many numbers do you want to enter? "))

for x in range(amount):
    number = int(input("Enter a number: "))
    numbers.append(number)

print(numbers)