# атрибуты класса и наследование
class Point2D():
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Shape():
    amount: int = 0

    def __init__(self, pos: Point2D):
        self.shape = ''
        self.position = pos
        Shape.amount += 1

    @staticmethod
    def about() -> str:
        return NotImplemented


class Circle(Shape):
    def __init__(self, pos: Point2D, radius: Point2D):
        super().__init__(pos)
        self.shape = 'circle'
        self.radius = radius

    @staticmethod
    def about() -> str:
        return 'This is a Circle and it has no angles.'


class Rectangle(Shape):
    def __init__(self, pos: Point2D, lo_left: Point2D, up_right: Point2D):
        super().__init__(pos)
        self.shape = 'rectangle'
        self.ll = lo_left
        self.ur = up_right

    @staticmethod
    def about() -> str:
        return 'This is a Rectangle and it has four angles.'


shapes = list()
for n in range(10):
    position = Point2D(n * 0.5, n * 1.5)
    shapes.append(Circle(position, n*0.1))

for n in range(5):
    position = Point2D(n * 5, n * 15)
    shapes.append(
        Rectangle(
            position, 
            Point2D(position.x - (n*0.5), position.y - (n*0.5)), 
            Point2D(position.x + (n*0.5), position.y + (n*0.5))
        ))


print(Shape.amount)

print(Circle.about())
print(Rectangle.about())

for shape in shapes:
    print(shape.shape)