import json
import os

FILE_NAME = "employees.json"


def load_employees():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []


def save_employees(employees):
    with open(FILE_NAME, "w") as file:
        json.dump(employees, file, indent=4)


def generate_id(employees):
    if not employees:
        return 1

    return max(employee["id"] for employee in employees) + 1


def add_employee(employees):
    print("\n--- Add Employee ---")

    name = input("Name: ")
    age = int(input("Age: "))
    position = input("Position: ")
    salary = float(input("Salary: "))

    employee = {
        "id": generate_id(employees),
        "name": name,
        "age": age,
        "position": position,
        "salary": salary
    }

    employees.append(employee)
    save_employees(employees)

    print("Employee added successfully!")


def view_employees(employees):
    print("\n--- Employees ---")

    if not employees:
        print("No employees found.")
        return

    for employee in employees:
        print(
            f"ID: {employee['id']} | "
            f"Name: {employee['name']} | "
            f"Age: {employee['age']} | "
            f"Position: {employee['position']} | "
            f"Salary: RM{employee['salary']:.2f}"
        )


def search_employee(employees):
    print("\n--- Search Employee ---")

    keyword = input("Enter name or position: ").lower()

    found = False

    for employee in employees:
        if (
            keyword in employee["name"].lower()
            or keyword in employee["position"].lower()
        ):
            print(
                f"ID: {employee['id']} | "
                f"Name: {employee['name']} | "
                f"Age: {employee['age']} | "
                f"Position: {employee['position']} | "
                f"Salary: RM{employee['salary']:.2f}"
            )
            found = True

    if not found:
        print("No matching employee found.")


def update_employee(employees):
    print("\n--- Update Employee ---")

    try:
        employee_id = int(input("Enter employee ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    for employee in employees:
        if employee["id"] == employee_id:

            print("Leave input empty to keep the current value.")

            name = input(f"Name [{employee['name']}]: ")
            age = input(f"Age [{employee['age']}]: ")
            position = input(f"Position [{employee['position']}]: ")
            salary = input(f"Salary [{employee['salary']}]: ")

            if name:
                employee["name"] = name

            if age:
                employee["age"] = int(age)

            if position:
                employee["position"] = position

            if salary:
                employee["salary"] = float(salary)

            save_employees(employees)

            print("Employee updated successfully!")
            return

    print("Employee not found.")


def delete_employee(employees):
    print("\n--- Delete Employee ---")

    try:
        employee_id = int(input("Enter employee ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    for employee in employees:
        if employee["id"] == employee_id:

            confirm = input(
                f"Delete {employee['name']}? (y/n): "
            ).lower()

            if confirm == "y":
                employees.remove(employee)
                save_employees(employees)
                print("Employee deleted successfully!")
            else:
                print("Deletion cancelled.")

            return

    print("Employee not found.")


def salary_statistics(employees):
    print("\n--- Salary Statistics ---")

    if not employees:
        print("No employees available.")
        return

    total = sum(employee["salary"] for employee in employees)
    average = total / len(employees)

    highest = max(employees, key=lambda employee: employee["salary"])
    lowest = min(employees, key=lambda employee: employee["salary"])

    print(f"Total employees: {len(employees)}")
    print(f"Total salary: RM{total:.2f}")
    print(f"Average salary: RM{average:.2f}")

    print(
        f"Highest salary: {highest['name']} "
        f"- RM{highest['salary']:.2f}"
    )

    print(
        f"Lowest salary: {lowest['name']} "
        f"- RM{lowest['salary']:.2f}"
    )


def main():
    employees = load_employees()

    while True:

        print("\n==============================")
        print("   EMPLOYEE MANAGEMENT SYSTEM")
        print("==============================")
        print("1. Add Employee")
        print("2. View Employees")
        print("3. Search Employee")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Salary Statistics")
        print("7. Exit")
        print("==============================")

        choice = input("Choose an option: ")

        if choice == "1":
            add_employee(employees)

        elif choice == "2":
            view_employees(employees)

        elif choice == "3":
            search_employee(employees)

        elif choice == "4":
            update_employee(employees)

        elif choice == "5":
            delete_employee(employees)

        elif choice == "6":
            salary_statistics(employees)

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


main()