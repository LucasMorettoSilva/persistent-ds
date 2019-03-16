import unittest

from src.util.numbers import Numbers


class TestNumbers(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestNumbers, self).__init__(*args, **kwargs)
        self.__data_dec_skew = [
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
        self.__data_skew_nonzero = [
            (0, 0),
            (1, 1),
            (2, 1),
            (3, 1),
            (4, 1),
            (5, 1),
            (6, 1),
            (7, 1),
            (8, 1),
            (9, 1),
            (10, 2),
            (11, 1),
            (12, 1),
            (13, 1),
            (14, 1),
            (15, 1),
            (100, 3),
            (1000, 4)
        ]

    def test_skewBinary_withNegativeNumbers_shouldRaiseValueError(self):
        with self.assertRaises(ValueError):
            for i in range(1, 20):
                Numbers.skew_binary(-1 * i)

    def test_skewBinary_withPositiveNumbers_shouldConvertNumberToSkewBinaryRepresentation(self):
        for number, expected in self.__data_dec_skew:
            self.assertEqual(expected, Numbers.skew_binary(number))

    def test_nonZero_withZero_shouldReturnZero(self):
        self.assertEqual(0, Numbers.non_zero(0))

    def test_nonZero_withPositiveNumbers_shouldReturnTheIndexOfTheLessSignificantDigitThatDiffersFromZero(self):
        for number, expected in self.__data_skew_nonzero:
            self.assertEqual(expected, Numbers.non_zero(number))

