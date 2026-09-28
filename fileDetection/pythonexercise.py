import json
employee = {
"name": "Emir",
"age": 24,
"job": "Software engineer"
}
file_path = r"C:\Users\USER\OneDrive\Desktop\output.json"
try:
    with open(file_path, "w") as file:
        json.dump(employee,file, indent = 4)
        print(f"Json file '{file_path}' was created")
except FileExistsError:
    print("That file has already exists"