import json

FILE_NAME = "inventory.json"


class Product:
    def __init__(self, product_id, name, price, quantity, category):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category

    def to_dict(self):
        return {
            "id": self.product_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "category": self.category
        }


def load_inventory():
    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)

        products = []

        for item in data:
            product = Product(
                item["id"],
                item["name"],
                item["price"],
                item["quantity"],
                item["category"]
            )

            products.append(product)

        return products

    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_inventory(products):
    data = []

    for product in products:
        data.append(product.to_dict())

    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


def product_exists(products, product_id):
    for product in products:
        if product.product_id == product_id:
            return product

    return None


def add_product(products):
    print("\n--- ADD PRODUCT ---")

    product_id = input("Product ID: ")

    if product_exists(products, product_id):
        print("Product ID already exists.")
        return

    name = input("Product name: ")
    category = input("Category: ")

    while True:
        try:
            price = float(input("Price (RM): "))

            if price < 0:
                print("Price cannot be negative.")
                continue

            break

        except ValueError:
            print("Enter a valid price.")


    while True:
        try:
            quantity = int(input("Quantity: "))

            if quantity < 0:
                print("Quantity cannot be negative.")
                continue

            break

        except ValueError:
            print("Enter a valid quantity.")

    product = Product(
        product_id,
        name,
        price,
        quantity,
        category
    )

    products.append(product)

    save_inventory(products)

    print("Product added successfully!")


def view_inventory(products):
    print("\n--- INVENTORY ---")

    if not products:
        print("Inventory is empty.")
        return

    print(
        f"{'ID':<10}"
        f"{'Name':<20}"
        f"{'Category':<15}"
        f"{'Price':<12}"
        f"{'Stock':<10}"
    )

    print("-" * 67)

    for product in products:
        print(
            f"{product.product_id:<10}"
            f"{product.name:<20}"
            f"{product.category:<15}"
            f"RM {product.price:<9.2f}"
            f"{product.quantity:<10}"
        )


def search_product(products):
    print("\n--- SEARCH PRODUCT ---")

    keyword = input("Enter product name or ID: ").lower()

    found = False

    for product in products:
        if (
            keyword in product.name.lower()
            or keyword in product.product_id.lower()
        ):
            print("\nProduct found:")
            print(f"ID: {product.product_id}")
            print(f"Name: {product.name}")
            print(f"Category: {product.category}")
            print(f"Price: RM {product.price:.2f}")
            print(f"Quantity: {product.quantity}")

            found = True

    if not found:
        print("No product found.")


def update_stock(products):
    print("\n--- UPDATE STOCK ---")

    product_id = input("Enter product ID: ")

    product = product_exists(products, product_id)

    if product is None:
        print("Product not found.")
        return

    print(f"Current stock: {product.quantity}")

    print("\n1. Add Stock")
    print("2. Remove Stock")

    choice = input("Choose option: ")

    try:
        amount = int(input("Enter quantity: "))

        if amount <= 0:
            print("Quantity must be greater than 0.")
            return

        if choice == "1":
            product.quantity += amount

        elif choice == "2":

            if amount > product.quantity:
                print("Not enough stock.")
                return

            product.quantity -= amount

        else:
            print("Invalid option.")
            return

        save_inventory(products)

        print(f"Stock updated. New quantity: {product.quantity}")

    except ValueError:
        print("Enter a valid quantity.")


def remove_product(products):
    print("\n--- REMOVE PRODUCT ---")

    product_id = input("Enter product ID: ")

    product = product_exists(products, product_id)

    if product is None:
        print("Product not found.")
        return

    print(f"\nProduct: {product.name}")
    print(f"Stock: {product.quantity}")

    confirm = input("Are you sure? (y/n): ").lower()

    if confirm == "y":
        products.remove(product)

        save_inventory(products)

        print("Product removed successfully!")

    else:
        print("Operation cancelled.")


def low_stock(products):
    print("\n--- LOW STOCK PRODUCTS ---")

    try:
        limit = int(input("Show products with stock below: "))

        found = False

        for product in products:

            if product.quantity <= limit:
                print(
                    f"{product.product_id} | "
                    f"{product.name} | "
                    f"Stock: {product.quantity}"
                )

                found = True

        if not found:
            print("No low-stock products.")

    except ValueError:
        print("Enter a valid number.")


def inventory_value(products):
    print("\n--- INVENTORY VALUE ---")

    total = 0

    for product in products:
        total += product.price * product.quantity

    print(f"Total inventory value: RM {total:.2f}")


def category_summary(products):
    print("\n--- CATEGORY SUMMARY ---")

    categories = {}

    for product in products:

        if product.category not in categories:
            categories[product.category] = 0

        categories[product.category] += product.quantity

    if not categories:
        print("No products available.")
        return

    for category, quantity in categories.items():
        print(f"{category}: {quantity} units")


def main():

    products = load_inventory()

    while True:

        print("\n" + "=" * 45)
        print("       INVENTORY MANAGEMENT SYSTEM")
        print("=" * 45)

        print("1. Add Product")
        print("2. View Inventory")
        print("3. Search Product")
        print("4. Update Stock")
        print("5. Remove Product")
        print("6. Low Stock Products")
        print("7. Inventory Value")
        print("8. Category Summary")
        print("9. Exit")

        print("=" * 45)

        choice = input("Choose an option: ")

        if choice == "1":
            add_product(products)

        elif choice == "2":
            view_inventory(products)

        elif choice == "3":
            search_product(products)

        elif choice == "4":
            update_stock(products)

        elif choice == "5":
            remove_product(products)

        elif choice == "6":
            low_stock(products)

        elif choice == "7":
            inventory_value(products)

        elif choice == "8":
            category_summary(products)

        elif choice == "9":
            print("\nThank you for using the system! 👋")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()