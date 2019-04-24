import unittest

from src.ds.bst_pp import BSTPP


class TestBSTPP(unittest.TestCase):

    def test_constructor_withoutCompareFunction_shouldCreateEmptyBST(self):
        bst = BSTPP()
        for i in range(1, 20):
            bst.insert(i)
        for i in range(1, 20):
            self.assertTrue(bst.contains(i))
            self.assertFalse(bst.contains(i, 0))

        self.assertEqual(1, bst.min())
        self.assertEqual(19, bst.max())

        expected = "[]"
        for i in range(1, 20):
            if i == 1:
                expected = expected.replace("]", "{}]".format(i))
            else:
                expected = expected.replace("]", ", {}]".format(i))

        for i in range(1, 20):
            bst.delete(i)

        for i in range(40):
            self.assertFalse(bst.contains(i))
