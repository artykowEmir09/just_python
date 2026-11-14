class Student :

    count = 0
    total_gpa = 0

    def __init__(self, name , gpa):
        self.name = name
        self.gpa = gpa
        Student.count += 1
        Student.total_gpa += gpa

        #instance method
    def get_info(self):
        return f"{self.name} {self.gpa}"
    @classmethod
    def get_count(cls):
        return f"Total # of students {cls.count}" 
    @classmethod
    def get_avarage_gpa(cls):
        if cls.count == 0:
            return 0 
        else:
            return f"Average GPA: {cls.total_gpa / cls.count:.2f}"


student1 = Student("Mike", 3.4)   
student2 = Student("Muhammetali", 4.0)   
student3 = Student("Jorge", 3.2) 

print(Student.get_count())
print(Student.get_avarage_gpa())