menu = {"pizza":30.0,
        "nachos":5.00,
        "fries": 2.50,
        "chips":  1.00,
        "protozel":3.50,
        "soda":  3.0,
        "lemonade":4.25,
        "popcorn": 6.00,}
cart = [    ]
total = 0
print("======== Menu ========")
for key , value in menu.items():
    print(f"{key:10}: RM {value:.2f}")
print("=======================")

while True:
    food = input("Select an item (q to quit): ").lower()
    if food == "q":
        break
    elif menu.get(food)is not None:
        cart.append(food)

print("======== Your order ========")    
for food in cart:
        total +=menu.get(food)
        print (food , end =" ")
print()
print(F"total is: Rm {total:.2f}")
print("=======================")