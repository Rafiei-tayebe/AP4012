import unittest


def multipy(a, b):
    return a * b


class Integer:
    def __init__(self, value):
        if not isinstance(value, int):
            raise TypeError()
        self.value = value

    def __repr__(self) -> str:
        return f"{self.value}"

    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other
        elif isinstance(other, Integer):
            return self.value == other.value
        else:
            raise TypeError()

    def __add__(self, other):
        if isinstance(other, Integer):
            return Integer(self.value + other.value)
        elif isinstance(other, Complex):
            return Complex(other.real + self.value, other.imag)

    def __mul__(self, other):
        if isinstance(other, Integer):
            return Integer(self.value * other.value)
        elif isinstance(other, Complex):
            return Complex(self.value * other.real, self.value * other.imag)

    def __sub__(self, other):
        if isinstance(other, Integer):
            return Integer(self.value - other.value)
        elif isinstance(other, Complex):
            return Complex(self.value - other.real, other.imag)


class Complex:
    def __init__(self, real, imag=0.0):
        if not (isinstance(real, int) or isinstance(real, float)):
            raise TypeError()
        if not (isinstance(imag, int) or isinstance(imag, float)):
            raise TypeError()
        self.real = real
        self.imag = imag

    def __repr__(self) -> str:
        if self.imag == 0:
            return f"{self.real}"
        return f"{self.real}+({self.imag})i"

    def __eq__(self, other):
        if isinstance(other, Complex):
            return (self.real == other.real) and (self.imag == other.imag)
        elif isinstance(other, str):
            return self.__repr__() == other
        else:
            raise TypeError()

    def __add__(self, other):
        if isinstance(other, Integer):
            return Complex(self.real + other.value, self.imag)
        elif isinstance(other, Complex):
            return Complex(self.real + other.real, self.imag + other.imag)

    def __mul__(self, other):
        if isinstance(other, Integer):
            return Complex(other.value * self.real, other.value * self.imag)
        elif isinstance(other, Complex):
            real = (self.real * other.real) - (self.imag * other.imag)
            imag = (self.real * other.imag) + (other.real * self.imag)
            return Complex(real, imag)

    def __sub__(self, other):
        if isinstance(other, Integer):
            return Complex(self.real - other.value, self.imag)
        elif isinstance(other, Complex):
            return Complex(self.real - other.real, self.imag - other.imag)


