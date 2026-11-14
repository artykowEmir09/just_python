import json
import os
from datetime import datetime

FILE_NAME = "transactions.json"


def load_transactions():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_transactions(transactions):
    with open(FILE_NAME, "w") as file:
        json.dump(transactions, file, indent=4)


def get_next_id(transactions):
    if not transactions:
        return 1

    return max(transaction["id"] for transaction in transactions) + 1


def get_amount():
    while True:
        try:
            amount = float(input("Amount: RM "))

            if amount <= 0:
                print("Amount must be greater than 0.")
                continue

            return amount

        except ValueError:
            print("Please enter a valid number.")


def add_transaction(transactions, transaction_type):

    print("\n==============================")
    print(f"       ADD {transaction_type.upper()}")
    print("==============================")

    amount = get_amount()

    category = input("Category: ").strip()

    description = input("Description: ").strip()

    transaction = {
        "id": get_next_id(transactions),
        "type": transaction_type,
        "amount": amount,
        "category": category,
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    transactions.append(transaction)

    save_transactions(transactions)

    print("\nTransaction added successfully!")


def view_transactions(transactions):

    print("\n==============================")
    print("      ALL TRANSACTIONS")
    print("==============================")

    if not transactions:
        print("No transactions found.")
        return

    for transaction in transactions:

        sign = "+" if transaction["type"] == "income" else "-"

        print(
            f"\nID: {transaction['id']}"
            f"\nType: {transaction['type'].title()}"
            f"\nAmount: {sign}RM{transaction['amount']:.2f}"
            f"\nCategory: {transaction['category']}"
            f"\nDescription: {transaction['description']}"
            f"\nDate: {transaction['date']}"
        )

        print("------------------------------")


def search_transactions(transactions):

    print("\n==============================")
    print("      SEARCH TRANSACTIONS")
    print("==============================")

    if not transactions:
        print("No transactions found.")
        return

    keyword = input("Search category or description: ").lower().strip()

    found = False

    for transaction in transactions:

        if (
            keyword in transaction["category"].lower()
            or keyword in transaction["description"].lower()
        ):

            sign = "+" if transaction["type"] == "income" else "-"

            print(
                f"\nID: {transaction['id']} | "
                f"{transaction['date']} | "
                f"{transaction['category']} | "
                f"{transaction['description']} | "
                f"{sign}RM{transaction['amount']:.2f}"
            )

            found = True

    if not found:
        print("No matching transactions found.")


def monthly_summary(transactions):

    print("\n==============================")
    print("       MONTHLY SUMMARY")
    print("==============================")

    if not transactions:
        print("No transactions found.")
        return

    current_month = datetime.now().strftime("%Y-%m")

    income = 0
    expenses = 0

    for transaction in transactions:

        if transaction["date"].startswith(current_month):

            if transaction["type"] == "income":
                income += transaction["amount"]

            else:
                expenses += transaction["amount"]

    balance = income - expenses

    print(f"\nMonth: {current_month}")
    print(f"Total Income:   RM{income:.2f}")
    print(f"Total Expenses: RM{expenses:.2f}")
    print("------------------------------")
    print(f"Balance:        RM{balance:.2f}")


def category_summary(transactions):

    print("\n==============================")
    print("       CATEGORY SUMMARY")
    print("==============================")

    if not transactions:
        print("No transactions found.")
        return

    categories = {}

    for transaction in transactions:

        if transaction["type"] == "expense":

            category = transaction["category"]
            amount = transaction["amount"]

            if category not in categories:
                categories[category] = 0

            categories[category] += amount

    if not categories:
        print("No expenses found.")
        return

    for category, amount in categories.items():

        print(
            f"{category}: RM{amount:.2f}"
        )


def delete_transaction(transactions):

    print("\n==============================")
    print("      DELETE TRANSACTION")
    print("==============================")

    if not transactions:
        print("No transactions found.")
        return

    try:
        transaction_id = int(input("Enter transaction ID: "))

    except ValueError:
        print("Invalid ID.")
        return

    for transaction in transactions:

        if transaction["id"] == transaction_id:

            print("\nTransaction found:")

            print(
                f"{transaction['category']} - "
                f"RM{transaction['amount']:.2f}"
            )

            confirm = input(
                "Are you sure? (y/n): "
            ).lower()

            if confirm == "y":

                transactions.remove(transaction)

                save_transactions(transactions)

                print("Transaction deleted successfully!")

            else:

                print("Deletion cancelled.")

            return

    print("Transaction not found.")


def statistics(transactions):

    print("\n==============================")
    print("         STATISTICS")
    print("==============================")

    if not transactions:
        print("No transactions found.")
        return

    income_transactions = [
        t for t in transactions
        if t["type"] == "income"
    ]

    expense_transactions = [
        t for t in transactions
        if t["type"] == "expense"
    ]

    total_income = sum(
        t["amount"]
        for t in income_transactions
    )

    total_expenses = sum(
        t["amount"]
        for t in expense_transactions
    )

    balance = total_income - total_expenses

    print(f"\nNumber of transactions: {len(transactions)}")
    print(f"Income transactions:   {len(income_transactions)}")
    print(f"Expense transactions:  {len(expense_transactions)}")

    print(f"\nTotal Income:   RM{total_income:.2f}")
    print(f"Total Expenses: RM{total_expenses:.2f}")
    print(f"Balance:        RM{balance:.2f}")

    if expense_transactions:

        highest_expense = max(
            expense_transactions,
            key=lambda x: x["amount"]
        )

        print(
            f"\nHighest Expense:"
            f"\n{highest_expense['category']} - "
            f"RM{highest_expense['amount']:.2f}"
        )


def main():

    transactions = load_transactions()

    while True:

        print("\n")
        print("================================")
        print("       💰 FINANCE TRACKER")
        print("================================")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Transactions")
        print("4. Search Transactions")
        print("5. Monthly Summary")
        print("6. Category Summary")
        print("7. Statistics")
        print("8. Delete Transaction")
        print("9. Exit")
        print("================================")

        choice = input("Choose an option: ").strip()

        if choice == "1":

            add_transaction(
                transactions,
                "income"
            )

        elif choice == "2":

            add_transaction(
                transactions,
                "expense"
            )

        elif choice == "3":

            view_transactions(
                transactions
            )

        elif choice == "4":

            search_transactions(
                transactions
            )

        elif choice == "5":

            monthly_summary(
                transactions
            )

        elif choice == "6":

            category_summary(
                transactions
            )

        elif choice == "7":

            statistics(
                transactions
            )

        elif choice == "8":

            delete_transaction(
                transactions
            )

        elif choice == "9":

            print("\nThank you for using Finance Tracker!")
            print("Goodbye! 👋")
            break

        else:

            print("\nInvalid option. Please try again.")


if __name__ == "__main__":
    main()