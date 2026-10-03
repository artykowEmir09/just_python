#python reading files

file_path ="C:/Users/USER/OneDrive/Desktop/def show_balance(balance).txt"
try:
    with  open (file_path, "r") as file:
        content =  file.read()
        print(content)
except FileNotFoundError:
    print("That file not found")
except PermissionError:
    print("You dont have permission to read that file")