class Shape:
    def __init__(self, color,is_filled):
        self.color = color
        self.is_filled  = is_filled
class Circle (Shape):
    def __init__(self, color, is_filled, radius):
        super().__init__(color, is_filled)
        self.radius = radius
class Square(Shape):
    def __init__(self, color, is_filled,width):
        super().__init__(color, is_filled)
        self.width = width
class Triangle (Shape):
    def __init__(self, color, is_filled ,width , height):
        super().__init__(color, is_filled)
        self.height = height
        self.width = width
circle = Circle(color="Black", is_filled=True, radius=10)
print(circle.color ,circle.is_filled , circle.radius)
