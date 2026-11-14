# 10 exercises

# Don't look for solutions yet. Try them yourself.

# 🟢 Exercise 1 — Personal Information

# Create variables for:

# your name
# your age
# your country
# your university

# Print all four.
name = " Emir"
age = 24
country = "Turkmenistan "
university ="Uniten"
print(f"Name: {name}")
print(f"Age: {age}")
print(f"Country: {country}")
print(f"University: {university}")








# 🟢 Exercise 2 — Favorite Things

# Create variables for:

# favorite_food
# favorite_movie
# favorite_game
# favorite_language

# Print them.

favorite_food = "manty"
favorite_movie = "Creed"
favorite_game ="Assassins creed"
favorite_language = "Turkish"

print(f"Food: {favorite_food}")
print(f"Movie: {favorite_movie}")
print(f"Game: {favorite_game}")
print(f"Language: {favorite_language}")













# 🟢 Exercise 3 — Student Profile

# Create:

# name
# age
# university
# course
# country

# Then print:

# ===== STUDENT PROFILE =====
# Name:
# Age:
# University:
# Course:
# Country:
# ===========================


name = "Emir"
age = 24

university= "UNITEN"

course = "Software engineering"

country = "Turkmenistan"
print("===== STUDENT PROFILE =====")
print (f"Name:       {name}")
print (f"Age:        {age}")
print (f"University: {university}")
print (f"Course:     {course}")
print (f"Country:    {country}")
print("===========================")













# 🟡 Exercise 4 — Update Variables

# Create:

# age = 23

# Then increase the age by 1.

# Expected:

# 24
age = 23 
age +=1
print (age)


# 🟡 Exercise 5 — Rectangle

# Create:

# length = 10
# width = 5

# Calculate and print:

# Area: 50

# Don't hard-code 50.

length = 10
width = 5
area = length * width

print(area)

# 🟡 Exercise 6 — Salary

# Create:

# monthly_salary = 3000

# Calculate:

# yearly salary

# Expected:

# Yearly salary: 36000

monthly_salary = 3000
yearly_salary = monthly_salary* 12
print(yearly_salary)





# 🟠 Exercise 7 — Shopping

# Create variables for:

# laptop_price
# phone_price
# headphones_price

# Calculate the total price.

# Output:

# Total: ...

laptop_price = 1250
phone_price = 700
headphones_price = 250
total = laptop_price + phone_price + headphones_price

print(f"Total: {total}")



# 🟠 Exercise 8 — Student Average

# Create three variables:

# math = 85
# programming = 92
# english = 78

# Calculate the average.

# Expected concept:

# Average: 85.0

math = 85
programming = 92
english = 78
average = (math + programming + english)/3
print(F"Average: {average   }")




# 🔴 Exercise 9 — Real-world profile

# Create a small developer profile using variables:

# name
# age
# country
# university
# course
# programming_language
# years_learning
# github_username

# Print it in a professional format.

name = "king"
age = 30
country = "Germany"
university = "Offenburg"
course = "computer science"
programming_language = "python"
years_learning = 1
github_username  = "Username"

print (f"Name: {name}")
print (f"Age: {age}")
print (f"Country: {country}")
print (f"University: {university}")
print (f"Course: {course}")
print (f"Programming language: {programming_language}")
print (f"Years learning: {years_learning}")
print (f"Github username: {github_username}")







# 🔥 Exercise 10 — Challenge

# Create variables for:

# product_name
# price
# quantity

# Calculate:

# total_price

# Then create another variable:

# discount

# For example:

# discount = 0.10

# Calculate the final price after the 10% discount.

# Your program should produce something like:

# ========== RECEIPT ==========
# Product: Laptop
# Price: 3000
# Quantity: 2
# Subtotal: 6000
# Discount: 600
# Final Price: 5400
# ==============================



product_name = "Laptop"
price = 3000
quantity = 2
subTotal = quantity * price
Discount = subTotal * 0.1
Final_Price = subTotal - Discount

print("========== RECEIPT ==========")
print(f"Product:     {product_name}")
print(f"Price:       {price}")
print(f"Quantity:    {quantity}")
print(f"Subtotal:    {subTotal}")
print(f"Discount:    {Discount}")
print(f"Final Price: {Final_Price}")
print("==============================")

