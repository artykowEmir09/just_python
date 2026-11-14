class Car ():
    def __init__(self, model,year,color):
        self.model = model
        self.year = year
        self.color = color
    def drive(self):
        print(f"you drive the{self.color} {self.model}")
         
