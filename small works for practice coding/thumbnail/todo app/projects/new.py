expenses = []


def add_expense():
    name = input("Enter expense name: ")
    amount = float(input("Enter amount: "))

    expenses.append({
        "name": name,
        "amount": amount
    })

    print("Expense added successfully!")


def show_expenses():
    if not expenses:
        print("No expenses yet.")
        return

    print("\n===== Expenses =====")

    total = 0

    for expense in expenses:
        print(f"{expense['name']}: RM{expense['amount']:.2f}")
        total += expense["amount"]

    print("--------------------")
    print(f"Total: RM{total:.2f}")


while True:
    print("\n===== Expense Tracker =====")
    print("1. Add expense")
    print("2. Show expenses")
    print("3. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        add_expense()

    elif choice == "2":
        show_expenses()

    elif choice == "3":
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")