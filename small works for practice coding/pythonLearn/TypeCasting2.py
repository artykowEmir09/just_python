"""
# 🟢 Exercise 1 — String → Integer

# Create:

# age = "24"

# Convert age into an integer.

# Then print:

# 24
# <class 'int'>

# Use type() to verify it.

age = "24"

age = int(age)
print (age)
print(type(age))



# 🟢 Exercise 2 — String → Float

# Create:

# price = "19.99"

# Convert it into a float.

# Print the value and its type.

# Expected:

# 19.99
# <class 'float'>

price = "19.99"
price = float(price)
print (price)
print(type(price))



# 🟢 Exercise 3 — Integer → Float

# Create:

# number = 10

# Convert it into a float.

# Expected:

# 10.0
# <class 'float'>

x = 10
x = float(x)
print(x)
print(type ( x ))



# 🟢 Exercise 4 — Number → String

# Create:

# age = 24

# Convert it to a string.

# Then print:

# 24
# <class 'str'>

y = 24
y = str(y)
print(y)
print(type ( y ))




# 🟡 Exercise 5 — Two Conversions

# Create:

# q = "10"
# w = "5"

# Convert both to integers.

# Then calculate:

# 15

# Don't change the original values from strings.

q = "10"
w = "5"
q_int = int(q)
w_int = int(w)

result = q_int + w_int
print(result)
 


# 🟡 Exercise 6 — Calculate Price

# Create:

# price = "25.50"
# quantity = "4"

# Convert the appropriate values so that you can calculate:

# Total: 102.0

# The calculation must be:

# price x quantity

price = "25.50"
quantity = "4"
price = float(price) 
quantity = int(quantity)
total = price * quantity
print(f"Total: {total}")

# 🟡 Exercise 7 — Age in 5 Years
# Create:
# age = "24"
# Convert it to an integer and calculate the age 5 years from now.
# Expected:
# Current age: 24
# Age in 5 years: 29
age = "24"
age = int(age)
print (f"Current age: {age}")
print (f"Age in 5 years: {age + 5}")






# 🟠 Exercise 8 — Average
# Create:

# math = "85"
# programming = "92"
# english = "78"

# Convert the values so you can calculate their average.

# Expected:

# Average: 85.0
math = "85"
programming = "92"
english = "78"

math = float(math)
programming = float(programming)
english = float(english)
average = (math + programming + english)/3
print (f"Average : {average}")
 

# 🟠 Exercise 9 — Shopping Receipt
# Create:
# price = "1200"
# quantity = "2"
# discount = "0.10"
# Convert the values to appropriate numeric types.
# Calculate:
# Subtotal: 2400
# Discount: 240.0
# Final price: 2160.0

# Don't hard-code any of the results.



price = "1200"
quantity = "2"
discount = "0.10"
price = int (price )
quantity = int (quantity)
discount = float(discount)
subtotal = price * quantity
disc = subtotal * discount
final_price = subtotal - disc
print (f"Subtotal: {subtotal}") 
print (f"Discount: {disc}")
print (f"Final price: {final_price}")

"""



# 🔴 Exercise 10 — Challenge

# You receive this data as strings:

# product = "Laptop"
# price = "3000"
# quantity = "2"
# discount = "0.15"

# Your job is to convert the appropriate values and produce:

# ========== RECEIPT ==========

# Product: Laptop
# Price: 3000
# Quantity: 2
# Subtotal: 6000
# Discount: 900.0
# Final Price: 5100.0

# =============================
# Rules

# You must:

# Keep product as a string.
# Convert price.
# Convert quantity.
# Convert discount.
# Calculate everything using variables.
# Don't hard-code the calculated results.


product = "Laptop"
price = "3000"
quantity = "2"
discount = "0.15"

price = int (price )
quantity = int (quantity)
discount = float(discount)


subtotal = price * quantity
disc = subtotal * discount
final_price = subtotal - disc

print("========== RECEIPT ==========")
print(f"Product:      {product}")
print(f"Price:        {price}")
print(f"Quantity:     {quantity}")
print(f"Subtotal:     {subtotal}")
print(f"Discount:     {disc}")
print(f"Final Price:  {final_price}")

print("=============================")


