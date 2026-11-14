import json
import csv

employee = [["Name","Age","Job"],
            ["Merdan", 23,"student"],
            ["Meret", 27 , "Dali"],
            ["Merjen", 25,"Accounter"]]
file_path = r"C:\Users\USER\OneDrive\Desktop\output.csv"
try:
    with open(file_path, "w") as file:
        writer = csv.writer(file)
        for row in employee:
            writer.writerow(row)
        print(f"csv file '{file_path}' was created")
except FileExistsError:
    print("That file has already exists")