class Matrix:
    def __init__(self, row, column, values):
        if not isinstance(row, int):
            raise TypeError()

        if not isinstance(column, int):
            raise TypeError()

        if not isinstance(values, list):
            raise TypeError()

        if (row * column) != len(values):
            raise ValueError()

        for i in range(len(values)):
            if not (isinstance(values[i], Integer) or isinstance(values[i], Complex)):
                raise TypeError()

        self.row = row
        self.column = column

        self.matrix = []

        start, end = 0, self.column
        for _ in range(self.row):
            self.matrix.append(values[start:end])
            start = end
            end += self.column

    def __add__(self, other):
        if isinstance(other, Matrix):
            if (self.row == other.row) and (self.column == other.column):
                values = []
                for r in range(self.row):
                    for c in range(self.column):
                        values.append(self.matrix[r][c] + other.matrix[r][c])
                return Matrix(self.row, self.column, values)
        else:
            raise TypeError()

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if (self.row == other.column) and (self.column == other.row):
                values = []
                sum_values = Integer(0)
                for r in range(self.row):
                    for c in range(other.column):
                        for v1, v2 in zip(self.matrix[r], [row[c] for row in other.matrix]):
                            sum_values += (v1 * v2)
                        values.append(sum_values)
                        sum_values = Integer(0)
                return Matrix(self.row, other.column, values)
        elif isinstance(other, Integer) or isinstance(other, Complex):
            values = []
            for r in range(self.row):
                for c in range(self.column):
                    values.append(self.matrix[r][c] * other)
            return Matrix(self.row, self.column, values)
        else:
            raise TypeError()

    def __sub__(self, other):
        if isinstance(other, Matrix):
            if (self.row == other.row) and (self.column == other.column):
                values = []
                for r in range(self.row):
                    for c in range(self.column):
                        values.append(self.matrix[r][c] - other.matrix[r][c])
                return Matrix(self.row, self.column, values)
        else:
            raise TypeError()

    @staticmethod
    def make_unit_matrix(n):
        matrix = []
        for i in range(n):
            row = []
            for j in range(n):
                if i == j:
                    row.append(Integer(1))
                else:
                    row.append(Integer(0))
            matrix.append(row.copy())
        return matrix

    @staticmethod
    def get_ith_row(matrix, i):
        if len(matrix) < i:
            raise ValueError()
        return matrix[i]

    @staticmethod
    def get_ith_col(matrix, i):
        return [row[i] for row in matrix]

    @staticmethod
    def is_zero_matrix(matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] != Integer(0):
                    return False
        return True

    @staticmethod
    def is_unit_matrix(matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if i == j and matrix[i][j] != Integer(1):
                    return False
                elif i != j and matrix[i][j] != Integer(0):
                    return False
        return True

    @staticmethod
    def is_top_triangular_matrix(matrix):
        for i in range(1, len(matrix)):
            for j in range(i):
                if matrix[i][j] != Integer(0):
                    return False
        return True

    @staticmethod
    def is_bottom_triangular_matrix(matrix):
        for i in range(len(matrix)):
            for j in range(i+1, len(matrix)):
                if matrix[i][j] != Integer(0):
                    return False
        return True

    @classmethod
    def make_matrix_from_string(cls, elements):
        if isinstance(elements, str):
            elements = elements.split(',')
            row = len(elements)
            column = len(elements[0].split(' '))
            values = []
            for element in elements:
                element = element.split(' ')
                for e in element:
                    if e.isdigit():
                        values.append(Integer(int(e)))
                    else:
                        if 'i' in e:
                            if e.startswith('-'):
                                e = e[1::]
                                if '-' in e:
                                    e = e.split('-')
                                else:
                                    e = e.split('+')
                                values.append(
                                    Complex(-int(e[0]), int(e[1].split('i')[0])))
                            else:
                                if '-' in e:
                                    e = e.split('-')
                                else:
                                    e = e.split('+')
                                values.append(
                                    Complex(int(e[0]), int(e[1].split('i')[0])))
                        elif e.startswith('-'):
                            values.append(Integer(int(e)))
            return cls(row, column, values)
        else:
            raise ValueError()


class IntegerTest(unittest.TestCase):
    def test_create_integer(self):
        self.assertEqual(Integer(20), 20)
        self.assertEqual(Integer(2), 2)
        self.assertEqual(Integer(0), 0)
        self.assertEqual(Integer(-10), -10)

    def test_create_bad_integer(self):
        with self.assertRaises(TypeError):
            Integer(10.1)
            Integer("20")

    def test_add_two_integer(self):
        self.assertEqual(Integer(20) + Integer(10), Integer(30))
        self.assertEqual(Integer(0) + Integer(10), Integer(10))
        self.assertEqual(Integer(-20) + Integer(10), Integer(-10))

    def test_multipy_two_integer(self):
        self.assertEqual(Integer(10) * Integer(10), Integer(100))
        self.assertEqual(Integer(10) * Integer(0), Integer(0))
        self.assertEqual(Integer(10) * Integer(-10), Integer(-100))

    def test_sub_two_integer(self):
        self.assertEqual(Integer(10) - Integer(8), Integer(2))
        self.assertEqual(Integer(10) - Integer(0), Integer(10))
        self.assertEqual(Integer(0) - Integer(10), Integer(-10))

    def test_add_with_complex(self):
        self.assertEqual(Integer(10) + Complex(20, 1), Complex(30, 1))
        self.assertEqual(Integer(-10) + Complex(20, 1), Complex(10, 1))
        self.assertEqual(Integer(10) + Complex(-10, 1), Complex(0, 1))

    def test_multipy_with_complex(self):
        self.assertEqual(Integer(10) * Complex(10, 1), Complex(100, 10))
        self.assertEqual(Integer(2) * Complex(20), Complex(40))
        self.assertEqual(Integer(0) * Complex(10, 1), Complex(0))

    def test_sub_with_complex(self):
        self.assertEqual(Integer(10) - Complex(20, 3), Complex(-10, 3))
        self.assertEqual(Integer(10) - Complex(10), Complex(0))
        self.assertEqual(Integer(100) - Complex(0, 100), Complex(100, 100))


class ComplexTest(unittest.TestCase):
    def test_create_complex(self):
        self.assertEqual(Complex(10, 1), "10+(1)i")
        self.assertEqual(Complex(20), "20")
        self.assertEqual(Complex(20, 2.3), "20+(2.3)i")
        self.assertEqual(Complex(20, -20), "20+(-20)i")
        self.assertEqual(Complex(10, 10), "10+(10)i")

    def test_bad_create_complex(self):
        with self.assertRaises(TypeError):
            Complex("20", 3)
            Complex("20", "20.4")
            Complex(3, True)
            Complex(2, "2.2")
            Complex(True, 3.3)
            Complex(True, False)

    def test_add_two_complex(self):
        self.assertEqual(Complex(10, 1) + Complex(1), Complex(11, 1))
        self.assertEqual(Complex(20, -1) + Complex(-10), Complex(10, -1))

    def test_multipy_two_complex(self):
        self.assertEqual(Complex(1, 2) * Complex(2), Complex(2, 4))
        self.assertEqual(Complex(3, 1) * Complex(2, 2), Complex(4, 8))
        self.assertEqual(Complex(0, 1) * Complex(1, 2), Complex(-2, 1))
        self.assertEqual(Complex(1, 1) * Complex(0, 2), Complex(-2, 2))

    def test_sub_two_complex(self):
        self.assertEqual(Complex(10) - Complex(10), Complex(0))
        self.assertEqual(Complex(20, 1) - Complex(5, 1), Complex(15))
        self.assertEqual(Complex(20) - Complex(0), Complex(20))
        self.assertEqual(Complex(10, 3) - Complex(7, -4), Complex(3, 7))

    def test_add_with_integer(self):
        self.assertEqual(Complex(10) + Integer(10), Complex(20))
        self.assertEqual(Complex(10, 2) + Integer(2), Complex(12, 2))

    def test_multipy_with_integer(self):
        self.assertEqual(Complex(10, 1) * Integer(10), Complex(100, 10))
        self.assertEqual(Complex(20, 2) * Integer(0), Complex(0))
        self.assertEqual(Complex(2) * Integer(2), Complex(4))

    def test_sub_with_integer(self):
        self.assertEqual(Complex(20) - Integer(20), Complex(0))
        self.assertEqual(Complex(20, 1) - Integer(10), Complex(10, 1))
        self.assertEqual(Complex(10, 10) - Integer(10), Complex(0, 10))


class MatrixTest(unittest.TestCase):
    def test_bad_row_and_col(self):
        with self.assertRaises(TypeError):
            Matrix("1", 2, [1, 2])
            Matrix(1, "2", [1, 2])

    def test_bad_size(self):
        with self.assertRaises(ValueError):
            Matrix(1, 2, [Integer(i) for i in range(100)])
            Matrix(2, 2, [1])

    def test_bad_values_type(self):
        with self.assertRaises(TypeError):
            Matrix(1, 2, "[1, 2, 3]")
            Matrix(12, 12, True)

    def test_add_two_matrix(self):
        matrix = [[Integer(2), Integer(3)], [Integer(4), Integer(3)]]
        self.assertEqual(
            (Matrix(2, 2, [Integer(1), Integer(2), Integer(4), Integer(1)]) + Matrix(2, 2, [Integer(1), Integer(1), Integer(0), Integer(2)])).matrix, matrix)

    def test_mul_two_matrix(self):
        m1 = Matrix(2, 2, [Integer(2), Integer(0), Integer(3), Integer(1)])
        m2 = Matrix(2, 2, [Integer(1), Integer(2), Integer(4), Integer(1)])
        m_result = [[Integer(2), Integer(4)],
                    [Integer(7), Integer(7)]]
        self.assertEqual((m1*m2).matrix, m_result)

    def test_mul_complex_to_matrix(self):
        m = Matrix(2, 2, [Integer(2), Integer(0), Integer(3), Integer(1)])
        c = Complex(3, 1)
        matirx = [[Complex(6, 2), Complex(0)],
                  [Complex(9, 3), Complex(3, 1)]]
        self.assertEqual((m * c).matrix, matirx)

    def test_mul_integer_to_matrix(self):
        m = Matrix(2, 2, [Integer(2), Integer(0), Integer(3), Integer(1)])
        i = Integer(3)
        matirx = [[Integer(6), Integer(0)],
                  [Integer(9), Integer(3)]]
        self.assertEqual((m * i).matrix, matirx)

    def test_sub_two_matrix(self):
        m1 = Matrix(2, 2, [Integer(2), Integer(3), Integer(0), Integer(4)])
        m2 = Matrix(2, 2, [Integer(1), Integer(2), Integer(9), Integer(4)])
        result = [[Integer(1), Integer(1)], [Integer(-9), Integer(0)]]
        self.assertEqual((m1-m2).matrix, result)

    def test_make_unit_matrix(self):
        matrix = [[1, 0],
                  [0, 1]]
        self.assertEqual(Matrix.make_unit_matrix(2), matrix)

    def test_get_ith_row(self):
        matrix = [[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]]
        self.assertEqual(Matrix.get_ith_row(matrix, 1), matrix[1])

    def test_get_ith_col(self):
        matrix = [[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]]
        self.assertEqual(Matrix.get_ith_col(matrix, 1), [2, 5, 8])

    def test_is_zero_matrix(self):
        self.assertTrue(Matrix.is_zero_matrix([[0, 0], [0, 0]]))
        self.assertFalse(Matrix.is_zero_matrix([[0, 1], [0, 0]]))

    def test_is_unit_matrix(self):
        self.assertTrue(Matrix.is_unit_matrix([[1, 0], [0, 1]]))
        self.assertFalse(Matrix.is_unit_matrix([[1, 1], [0, 1]]))

    def test_is_top_triangular_matrix(self):
        matrix = [[1, 2, 3],
                  [0, 4, 5],
                  [0, 0, 6]]
        self.assertTrue(Matrix.is_top_triangular_matrix(matrix))
        matrix[2][0] = 10
        self.assertFalse(Matrix.is_top_triangular_matrix(matrix))

    def test_is_bottom_triangular_matrix(self):
        matrix = [[1, 0, 0],
                  [2, 3, 0],
                  [4, 5, 6]]
        self.assertTrue(Matrix.is_bottom_triangular_matrix(matrix))
        matrix[0][2] = 10
        self.assertFalse(Matrix.is_bottom_triangular_matrix(matrix))

    def test_make_matrix_from_string(self):
        matrix = [[Integer(1), Integer(2)], [Integer(3), Integer(4)]]
        self.assertEqual(Matrix.make_matrix_from_string(
            '1 2,3 4').matrix, matrix)


class MultipyTest(unittest.TestCase):
    def test_multipy_integer_complex(self):
        self.assertEqual(multipy(Complex(3, 1), Integer(2)), Complex(6, 2))
        self.assertEqual(multipy(Integer(2), Complex(3, 1)), Complex(6, 2))
        self.assertEqual(multipy(Complex(6), Integer(5)), Complex(30))

    def test_multipy_integer_matrix(self):
        m = Matrix(2, 2, [Integer(2), Integer(0), Integer(3), Integer(1)])
        i = Integer(2)
        matirx = [[Integer(4), Integer(0)],
                  [Integer(6), Integer(2)]]
        self.assertEqual(multipy(m, i).matrix, matirx)

    def test_multipy_complex_matrix(self):
        m = Matrix(2, 2, [Integer(2), Integer(0), Integer(3), Integer(1)])
        c = Complex(3, 1)
        matirx = [[Complex(6, 2), Complex(0)],
                  [Complex(9, 3), Complex(3, 1)]]
        self.assertEqual(multipy(m, c).matrix, matirx)
