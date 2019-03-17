import unittest

from src.ds.deque_tp import DequeTP


class TestDequeTP(unittest.TestCase):

    def test_constructor_shouldReturnEmptyDeque(self):
        d = DequeTP()
        self.assertEqual(0, d.size())
        self.assertIsNone(d.front())
        self.assertIsNone(d.back())
    
    def test_pushFront_withEmptyDequeAndNoneValueArgument_shouldRaiseValueError(self):
        d = DequeTP()
        with self.assertRaises(ValueError):
            d.push_front(None)

    def test_pushFront_withValidVersionAndNoneTypeValueArgument_shouldRaiseValueError(self):
        d = DequeTP()
        for i in range(1, 20):
            d.push_front(i)

        for i in range(0, 20):
            with self.assertRaises(ValueError):
                d.push_front(None, i)
    
    def test_pushFront_withInvalidVersionAndValidValueArgument_shouldRaiseValueError(self):
        d = DequeTP()
        for i in range(1, 20):
            d.push_front(i)

        for i in range(-20, 0):
            with self.assertRaises(ValueError):
                d.push_front(1, i)

        for i in range(20, 40):
            with self.assertRaises(ValueError):
                d.push_front(1, i)
    
    def test_pushFront_withEmptyDeque_shouldInsertElementAtDequeAsFirstAndLastElement(self):
        d = DequeTP()
        self.assertIsNone(d.front())
        self.assertIsNone(d.back())
        
        d.push_front(1)
        self.assertEqual(1, d.front())
        self.assertEqual(1, d.back())
    
    def test_pushFront_withCurrentVersion_shouldInsertElementInFrontOfCurrentDequeVersion(self):
        # Should behave as ephemeral deque
        d = DequeTP()
        for i in range(1, 20):
            d.push_front(i)
            self.assertEqual(i, d.front())

    def test_pushFront_withDifferentVersions_shouldInsertElementInFrontOfGivenVersion(self):
        d = DequeTP()
        for i in range(1, 20):
            d.push_front(i)

        # Version 0 = []
        d.push_front(0, 0)
        self.assertEqual(0, d.front())
        self.assertEqual(0, d.back())

        # Version 1 = [1]
        d.push_front(2, 1)
        self.assertEqual(2, d.front())
        self.assertEqual(1, d.back())

        for i in range(3, 20):
            # Version i = [i, ..., 1]
            d.push_front(0, i)
            self.assertEqual(0, d.front())

    def test_pushBack_withEmptyDequeAndNoneValueArgument_shouldRaiseValueError(self):
        d = DequeTP()
        with self.assertRaises(ValueError):
            d.push_front(None)

    def test_pushBack_withValidVersionAndNoneTypeValueArgument_shouldRaiseValueError(self):
        d = DequeTP()
        for i in range(1, 20):
            d.push_back(i)

        for i in range(0, 20):
            with self.assertRaises(ValueError):
                d.push_back(None, i)

    def test_pushBack_withInvalidVersionAndValidValueArgument_shouldRaiseValueError(self):
        d = DequeTP()
        for i in range(1, 20):
            d.push_back(i)

        for i in range(-20, 0):
            with self.assertRaises(ValueError):
                d.push_back(1, i)

        for i in range(20, 40):
            with self.assertRaises(ValueError):
                d.push_back(1, i)

    def test_pushBack_withEmptyDeque_shouldInsertElementAtDequeAsFirstAndLastElement(self):
        d = DequeTP()
        self.assertIsNone(d.front())
        self.assertIsNone(d.back())

        d.push_back(1)
        self.assertEqual(1, d.front())
        self.assertEqual(1, d.back())

    def test_pushBack_withCurrentVersion_shouldInsertElementInBackOfCurrentDequeVersion(self):
        # Should behave as ephemeral deque
        d = DequeTP()
        for i in range(1, 20):
            d.push_back(i)
            self.assertEqual(i, d.back())

    def test_pushBack_withDifferentVersions_shouldInsertElementInBackOfGivenVersion(self):
        d = DequeTP()
        for i in range(1, 20):
            d.push_back(i)

        # Version 0 = []
        d.push_back(0, 0)
        self.assertEqual(0, d.front())
        self.assertEqual(0, d.back())

        # Version 1 = [1]
        d.push_back(2, 1)
        self.assertEqual(2, d.back())
        self.assertEqual(1, d.front())

        for i in range(3, 20):
            # Version i = [1, ..., i]
            d.push_back(0, i)
            self.assertEqual(0, d.back())

    def test_popFront_withEmptyDeque_shouldReturnNone(self):
        self.assertIsNone(DequeTP().pop_front())
    
    def test_popFront_withInvalidVersionNumber_shouldRaiseValueError(self):
        d = DequeTP()
        for i in range(1, 20):
            d.push_front(i)

        for i in range(-20, 0):
            with self.assertRaises(ValueError):
                d.pop_front(i)
        for i in range(20, 40):
            with self.assertRaises(ValueError):
                d.pop_front(i)
    
    def test_popFront_withCurrentVersion_shouldRemoveAndReturnFrontOfCurrentDequeVersion(self):
        # Should behave as ephemeral deque
        d = DequeTP()
        for i in range(1, 20):
            d.push_front(i)

        for i in range(19, 0, -1):
            self.assertEqual(i, d.pop_front())
            if i == 1:
                self.assertIsNone(d.front())
            else:
                self.assertEqual(i - 1, d.front())
    
    def test_popFront_withDifferentVersions_shouldRemoveAndReturnFrontOfGivenDequeVersion(self):
        d = DequeTP()
        for i in range(1, 20):
            d.push_front(i)

        # Version 0 = []
        self.assertIsNone(d.front(0))

        for i in range(1, 20):
            # Version i = [i, ..., 1]
            self.assertEqual(i, d.pop_front(i))

    def test_popBack_withEmptyDeque_shouldReturnNone(self):
        self.assertIsNone(DequeTP().pop_back())

    def test_popBack_withInvalidVersionNumber_shouldRaiseValueError(self):
        d = DequeTP()
        for i in range(1, 20):
            d.push_back(i)

        for i in range(-20, 0):
            with self.assertRaises(ValueError):
                d.pop_back(i)
        for i in range(20, 40):
            with self.assertRaises(ValueError):
                d.pop_back(i)

    def test_popBack_withCurrentVersion_shouldRemoveAndReturnBackOfCurrentDequeVersion(self):
        # Should behave as ephemeral deque
        d = DequeTP()
        for i in range(1, 20):
            d.push_back(i)

        for i in range(19, 0, -1):
            self.assertEqual(i, d.pop_back())
            if i == 1:
                self.assertIsNone(d.back())
            else:
                self.assertEqual(i - 1, d.back())

    def test_popBack_withDifferentVersions_shouldRemoveAndReturnFrontOfGivenDequeVersion(self):
        d = DequeTP()
        for i in range(1, 20):
            d.push_back(i)

        # Version 0 = []
        self.assertIsNone(d.back(0))

        for i in range(1, 20):
            # Version i = [i, ..., 1]
            self.assertEqual(i, d.pop_back(i))
    
    def test_kth_withInvalidVersionNumber_shouldRaiseValueError(self):
        d = DequeTP()
        for i in range(1, 20):
            d.push_front(i)

        for i in range(-20, 0):
            with self.assertRaises(ValueError):
                d.kth(1, i)

        for i in range(20, 40):
            with self.assertRaises(ValueError):
                d.kth(1, i)

    def test_kth_withEmptyDequeVersion_shouldRaiseIndexError(self):
        d = DequeTP()
        for i in range(-20, 20):
            with self.assertRaises(IndexError):
                d.kth(i)

    def test_kth_withCurrentVersionAndIndexOutOfBounds_shouldRaiseIndexError(self):
        d = DequeTP()
        d.push_front(0)
        for i in range(-20, 1):
            with self.assertRaises(IndexError):
                d.kth(i)
        for i in range(2, 20):
            with self.assertRaises(IndexError):
                d.kth(i)

    def test_kth_withDifferentVersionsAndIndexOutOfBounds_shouldRaiseIndexError(self):
        d = DequeTP()
        for i in range(1, 20):
            d.push_front(i)

        for i in range(1, 20):
            for j in range(-20, 1):
                with self.assertRaises(IndexError):
                    d.kth(j, i)
            for j in range(i + 1, 40):
                with self.assertRaises(IndexError):
                    d.kth(j, i)
    
    def test_kth_withCurrentVersionAndValidIndex_shouldReturnDequeElementAtGivenIndex(self):
        # Should behave as ephemeral deque
        d = DequeTP()
        for i in range(1, 20):
            d.push_front(i)

        for i in range(1, 20):
            self.assertEqual(20 - i, d.kth(i))

    def test_kth_withDifferentVersionsAndValidIndex_shouldReturnDequeElementAtGivenIndexAndGivenVersion(self):
        d = DequeTP()
        for i in range(1, 20):
            d.push_back(i)

        for i in range(1, 20):
            # Version i = [1, ..., i]
            for j in range(1, i):
                self.assertEqual(j, d.kth(j, i))
    
    def test_size_withInvalidVersionNumber_shouldRaiseValueError(self):
        d = DequeTP()
        for i in range(-20, 0):
            with self.assertRaises(ValueError):
                d.size(i)
        for i in range(1, 20):
            with self.assertRaises(ValueError):
                d.size(i)

    def test_size_withEmptyDeque_shouldReturnZero(self):
        d = DequeTP()
        self.assertEqual(0, d.size())

    def test_size_withCurrentVersionAndSequencesOfInsertAndDelete_shouldReturnCorrectSize(self):
        # Should behave as ephemeral deque
        d = DequeTP()
        for i in range(1, 20):
            d.push_front(i)
            self.assertEqual(i, d.size())

        for i in range(19, 0, -1):
            d.pop_front()
            self.assertEqual(i - 1, d.size())

    def test_size_withDifferentVersions_shouldReturnCorrectSizeAtGivenVersion(self):
        d = DequeTP()
        for i in range(1, 20):
            d.push_front(i)

        for i in range(0, 20):
            self.assertEqual(i, d.size(i))
    
    def test_print_withInvalidVersionNumber_shouldRaiseValueError(self):
        d = DequeTP()
        for i in range(1, 20):
            d.push_front(i)

        for i in range(-20, 0):
            with self.assertRaises(ValueError):
                d.print(i)

        for i in range(20, 40):
            with self.assertRaises(ValueError):
                d.print(i)

    def test_print_withEmptyDeque_shouldReturnEmptyDequeRepresentation(self):
        self.assertEqual("[]", DequeTP().print())

    def test_print_withCurrentVersion_shouldReturnCurrentDequeRepresentation(self):
        expected = "[]"
        d = DequeTP()
        for i in range(1, 20):
            if i == 1:
                expected = expected.replace("[", "[{}".format(i))
            else:
                expected = expected.replace("[", "[{}, ".format(i))

            d.push_front(i)
            self.assertEqual(expected, d.print())

        expected = "[]"
        d = DequeTP()
        for i in range(1, 20):
            if i == 1:
                expected = expected.replace("]", "{}]".format(i))
            else:
                expected = expected.replace("]", ", {}]".format(i))

            d.push_back(i)
            self.assertEqual(expected, d.print())

    def test_print_withDifferentVersions_shouldReturnDequeRepresentationAtGivenVersion(self):
        expected = "[]"
        version = list()
        version.append(expected)

        d = DequeTP()
        for i in range(1, 20):
            if i == 1:
                expected = expected.replace("[", "[{}".format(i))
            else:
                expected = expected.replace("[", "[{}, ".format(i))
            version.append(expected)
            d.push_front(i)

        for i in range(20):
            self.assertEqual(version[i], d.print(i))

        expected = "[]"
        version = list()
        version.append(expected)

        d = DequeTP()
        for i in range(1, 20):
            if i == 1:
                expected = expected.replace("]", "{}]".format(i))
            else:
                expected = expected.replace("]", ", {}]".format(i))
            version.append(expected)
            d.push_back(i)

        for i in range(20):
            self.assertEqual(version[i], d.print(i))
