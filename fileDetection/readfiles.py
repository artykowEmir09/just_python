#python reading files

file_path ="C:/Users/USER/OneDrive/Desktop/def show_balance(balance).txt"

with  open (file_path, "r") as file:
    content =  file.read()
    print(content)