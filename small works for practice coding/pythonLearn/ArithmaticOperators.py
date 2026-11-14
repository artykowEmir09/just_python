# Arithmetic & Math
# Exercise 1 — Movie Tickets 🟢
# Ask the user for:
# ticket price
# number of tickets
# Calculate the total cost.
# Example:
# Ticket price: 12.50
# Number of tickets: 3
# Total: 37.5
"""
ticket_price = float(input("Enter ticket prices: "))
quantity = int(input("How many tickets do you want: "))
total = ticket_price * quantity
print(f"Ticket price: {ticket_price}")
print(f"Quantity: {quantity}")
print(f"Total: {total}")
"""
# Exercise 2 — Trip Distance 🟢
# Ask for:
# distance traveled in km
# fuel used in liters
# Calculate:
# km per liter = distance / fuel
# Example:
# Distance: 450
# Fuel: 30
# Fuel efficiency: 15.0 km/L
"""
distance = float(input("Distance Traveled:  "))
fuel = float (input("How many liter did it take?  "))
km_per_liter = distance / fuel
print (f"Fuel efficeincy: {km_per_liter} km/L")
"""




# Exercise 3 — Salary Calculator 🟡
# Ask for:
# monthly salary
# monthly bonus
# Calculate:
# yearly salary without bonus
# yearly bonus
# total yearly income
# Example:
# Monthly salary: 3000
# Monthly bonus: 500
# Yearly salary: 36000
# Yearly bonus: 6000
# Total yearly income: 42000
"""
monthly_salary = int(input("Enter your monthly salary: "))
monthly_bonus = int(input("Enter your monthly bonus: "))
yearly_salary = monthly_salary * 12
yearly_bonus = monthly_bonus * 12
total_income = yearly_bonus + yearly_salary
print(f"Monthly salary:      {monthly_salary}")
print(f"Monthly bonus:       {monthly_bonus}")
print(f"Yearly salary:       {yearly_salary}")
print(f"Yearly bonus:        {yearly_bonus}")
print(f"Total yearly income: {total_income}")
"""

# Exercise 4 — Temperature Conversion 🟡
# Ask the user for a temperature in Celsius.
# Convert it to Fahrenheit using:
# F = (C × 9/5) + 32
# Example:
# Celsius: 25
# Fahrenheit: 77.0
"""
celsius = float(input ("Enter temperature in  celsius: "))
fahrenheit = (celsius * 9/5) + 32
print(f"Celsius: {celsius}")
print(f"Fahrenheit: {fahrenheit}")
"""
# Exercise 5 — Shopping Discount 🟡
# Ask for:
# product price
# quantity
# discount percentage
# Calculate:
# subtotal
# discount amount
# final price
# Twist: The user enters the discount as a normal percentage.
# Example:
# Price: 80
# Quantity: 3
# Discount: 15
# Subtotal: 240
# Discount amount: 36
# Final price: 204

# Think carefully about converting 15 into 0.15.

# Exercise 6 — BMI Calculator 🟠
# Ask the user for:
# weight in kg
# height in meters
# Calculate:
# BMI = weight / (height × height)
# Example:
# Weight: 70
# Height: 1.75
# BMI: 22.857...
# You don't need to round it yet.

 
# Exercise 7 — Restaurant Bill 🟠
# A restaurant customer enters:

# food cost
# number of people
# tax percentage
# tip percentage

# Calculate:

# Tax amount
# Tip amount
# Final bill
# Amount each person pays

# Example:

# Food cost: 100
# People: 4
# Tax: 6
# Tip: 10

# Your program should calculate everything.

# Exercise 8 — Currency Breakdown 🔴

# Ask the user for an amount of money.

# For example:

# Amount: 187

# Calculate how many:

# 100 bills
# 50 bills
# 20 bills
# 10 bills
# 5 bills
# 1 bills

# are needed.

# For 187, the result should be:

# 100: 1
# 50: 1
# 20: 1
# 10: 1
# 5: 1
# 1: 2

# 💡 You'll need an arithmetic operator you haven't specifically practiced much yet.

# Exercise 9 — Employee Paycheck 🔴

# Ask for:

# employee name
# hourly wage
# hours worked
# tax percentage

# Calculate:

# gross pay = wage × hours
# tax amount = gross pay × tax percentage
# net pay = gross pay - tax amount

# Then print a professional-looking paycheck.

# Example:

# ========== PAYCHECK ==========

# Employee: Alex
# Hourly Wage: 25
# Hours Worked: 40
# Gross Pay: 1000
# Tax: 100
# Net Pay: 900

# ==============================

# The user should enter the tax as a percentage, e.g. 10, not 0.10.

# 🔥 Exercise 10 — Challenge

# Build a Travel Cost Calculator.

# Ask the user for:

# traveler name
# destination
# number of days
# hotel cost per night
# food cost per day
# transportation cost
# activity cost
# discount percentage

# Calculate:

# hotel total
# food total
# subtotal
# discount
# final trip cost
# cost per day

# Then produce a clean report.

# Example structure:

# ========== TRIP COST ==========

# Traveler: John
# Destination: Tokyo
# Days: 5

# Hotel: ...
# Food: ...
# Transportation: ...
# Activities: ...

# Subtotal: ...
# Discount: ...
# Final Cost: ...
# Cost Per Day: ...

# ===============================