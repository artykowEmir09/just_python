students = []
while True:
    print("=====STUDENT SYSTEM=====")
    print("1. Add student")
    print("2. Show students")
    print("3. Search students")
    print("4. remove students")
    print("5. Exit")
    print("========================")
    choice = input("Choice: ") 
    
    if choice ==  "1":
        print("======ADD STUDENT======")
        student = input("Enter name of student: ")
        if student in students:
            print("Student already exists!")
        else:
            students.append(student)
            print("Student added successfully")
        print("========================")
    elif choice =="2":
        print("======SHOW STUDENT======")
        print("Students")
        for x in students:
            print(x)
        print("========================")
    elif choice =="3":
        print("======SEARCH STUDENT======")
        name = input ("Enter a name: ")
        if name in students:
            print(name," found")
        else:
            print(name,"Not found")
        print("===========================") 
    elif choice =="4":
        print("======REMOVE STUDENT======")
        delete = input("Enter a name ")
        if delete in students:
            students.remove(delete)
            print("Student successfully removed")
        else:
            print("Student not found!")
        print("========================")
    elif choice =="5":
        print("Have a good day")
        break
    else:
        print("Invalid choice")