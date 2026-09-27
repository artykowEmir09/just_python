from datetime import datetime


balance = 1000.00
transactions = []


def show_balance():
    print(f"\nCurrent balance: ${balance:.2f}")


def deposit():
    global balance

    try:
        amount = float(input("Enter deposit amount: $"))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        balance += amount

        transactions.append({
            "type": "Deposit",
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        print(f"${amount:.2f} deposited successfully.")

    except ValueError:
        print("Please enter a valid number.")


def withdraw():
    global balance

    try:
        amount = float(input("Enter withdrawal amount: $"))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        if amount > balance:
            print("Insufficient funds.")
            return

        balance -= amount

        transactions.append({
            "type": "Withdrawal",
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        print(f"${amount:.2f} withdrawn successfully.")

    except ValueError:
        print("Please enter a valid number.")


def show_transactions():

    if not transactions:
        print("\nNo transactions yet.")
        return

    print("\n========== TRANSACTION HISTORY ==========")

    for transaction in transactions:

        print(
            f"{transaction['date']} | "
            f"{transaction['type']} | "
            f"${transaction['amount']:.2f}"
        )


def main():

    while True:

        print("\n========== BANKING SYSTEM ==========")
        print("1. Show Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transaction History")
        print("5. Exit")
        print("====================================")

        choice = input("Choose an option: ")

        if choice == "1":
            show_balance()

        elif choice == "2":
            deposit()

        elif choice == "3":
            withdraw()

        elif choice == "4":
            show_transactions()

        elif choice == "5":
            print("Thank you for using our banking system.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()