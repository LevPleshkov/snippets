# для создания иерархии классов плоаских геометрических фигур
# с базовым абстрактным классом, воспользуемся модулем, позволяющим
# воплощать абстрактные методы с помощью декоратора `abstractmethod`.
# ABC - Abstract Base Class.
from abc import ABC, abstractmethod


# вспомогательный класс для репрезентации двумерной точки
class Point2D:
    # этот метод - инициализатор, который вызывается при создании
    # экземпляра класса.
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


# абстрактный класс наследуется от ABC и нужен для того, чтобы 
# задать общий интерфейс, необходимый всем наследующим его классам.
class Shape(ABC):

    # атрибут класса, который будет одинаковым для всех экземпляров.
    # с помощью аннотации типов, разработчик может указать свои
    # ОЖИДАНИЯ насчет того, какого типа должны быть переменная.
    # аннотация не гарантирует строгого соблюдения типов.  
    amount: int = 0

    # именно наличие абстрактных методов запрещает интерпретатору 
    # создавать экземпляры абстрактного класса. первый аргумент
    # метода всегда будет являться ссылккой на экземпляр класса.
    @abstractmethod
    def __init__(self, shape, pos: Point2D):
        # эти атрибуты будут уникальными для каждого экземпляра
        # класса, так как добавляются к экземпляру при его создании.
        self.shape = shape  # str
        self.position = pos  # Point2D
        # а к атрибуту класса стоит обращаться по имени класса.
        Shape.amount += 1

    # так же как и атрибут, метод тоже может быть методом класса.
    # метод становится методом класса с помощью декоратора 
    # `staticmethod`.  аннотировать тип можно и для значения,
    # возвращающего функцию.
    @staticmethod
    @abstractmethod  # последний (внутренний) в списке декораторов
    def __str__() -> str:
        return NotImplemented


# конкретному классу, наследуемому от абстрактного, необходимо
# переопределить все абстрактные методы базового класса. 
class Circle(Shape):
    def __init__(self, pos: Point2D, radius: Point2D):
        # вызываем инициализатор базового класса, с помощью встроенной
        # функции `super()`, позволяющей получить доступ к методам 
        # базового класса.
        super().__init__('circle', pos)
        # это свойство будет только у экземпляров `Circle`.
        self.radius = radius

    @staticmethod
    def __str__() -> str:
        return f'Circle has no angles. x: {position.x}, y: {position.y}.'

    def __gt__(self, other):
        return self.radius > other.radius


# еще конкретный класс, унаследованный от `Shape`.
class Rectangle(Shape):
    def __init__(self, pos: Point2D, lo_left: Point2D, up_right: Point2D):
        super().__init__('rectangle', pos)
        self.lower_left = lo_left
        self.upper_right = up_right

    @staticmethod
    def __str__() -> str:
        return f'Rectangle has four angles. x: {position.x}, y: {position.y}.'


# создадим список разных фигур - из 3 кругов и
#  3 прямоугольников.
shapes = list()

for n in range(1, 4):
    # для создания экземпляра класса, нужно обратиться 
    # к объекту класса как к функции с аргументами, перечисленными
    # в инициализаторе `__init__()`.  
    position = Point2D(n*0.5, n*1.5)
    shapes.append(Circle(position, n*0.1))

for n in range(1, 4):
    position = Point2D(-n*0.5, -n*1.5)
    shapes.append(
        Rectangle(
            position, 
            Point2D(position.x - (n*0.5), position.y - (n*0.5)), 
            Point2D(position.x + (n*0.5), position.y + (n*0.5))
        ))


# статическое свойство теперь имеет значение 6
print(f'total shapes: {Shape.amount}')

# приведет к ошибке, потому что Shape - абстрактный класс
shape = Shape('shape', Point2D(0, 0))


# общий интерфейс базового абстрактного класса `Shape` позволяет
# обращаться к атрибутам сущностей конкретных классов однаково. 
for shape in shapes:
    print(shape)
