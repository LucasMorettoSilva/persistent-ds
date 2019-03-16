import unittest

from src.ds.stack_tp import StackTP


class TestStackTP(unittest.TestCase):

    def test_constructor_shouldReturnEmptyStack(self):
        s = StackTP()
        self.assertEqual(0, s.size())
        self.assertIsNone(s.top())

    def test_push_withCurrentVersion_shouldInsertElementInTheCurrentStackVersion(self):
        # Should behave as ephemeral stack
        s = StackTP()
        for i in range(1, 20):
            s.push(i)
            self.assertEqual(i, s.size())
            self.assertEqual(i, s.top())

    def test_push_withDifferentVersions_shouldInsertElementAtGivenVersion(self):
        s = StackTP()
        for i in range(1, 20):
            s.push(i)

        # Version 0 = []
        s.push(2, 0)
        self.assertEqual(1, s.size())

        # Version 1 = [1]
        s.push(2, 1)
        self.assertEqual(2, s.size())

        # Version 2 = [2, 1]
        s.push(3, 2)
        self.assertEqual(3, s.size())

        for i in range(3, 20):
            # Version i = [i, ..., 1]
            s.push(0, i)
            self.assertEqual(i + 1, s.size())

    def test_top_withCurrentVersion_shouldReturnTopElementOfCurrentStackVersion(self):
        # Should behave as ephemeral stack
        s = StackTP()
        for i in range(1, 20):
            s.push(i)
            self.assertEqual(i, s.top())

    def test_top_withDifferentVersions_shouldReturnTopElementOfGivenStackVersion(self):
        s = StackTP()
        for i in range(1, 20):
            s.push(i)

        self.assertIsNone(s.top(0))
        for i in range(1, 20):
            self.assertEqual(i, s.top(i))

        # Version 0 = []
        s.push(1, 0)
        self.assertEqual(1, s.top())

        # Version 1 = [1]
        s.push(2, 1)
        self.assertEqual(2, s.top())

        # Version 2 = [2, 1]
        s.push(3, 2)
        self.assertEqual(3, s.top())

        for i in range(3, 20):
            # Version i = [i, ..., 1]
            s.push(0, i)
            self.assertEqual(i + 1, s.size())
            self.assertEqual(0, s.top())

    def test_pop_withCurrentVersion_shouldRemoveAndReturnTopStackElementOfCurrentVersion(self):
        # Should behave as ephemeral stack
        s = StackTP()
        for i in range(1, 20):
            s.push(i)

        for i in range(19, 0, -1):
            self.assertEqual(i, s.pop())
            self.assertEqual(i - 1, s.size())
            if i == 1:
                self.assertIsNone(s.top())
            else:
                self.assertEqual(i - 1, s.top())

    def test_pop_withDifferentVersions_shouldRemoveAndReturnTopStackElementOfGivenVersion(self):
        s = StackTP()
        for i in range(1, 20):
            s.push(i)

        # Version 0 = []
        self.assertIsNone(s.top(0))

        for i in range(1, 20):
            # Version i = [i, ..., 1]
            self.assertEqual(i, s.pop(i))

    def test_kth_withEmptyStackVersion_shouldRaiseIndexError(self):
        s = StackTP()
        for i in range(-20, 20):
            with self.assertRaises(IndexError):
                s.kth(i)

    def test_kth_withCurrentVersionAndIndexOutOfBounds_shouldRaiseIndexError(self):
        s = StackTP()
        s.push(0)
        for i in range(-20, 1):
            with self.assertRaises(IndexError):
                s.kth(i)
        for i in range(2, 20):
            with self.assertRaises(IndexError):
                s.kth(i)

    def test_kth_withDifferentVersionsAndIndexOutOfBounds_shouldRaiseIndexError(self):
        s = StackTP()
        for i in range(1, 20):
            s.push(i)

        for i in range(1, 20):
            for j in range(-20, 1):
                with self.assertRaises(IndexError):
                    s.kth(j, i)
            for j in range(i + 1, 40):
                with self.assertRaises(IndexError):
                    s.kth(j, i)

    def test_kth_withCurrentVersionAndValidIndex_shouldReturnStackElementAtGivenIndex(self):
        s = StackTP()
        for i in range(1, 20):
            s.push(i)

        for i in range(1, 20):
            self.assertEqual(i, s.kth(i))

    def test_kth_withDifferentVersionsAndValidIndex_shouldReturnStackElementAtGivenIndexAndGivenVersion(self):
        s = StackTP()
        for i in range(1, 20):
            s.push(i)

        for i in range(1, 20):
            # Version i = [i, ..., 1]
            for j in range(1, i):
                self.assertEqual(j, s.kth(j, i))



