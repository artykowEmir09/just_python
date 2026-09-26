try:
    number = int (input("Enter a number: "))
    print(1/number)
except ZeroDivisionError:
    print("Number cannot divide by zero")
except ValueError:
    print("it is not a number")
except Exception:
    print("Enter a number")
    