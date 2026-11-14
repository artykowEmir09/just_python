import json

FILE_NAME = "employees.json"


class Employee:
    def __init__(self, employee_id, name, department, position, salary):
        self.employee_id = employee_id
        self.name = name
        self.department = department
        self.position = position
        self.salary = salary

    def calculate_salary(self):
        return self.salary

    def to_dict(self):
        return {
            "id": self.employee_id,
            "name": self.name,
            "department": self.department,
            "position": self.position,
            "salary": self.salary,
            "type": "Employee"
        }


class Manager(Employee):
    def __init__(
        self,
        employee_id,
        name,
        department,
        position,
        salary,
        bonus
    ):
        super().__init__(
            employee_id,
            name,
            department,
            position,
            salary
        )

        self.bonus = bonus

    def calculate_salary(self):
        return self.salary + self.bonus

    def to_dict(self):
        data = super().to_dict()

        data["bonus"] = self.bonus
        data["type"] = "Manager"

        return data


class Developer(Employee):
    def __init__(
        self,
        employee_id,
        name,
        department,
        position,
        salary,
        programming_language
    ):
        super().__init__(
            employee_id,
            name,
            department,
            position,
            salary
        )

        self.programming_language = programming_language

    def to_dict(self):
        data = super().to_dict()

        data["programming_language"] = self.programming_language
        data["type"] = "Developer"

        return data


def load_employees():

    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)

        employees = []

        for item in data:

            if item["type"] == "Manager":

                employee = Manager(
                    item["id"],
                    item["name"],
                    item["department"],
                    item["position"],
                    item["salary"],
                    item["bonus"]
                )

            elif item["type"] == "Developer":

                employee = Developer(
                    item["id"],
                    item["name"],
                    item["department"],
                    item["position"],
                    item["salary"],
                    item["programming_language"]
                )

            else:

                employee = Employee(
                    item["id"],
                    item["name"],
                    item["department"],
                    item["position"],
                    item["salary"]
                )

            employees.append(employee)

        return employees

    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_employees(employees):

    data = []

    for employee in employees:
        data.append(employee.to_dict())

    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


def find_employee(employees, employee_id):

    for employee in employees:

        if employee.employee_id == employee_id:
            return employee

    return None


def add_employee(employees):

    print("\n--- ADD EMPLOYEE ---")

    employee_id = input("Employee ID: ")

    if find_employee(employees, employee_id):
        print("Employee ID already exists.")
        return

    name = input("Name: ")
    department = input("Department: ")
    position = input("Position: ")

    while True:

        try:
            salary = float(input("Base Salary (RM): "))

            if salary < 0:
                print("Salary cannot be negative.")
                continue

            break

        except ValueError:
            print("Enter a valid salary.")

    print("\nEmployee Type")
    print("1. Normal Employee")
    print("2. Manager")
    print("3. Developer")

    employee_type = input("Choose type: ")

    if employee_type == "2":

        while True:

            try:
                bonus = float(input("Manager Bonus (RM): "))

                if bonus < 0:
                    print("Bonus cannot be negative.")
                    continue

                break

            except ValueError:
                print("Enter a valid bonus.")

        employee = Manager(
            employee_id,
            name,
            department,
            position,
            salary,
            bonus
        )

    elif employee_type == "3":

        language = input("Programming Language: ")

        employee = Developer(
            employee_id,
            name,
            department,
            position,
            salary,
            language
        )

    else:

        employee = Employee(
            employee_id,
            name,
            department,
            position,
            salary
        )

    employees.append(employee)

    save_employees(employees)

    print("Employee added successfully!")


