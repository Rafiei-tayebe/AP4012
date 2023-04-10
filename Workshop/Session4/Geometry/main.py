from geometry import ShapeList, Circle, Rectangle, Square, Triangle, EquilateralTriangle, ReqularPantagon


def menu():
    choose = input(f'''Learn Geometry
What do you want to do?
    (1) Add new shape
    (2) Show all shapes
    (3) Show shape with the largest perimeter
    (4) Show shape with the largest area
    (5) Show formulas 
    (0) Exit program
    ''')
    return int(choose) if choose else 0


def choose_shape():
    while True:
        choose_shape = input(f'''Choose Shape:
        (1) Circle
        (2) Rectangle
        (3) Square
        (4) Triangle
        (5) EquilateralTriangle
        (6) ReqularPantagon
        ''')
        if not (1 <= int(choose_shape) <= 6):
            print("wrong number choose one shape")
        else:
            break
    choose_shape = int(choose_shape)
    if choose_shape == 1:
        return Circle
    elif choose_shape == 2:
        return Rectangle
    elif choose_shape == 3:
        return Square
    elif choose_shape == 4:
        return Triangle
    elif choose_shape == 5:
        return EquilateralTriangle
    elif choose_shape == 6:
        return ReqularPantagon


def add_shape():
    shape = choose_shape()
    obj = None
    if shape == Circle:
        r = float(input("r = "))
        obj = Circle(r)
    elif shape == Rectangle:
        a = float(input("a = "))
        b = float(input("b = "))
        obj = Rectangle(a, b)
    elif shape == Square:
        a = float(input("a = "))
        obj = Square(a)
    elif shape == Triangle:
        a = float(input("a = "))
        b = float(input("b = "))
        c = float(input("c = "))
        obj = Triangle(a, b, c)
    elif shape == EquilateralTriangle:
        a = float(input("a = "))
        obj = EquilateralTriangle(a)
    elif shape == ReqularPantagon:
        a = float(input("a = "))
        obj = ReqularPantagon(a)
    return obj


def main():
    shape_list = ShapeList()
    while True:
        choose = menu()
        print()
        if choose == 1:
            shape_list.add_shape(add_shape())
            print()
        elif choose == 2:
            print(shape_list.get_shapes_table())
            print()
        elif choose == 3:
            print(str(shape_list.get_largest_shape_by_perimeter()))
            print()
        elif choose == 4:
            print(str(shape_list.get_largest_shape_by_area()))
            print()
        elif choose == 5:
            shape = choose_shape()
            print(f"area formula = {shape.get_area_formula()}")
            print(f"perimeter formula = {shape.get_perimeter_formula()}")
            print()
        else:
            break


if __name__ == "__main__":
    main()
