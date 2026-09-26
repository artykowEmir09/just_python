text_data = "I love Besiktas "
file_path = "output.txt"

with open(file_path , "w") as file:
    file.write(text_data)
    print(f"txt file '{file_path}'was created")