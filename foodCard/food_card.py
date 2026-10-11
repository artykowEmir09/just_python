

foods = []
prices = []
total = 0





while True:
    food = input("Enter a food to buy (q to quit): ")
    if food.lower() == "q":
        break
    
        price = float(input(f"Enter the price of the {food}: $  "))
        foods.append(food)
       

print("----- Your Cart -----")

for food in foods:
    print(food , end=" ")

for price in prices:
  


