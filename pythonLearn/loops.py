# # numbers = []

# # for x in range(5):
# #     number = int(input("Enter a number: "))
# #     numbers.append(number)

# # print(numbers)
# numbers = []

# amount = int(input("How many numbers do you want to enter? "))

# for x in range(amount):
#     number = int(input("Enter a number: "))
#     numbers.append(number)

# print(numbers)

number = int(input("Enter a number: "))

for x in range(1, 101):
    print(number, "x", x, "=", number * x)