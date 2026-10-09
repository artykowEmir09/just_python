

foods = []
prices = []
total = 0
foodN1 = 0
real = 0

while True:
    food = input("Enter a food to buy (q to quit): ")
    if food.lower() == "q":
        break
    else:
        price = float(input(f"Enter the price of the {food}: $  "))
        foods.append(food)
        prices.append(price)

print("----- Your Cart -----")

for food in foods:
    print(food , end=" ")

for price in prices:
    total += price

print()
print(f"Your total is: ${total}")