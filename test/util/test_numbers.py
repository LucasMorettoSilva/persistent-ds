import unittest

from src.util.numbers import Numbers


class TestNumbers(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestNumbers, self).__init__(*args, **kwargs)
        self.__data = [
            (0,  0),
            (1,  1),
            (2,  2),
            (3,  10),
            (4,  11),
            (5,  12),
            (6,  20),
            (7,  100),
            (8,  101),
            (9,  102),
            (10, 110),
            (11, 111),
            (12, 112),
            (13, 120),
            (14, 200),
            (15, 1000)
        ]

    def test_skewBinary_withNegativeNumbers_shouldRaiseValueError(self):
        with self.assertRaises(ValueError):
            for i in range(1, 20):
                Numbers.skew_binary(-1 * i)

    def test_skewBinary_withPositiveNumbers_shouldConvertNumberToSkewBinaryRepresentation(self):
        for number, expected in self.__data:
            self.assertEqual(expected, Numbers.skew_binary(number))

