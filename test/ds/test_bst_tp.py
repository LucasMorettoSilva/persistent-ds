import random
import unittest

from src.ds.bst_tp import BSTTP


class TestBSTTP(unittest.TestCase):

    def test_constructor_shouldCreateEmptyBSTWithOnlyTrivialVersion(self):
        bst = BSTTP()
        self.assertEqual(0, bst.size())

        for i in range(1, 20):
            with self.assertRaises(ValueError):
                bst.size(i)

    def test_put_withNoneTypeArgumentKey_shouldRaiseValueError(self):
        bst = BSTTP()
        with self.assertRaises(ValueError):
            bst.put(None, 0)

    def test_put_withCurrentVersion_shouldBehaveAsEphemeralBST(self):
        bst = BSTTP()
        for i in range(1, 20):
            bst.put(i, i)
            self.assertEqual(i, bst.size())
            self.assertTrue(bst.contains(i))
        for i in range(1, 20):
            self.assertTrue(bst.contains(i))

    def test_put_withDifferentVersions_shouldPutElementOnlyAtGivenVersion(self):
        bst = BSTTP()
        for i in range(1, 20):
            bst.put(i, i)

        # Version 0 = []
        bst.put(1, 1, 0)
        self.assertEqual(1, bst.size())
        for i in range(2, 20):
            self.assertFalse(bst.contains(i))

        # Version 1 = [1]
        bst.put(2, 2, 1)
        self.assertEqual(2, bst.size())
        for i in range(3, 20):
            self.assertFalse(bst.contains(i))

        for v in range(3, 20):
            bst.put(v, v, v)
            self.assertEqual(v, bst.size())

    def test_get_withNoneTypeArgumentKey_shouldRaiseValueError(self):
        bst = BSTTP()
        with self.assertRaises(ValueError):
            bst.get(None)

    def test_get_withKeyNotInGivenVersion_shouldReturnNone(self):
        bst = BSTTP()
        for i in range(1, 20):
            bst.put(i, i)

        for v in range(1, 20):
            for i in range(v, 20):
                self.assertIsNone(bst.get(i + 1, v))

    def test_get_withKeyInGivenVersion_shouldReturnValueOfKey(self):
        bst = BSTTP()
        for i in range(1, 20):
            bst.put(i, -i)

        for i in range(1, 20):
            self.assertEqual(-i, bst.get(i))

        for v in range(1, 20):
            for i in range(1, v + 1):
                self.assertEqual(-i, bst.get(i, v))

    def test_contains_withKeyNotInGivenVersion_shouldReturnFalse(self):
        bst = BSTTP()
        for i in range(-20, 20):
            self.assertFalse(bst.contains(i))

        for i in range(1, 20):
            bst.put(i, i)

        for v in range(1, 20):
            for i in range(v, 20):
                self.assertFalse(bst.contains(i + 1, v))

    def test_contains_withKeyInGivenVersion_shouldReturnTrue(self):
        bst = BSTTP()

        for i in range(1, 20):
            bst.put(i, i)

        for v in range(1, 20):
            for i in range(1, v + 1):
                self.assertTrue(bst.contains(i, v))

    def test_delete_withNoneTypeArgumentKey_shouldRaiseValueError(self):
        bst = BSTTP()
        with self.assertRaises(ValueError):
            bst.delete(None)

    def test_delete_withKeyInBSTAndOnlyCurrentVersion_shouldBehaveAsEphemeralBST(self):
        bst = BSTTP()
        for i in range(1, 20):
            bst.put(i, i)
        for i in range(1, 20):
            bst.delete(i)
            self.assertFalse(bst.contains(i))
            self.assertEqual(19 - i, bst.size())

    def test_delete_withKeyNotInGivenVersion_shouldNotAlterBSTAndNotCreateNewVersion(self):
        bst = BSTTP()
        for i in range(1, 20):
            bst.put(i, i)

        for v in range(1, 20):
            for i in range(20, 40):
                bst.delete(i, v)
                self.assertEqual(v, bst.size(v))
                self.assertEqual(19, bst.size())

    def test_delete_withKeyInGivenVersion_shouldDeleteKeyOnlyFromGivenVersionAndCreateNewVersionWithModifications(self):
        bst = BSTTP()
        for i in range(1, 20):
            bst.put(i, i)

        for v in range(1, 20):
            for i in range(1, v + 1):
                bst.delete(i, v)
                self.assertTrue(bst.contains(i, v))
                self.assertFalse(bst.contains(i))

                self.assertEqual(v - 1, bst.size())
                self.assertEqual(v, bst.size(v))

    def test_min_withEmptyVersion_shouldRaiseAttributeError(self):
        bst = BSTTP()
        with self.assertRaises(AttributeError):
            bst.min()

    def test_min_withNotEmptyVersion_shouldReturnSmallestKeyFromGivenVersion(self):
        bst = BSTTP()
        for i in range(-1, -20, -1):
            bst.put(i, i)
        for i in range(1, 20):
            self.assertEqual(-i, bst.min(i))

    def test_max_withEmptyVersion_shouldRaiseAttributeError(self):
        bst = BSTTP()
        with self.assertRaises(AttributeError):
            bst.max()

    def test_max_withNotEmptyVersion_shouldReturnLargestKeyFromGivenVersion(self):
        bst = BSTTP()
        for i in range(1, 20):
            bst.put(i, i)
        for i in range(1, 20):
            self.assertEqual(i, bst.max(i))

    def test_deleteMin_withEmptyVersion_shouldRaiseAttributeError(self):
        bst = BSTTP()
        with self.assertRaises(AttributeError):
            bst.delete_min()

    def test_deleteMin_withNotEmptyVersion_shouldDeleteSmallestKeyFromGivenVersionAndCreateNewVersion(self):
        bst = BSTTP()
        for i in range(1, 20):
            bst.put(-i, i)
        for i in range(1, 20):
            bst.delete_min(i)
            self.assertEqual(i - 1, bst.size())
            self.assertFalse(bst.contains(-i))

            self.assertEqual(i, bst.size(i))
            self.assertTrue(bst.contains(-i, i))

    def test_deleteMax_withEmptyVersion_shouldRaiseAttributeError(self):
        bst = BSTTP()
        with self.assertRaises(AttributeError):
            bst.delete_max()

    def test_deleteMax_withNotEmptyVersion_shouldDeleteLargestKeyFromGivenVersionAndCreateNewVersion(self):
        bst = BSTTP()
        for i in range(1, 20):
            bst.put(i, i)
        for i in range(1, 20):
            bst.delete_max(i)
            self.assertEqual(i - 1, bst.size())
            self.assertFalse(bst.contains(i))

            self.assertEqual(i, bst.size(i))
            self.assertTrue(bst.contains(i, i))

    def test_keysInOrder_withEmptyVersion_shouldReturnEmptyRepresentation(self):
        bst = BSTTP()
        self.assertEqual("[]", str(bst.keys_in_order()))

    def test_keysInOrder_withNotEmptyVersion_shouldReturnInOrderRepresentationOfKeysInGivenVersion(self):
        bst = BSTTP()
        expected = ["[]"]
        inputs   = random.sample(range(1, 100), 30)

        aux = []
        for i in inputs:
            aux.append(i)
            aux.sort()
            expected.append(str(aux))
            bst.put(i, i)

        for i in range(len(expected)):
            self.assertEqual(expected[i], str(bst.keys_in_order(i)))