def view_employees(employees):

    print("\n--- EMPLOYEE LIST ---")

    if not employees:
        print("No employees found.")
        return

    for employee in employees:

        print("\n" + "-" * 40)

        print(f"ID: {employee.employee_id}")
        print(f"Name: {employee.name}")
        print(f"Department: {employee.department}")
        print(f"Position: {employee.position}")
        print(f"Base Salary: RM {employee.salary:.2f}")
        print(
            f"Total Salary: RM "
            f"{employee.calculate_salary():.2f}"
        )

        if isinstance(employee, Manager):
            print(f"Bonus: RM {employee.bonus:.2f}")

        elif isinstance(employee, Developer):
            print(
                f"Programming Language: "
                f"{employee.programming_language}"
            )


def search_employee(employees):

    print("\n--- SEARCH EMPLOYEE ---")

    keyword = input(
        "Enter employee ID or name: "
    ).lower()

    found = False

    for employee in employees:

        if (
            keyword in employee.employee_id.lower()
            or keyword in employee.name.lower()
        ):

            print("\nEmployee found:")

            print(f"ID: {employee.employee_id}")
            print(f"Name: {employee.name}")
            print(f"Department: {employee.department}")
            print(f"Position: {employee.position}")

            found = True

    if not found:
        print("No employee found.")


def update_employee(employees):

    print("\n--- UPDATE EMPLOYEE ---")

    employee_id = input("Employee ID: ")

    employee = find_employee(
        employees,
        employee_id
    )

    if employee is None:
        print("Employee not found.")
        return

    print("\nPress Enter to keep the current value.")

    name = input(f"Name [{employee.name}]: ")
    department = input(
        f"Department [{employee.department}]: "
    )
    position = input(
        f"Position [{employee.position}]: "
    )

    if name:
        employee.name = name

    if department:
        employee.department = department

    if position:
        employee.position = position

    while True:

        salary = input(
            f"Salary [{employee.salary}]: "
        )

        if salary == "":
            break

        try:

            salary = float(salary)

            if salary < 0:
                print("Salary cannot be negative.")
                continue

            employee.salary = salary
            break

        except ValueError:
            print("Enter a valid salary.")

    save_employees(employees)

    print("Employee updated successfully!")


def delete_employee(employees):

    print("\n--- DELETE EMPLOYEE ---")

    employee_id = input("Employee ID: ")

    employee = find_employee(
        employees,
        employee_id
    )

    if employee is None:
        print("Employee not found.")
        return

    print(f"\nEmployee: {employee.name}")

    confirmation = input(
        "Are you sure? (y/n): "
    ).lower()

    if confirmation == "y":

        employees.remove(employee)

        save_employees(employees)

        print("Employee deleted successfully!")

    else:

        print("Operation cancelled.")


def department_search(employees):

    print("\n--- DEPARTMENT SEARCH ---")

    department = input(
        "Enter department: "
    ).lower()

    found = False

    for employee in employees:

        if employee.department.lower() == department:

            print(
                f"{employee.employee_id} | "
                f"{employee.name} | "
                f"{employee.position} | "
                f"RM {employee.calculate_salary():.2f}"
            )

            found = True

    if not found:
        print("No employees found in this department.")


def salary_report(employees):

    print("\n--- SALARY REPORT ---")

    if not employees:
        print("No employees found.")
        return

    total = 0

    for employee in employees:

        salary = employee.calculate_salary()

        total += salary

        print(
            f"{employee.name:<20} "
            f"RM {salary:,.2f}"
        )

    average = total / len(employees)

    print("\n" + "-" * 35)

    print(f"Total Payroll: RM {total:,.2f}")
    print(f"Average Salary: RM {average:,.2f}")


def main():

    employees = load_employees()

    while True:

        print("\n" + "=" * 50)
        print("        EMPLOYEE MANAGEMENT SYSTEM")
        print("=" * 50)

        print("1. Add Employee")
        print("2. View Employees")
        print("3. Search Employee")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Search by Department")
        print("7. Salary Report")
        print("8. Exit")

        print("=" * 50)

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

            department_search(employees)

        elif choice == "7":

            salary_report(employees)

        elif choice == "8":

            print("\nGoodbye! 👋")
            break

        else:

            print("Invalid option.")


if __name__ == "__main__":
    main()