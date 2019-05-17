# import unittest
#
# from src.ds.bst_pp import BSTPP
#
#
# class TestBSTPP(unittest.TestCase):
#
#     def test_constructor_withoutCompareFunction_shouldCreateEmptyBST(self):
#         bst = BSTPP()
#         for i in range(1, 20):
#             bst.put(i)
#         for i in range(1, 20):
#             self.assertTrue(bst.contains(i))
#             self.assertFalse(bst.contains(i, 0))
#
#         self.assertEqual(1, bst.min())
#         self.assertEqual(19, bst.max())
#
#         expected = "[]"
#         for i in range(1, 20):
#             if i == 1:
#                 expected = expected.replace("]", "{}]".format(i))
#             else:
#                 expected = expected.replace("]", ", {}]".format(i))
#
#         for i in range(1, 20):
#             bst.delete(i)
#
#         for i in range(40):
#             self.assertFalse(bst.contains(i))
#
#     def test_put_withNoneTypeArgument_shouldRaiseValueError(self):
#         bst = BSTPP()
#         with self.assertRaises(ValueError):
#             bst.put(None)
#
#     def test_put_withValidKey_shouldBehaveAsEphemeralBST(self):
#         bst = BSTPP()
#         for i in range(20):
#             bst.put(i)
#
#         for i in range(20):
#             self.assertTrue(bst.contains(i))
#
#     def test_delete_withNoneTypeArgument_shouldRaiseValueError(self):
#         bst = BSTPP()
#         with self.assertRaises(ValueError):
#             bst.delete(None)
#
#     def test_delete_withKeyNotInBST_shouldDoNothing(self):
#         bst = BSTPP()
#         for i in range(20):
#             bst.put(i)
#
#         bst.delete(20)
#         for i in range(20):
#             self.assertTrue(bst.contains(i))
#
#     def test_delete_withKeyInBST_shouldRemoveKeyFromCurrentBSTVersion(self):
#         bst = BSTPP()
#         for i in range(20):
#             bst.put(i)
#
#         for i in range(20):
#             bst.delete(i)
#             self.assertFalse(bst.contains(i))
#             for j in range(1, 20):
#                 print("{} {}".format(i, j))
#                 self.assertTrue(bst.contains(i, j))
#
#
#
