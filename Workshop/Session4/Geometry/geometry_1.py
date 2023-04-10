from abc import ABC, abstractmethod
from math import tan
from tabulate import tabulate
from unittest import TestCase
from random import randint

pi = 3.14


class Shape(ABC):
    __name__: str = "Shape"
    _area_formula: str = ""
    _perimeter_formula: str = ""

    @abstractmethod
    def get_area(self) -> float:
        ...

    @abstractmethod
    def get_perimeter(self) -> float:
        ...

    @abstractmethod
    def __str__(self) -> str:
        ...

    @classmethod
    def check_if_args_not_below_zero(cls, *args) -> bool:
        for i in args:
            if i < 0:
                return False
        return True

    @classmethod
    def get_area_formula(cls) -> str:
        return cls._area_formula.replace("{", "").replace("}", "")

    @classmethod
    def get_perimeter_formula(cls) -> str:
        return cls._perimeter_formula.replace("{", "").replace("}", "")


class Circle(Shape):
    __name__ = "Circle"
    _area_formula = "{pi}*({r}**2)"
    _perimeter_formula = "2*{pi}*{r}"

    def __init__(self, r: float):
        self.r = r

    def get_area(self) -> float:
        return eval(self._area_formula.format(pi=pi, r=self.r))

    def get_perimeter(self) -> float:
        return eval(self._perimeter_formula.format(pi=pi, r=self.r))

    def __str__(self) -> str:
        return f"circle, r={self.r}"


class Triangle(Shape):
    __name__ = "Triangle"
    _area_formula = "(((({a}**2) - (({c}/2) ** 2)) ** (1/2))*{c}) / 2"
    _perimeter_formula = "{a}+{b}+{c}"

    def __init__(self, a: float, b: float, c: float):
        self.a = a
        self.b = b
        self.c = c

    def get_area(self) -> float:
        return eval(self._area_formula.format(a=self.a, b=self.b, c=self.c))

    def get_perimeter(self) -> float:
        return eval(self._perimeter_formula.format(a=self.a, b=self.b, c=self.c))

    def __str__(self) -> str:
        return f"Triangle, a={self.a}, b={self.b}, c={self.c}"


class EquilateralTriangle(Triangle):
    __name__ = "EquilateralTriangle"
    _area_formula = "((3 ** (1/2)) / 4 )*({a} ** 2)"
    _perimeter_formula = "3*{a}"

    def __init__(self, a: float):
        super().__init__(a, b=0, c=0)

    def __str__(self) -> str:
        return f"EquilateralTriangle, a={self.a}"


class Rectangle(Shape):
    __name__ = "Rectangle"
    _area_formula = "{a}*{b}"
    _perimeter_formula = "2*({a}*{b})"

    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b

    def get_area(self) -> float:
        return eval(self._area_formula.format(a=self.a, b=self.b))

    def get_perimeter(self) -> float:
        return eval(self._perimeter_formula.format(a=self.a, b=self.b))

    def __str__(self) -> str:
        return f"Rectangle, a={self.a}, b={self.b}"


class Square(Rectangle):
    __name__ = "Square"
    _area_formula = "{a}**2"
    _perimeter_formula = "4*{a}"

    def __init__(self, a: float):
        super().__init__(a, b=0)

    def __str__(self) -> str:
        return f"Square, a={self.a}"


class ReqularPantagon(Shape):
    __name__ = "ReqularPantagon"
    _area_formula = "(P*h)/2"
    _perimeter_formula = "5*{a}"

    def __init__(self, a: float):
        self.a = a

    def get_area(self) -> float:
        h = self.a / 2 * (tan(180 / 5))
        return (self.get_perimeter() * h) / 2

    def get_perimeter(self) -> float:
        return eval(self._perimeter_formula.format(a=self.a))

    def __str__(self) -> str:
        return f"RequlatPantagon, a={self.a}"


class ShapeList:
    def __init__(self, shapes=None):
        self.shapes: list = shapes if shapes else []

    def add_shape(self, shape):
        if not isinstance(shape, Shape):
            raise TypeError()
        self.shapes.append(shape)

    def get_shapes_table(self) -> str:
        head = ["idx", "Class", "__str__",
                "Perimeter", "Formula", "Area", "Formula"]
        row = []
        for index, shape in enumerate(self.shapes):
            row.append([index, shape.__name__, str(shape), shape.get_perimeter(), shape.get_perimeter_formula(),
                        shape.get_area(), shape.get_area_formula()])
        return tabulate(row, headers=head, tablefmt="grid")

    def get_largest_shape_by_perimeter(self) -> Shape:
        obj = self.shapes[0]
        for i in range(1, len(self.shapes)):
            if obj.get_perimeter() < self.shapes[i].get_perimeter():
                obj = self.shapes[i]
        return obj

    def get_largest_shape_by_area(self) -> Shape:
        obj = self.shapes[0]
        for i in range(1, len(self.shapes)):
            if obj.get_area() < self.shapes[i].get_area():
                obj = self.shapes[i]
        return obj


class TestABC(ABC):
    @abstractmethod
    def setUp(self): ...

    def test_get_area(self):
        self.assertEqual(self.obj.get_area(), self.area)
        self.assertNotEqual(self.obj.get_area(), randint(-100, 10))

    def test_get_perimeter(self):
        self.assertEqual(self.obj.get_perimeter(), self.perimeter)
        self.assertNotEqual(self.obj.get_perimeter(), randint(-100, 10))

    def test_formula_area(self):
        self.assertEqual(self.obj.get_area_formula(), self.area_formula)

    def test_formula_perimeter(self):
        self.assertEqual(self.obj.get_perimeter_formula(),
                         self.perimeter_formula)


class TestCircle(TestCase, TestABC):
    def setUp(self):
        self.obj = Circle(10)

        self.area = pi * (10 ** 2)
        self.area_formula = "pi*(r**2)"

        self.perimeter = pi * 2 * 10
        self.perimeter_formula = "2*pi*r"


class TestRectangle(TestCase, TestABC):
    def setUp(self) -> None:
        self.obj = Rectangle(5, 10)

        self.area = 5 * 10
        self.area_formula = "a*b"

        self.perimeter = 2 * 5 * 10
        self.perimeter_formula = "2*(a*b)"


class TestSquare(TestCase, TestABC):
    def setUp(self) -> None:
        self.obj = Square(4)

        self.area = 4 ** 2
        self.area_formula = "a**2"

        self.perimeter = 4 * 4
        self.perimeter_formula = "4*a"


class TestTriangle(TestCase, TestABC):
    def setUp(self) -> None:
        self.obj = Triangle(2, 3, 4)

        self.area = ((((2 ** 2) - ((4 / 2) ** 2)) ** (1 / 2)) * 4) / 2
        self.area_formula = "((((a**2) - ((c/2) ** 2)) ** (1/2))*c) / 2"

        self.perimeter = 2 + 3 + 4
        self.perimeter_formula = "a+b+c"


class TestEquilateralTriangle(TestCase, TestABC):
    def setUp(self) -> None:
        self.obj = EquilateralTriangle(10)

        self.area = ((3 ** (1 / 2)) / 4) * (10 ** 2)
        self.area_formula = "((3 ** (1/2)) / 4 )*(a ** 2)"

        self.perimeter = 3 * 10
        self.perimeter_formula = "3*a"


class TestReqularPantagon(TestCase, TestABC):
    def setUp(self) -> None:
        self.obj = ReqularPantagon(20)

        self.perimeter = 5 * 20
        self.perimeter_formula = "5*a"

        self.area = (self.perimeter * (20 / 2 * (tan(180 / 5)))) / 2
        self.area_formula = "(P*h)/2"


class TestShapeList(TestCase):
    def setUp(self) -> None:
        self.shape_list = ShapeList()

    def test_add_shape(self):
        c = Circle(10)
        self.shape_list.add_shape(c)

        self.assertIn(c, self.shape_list.shapes)

        r = Rectangle(10, 20)
        self.shape_list.add_shape(r)

        self.assertIn(r, self.shape_list.shapes)

        self.assertEqual(self.shape_list.shapes, [c, r])

    def test_shapes_table(self):
        head = ["idx", "Class", "__str__",
                "Perimeter", "Formula", "Area", "Formula"]
        shapes = [Circle(10), Square(20), EquilateralTriangle(10)]
        row = []
        for index, shape in enumerate(shapes):
            row.append([index, shape.__name__, str(shape), shape.get_perimeter(), shape.get_perimeter_formula(),
                        shape.get_area(), shape.get_area_formula()])
            self.shape_list.add_shape(shape)

        table = tabulate(row, headers=head, tablefmt="grid")

        self.assertEqual(self.shape_list.get_shapes_table(), table)

    def test_get_largest_shape_by_perimeter(self):
        shapes = [Circle(10), Square(20), EquilateralTriangle(10)]
        max_ = 0
        obj = None

        for shape in shapes:
            if max_ < shape.get_perimeter():
                max_ = shape.get_perimeter()
                obj = shape
            self.shape_list.add_shape(shape)

        self.assertEqual(self.shape_list.get_largest_shape_by_perimeter(), obj)

    def test_get_largest_shape_by_area(self):
        shapes = [Circle(10), Square(20), EquilateralTriangle(10)]
        max_ = 0
        obj = None

        for shape in shapes:
            if max_ < shape.get_area():
                max_ = shape.get_area()
                obj = shape
            self.shape_list.add_shape(shape)

        self.assertEqual(self.shape_list.get_largest_shape_by_area(), obj)
