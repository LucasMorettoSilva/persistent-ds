import unittest

from src.ds.queue_tp import QueueTP


class TestQueueTP(unittest.TestCase):
    
    def test_constructor_shouldReturnEmptyQueue(self):
        q = QueueTP()
        self.assertEqual(0, q.size())
        self.assertIsNone(q.first())

    def test_enqueue_withEmptyQueueAndNoneArgument_shouldRaiseValueError(self):
        q = QueueTP()
        with self.assertRaises(ValueError):
            q.enqueue(None)

    def test_enqueue_withDifferentVersionsAndNoneArgument_shouldRaiseValueError(self):
        q = QueueTP()
        for i in range(1, 20):
            q.enqueue(i)

        for i in range(0, 20):
            with self.assertRaises(ValueError):
                q.enqueue(None, i)

    def test_enqueue_withInvalidVersionNumber_shouldRaiseValueError(self):
        q = QueueTP()
        for i in range(1, 20):
            q.enqueue(i)

        for i in range(-20, 0):
            with self.assertRaises(ValueError):
                q.enqueue(1, i)

        for i in range(20, 40):
            with self.assertRaises(ValueError):
                q.enqueue(1, i)

    def test_enqueue_withCurrentVersion_shouldInsertElementAtEndOfCurrentQueueVersion(self):
        # Should behave as ephemeral queue
        q = QueueTP()
        for i in range(1, 20):
            q.enqueue(i)
            self.assertEqual(i, q.size())

    def test_enqueue_withDifferentVersions_shouldInsertElementAtGivenVersion(self):
        q = QueueTP()
        for i in range(1, 20):
            q.enqueue(i)

        # Version 0 = []
        q.enqueue(2, 0)
        self.assertEqual(1, q.size())

        # Version 1 = [1]
        q.enqueue(2, 1)
        self.assertEqual(2, q.size())

        # Version 2 = [1, 2]
        q.enqueue(3, 2)
        self.assertEqual(3, q.size())

        for i in range(3, 20):
            # Version i = [1, ..., i]
            q.enqueue(0, i)
            self.assertEqual(i + 1, q.size())

    def test_first_withInvalidVersionNumber_shouldRaiseValueError(self):
        q = QueueTP()
        for i in range(1, 20):
            q.enqueue(i)

        for i in range(-20, 0):
            with self.assertRaises(ValueError):
                q.first(i)

        for i in range(20, 40):
            with self.assertRaises(ValueError):
                q.first(i)

    def test_first_withEmptyQueue_shouldReturnNone(self):
        self.assertIsNone(QueueTP().first())

    def test_first_withCurrentVersion_shouldReturnFirstElementOfCurrentQueueVersion(self):
        # Should behave as ephemeral queue
        q = QueueTP()
        for i in range(1, 20):
            q.enqueue(i)
            self.assertEqual(i, q.first())
            q.dequeue()

    def test_first_withDifferentVersions_shouldReturnFirstElementOfGivenQueueVersion(self):
        q = QueueTP()
        for i in range(1, 20):
            q.enqueue(i)
        for i in range(1, 20):
            q.dequeue()

        self.assertIsNone(q.first(0))

        size = 18
        expected = 2
        for i in range(20, 38):
            # Version i = [i, ..., 20]
            self.assertEqual(size, q.size(i))
            self.assertEqual(expected, q.first(i))
            expected += 1
            size -= 1

    def test_dequeue_withInvalidVersionNumber_shouldRaiseValueError(self):
        q = QueueTP()
        for i in range(1, 20):
            q.enqueue(i)

        for i in range(-20, 0):
            with self.assertRaises(ValueError):
                q.dequeue(i)

        for i in range(20, 40):
            with self.assertRaises(ValueError):
                q.dequeue(i)

    def test_dequeue_withEmptyQueue_shouldReturnNone(self):
        self.assertIsNone(QueueTP().dequeue())

    def test_dequeue_withCurrentVersion_shouldRemoveAndReturnFirstQueueElementOfCurrentVersion(self):
        # Should behave as ephemeral queue
        q = QueueTP()
        for i in range(1, 20):
            q.enqueue(i)

        for i in range(1, 20):
            size = q.size()
            self.assertEqual(i, q.dequeue())
            self.assertEqual(size - 1, q.size())
            if i == 19:
                self.assertIsNone(q.first())
            else:
                self.assertEqual(i + 1, q.first())

    def test_dequeue_withDifferentVersions_shouldRemoveAndReturnFirstQueueElementOfGivenVersion(self):
        q = QueueTP()
        for i in range(1, 20):
            q.enqueue(i)
        for i in range(1, 20):
            q.dequeue()

        expected = 2
        for i in range(20, 38):
            # Version i = [expected, ..., 20]
            self.assertEqual(expected, q.dequeue(i))
            expected += 1

    def test_kth_withInvalidVersionNumber_shouldRaiseValueError(self):
        q = QueueTP()
        for i in range(1, 20):
            q.enqueue(i)

        for i in range(-20, 0):
            with self.assertRaises(ValueError):
                q.kth(1, i)

        for i in range(20, 40):
            with self.assertRaises(ValueError):
                q.kth(1, i)

    def test_kth_withEmptyQueueVersion_shouldRaiseIndexError(self):
        q = QueueTP()
        for i in range(-20, 20):
            with self.assertRaises(IndexError):
                q.kth(i)

    def test_kth_withCurrentVersionAndIndexOutOfBounds_shouldRaiseIndexError(self):
        q = QueueTP()
        q.enqueue(0)
        for i in range(-20, 1):
            with self.assertRaises(IndexError):
                q.kth(i)
        for i in range(2, 20):
            with self.assertRaises(IndexError):
                q.kth(i)

    def test_kth_withDifferentVersionsAndIndexOutOfBounds_shouldRaiseIndexError(self):
        q = QueueTP()
        for i in range(1, 20):
            q.enqueue(i)

        for i in range(1, 20):
            for j in range(-20, 1):
                with self.assertRaises(IndexError):
                    q.kth(j, i)
            for j in range(i + 1, 40):
                with self.assertRaises(IndexError):
                    q.kth(j, i)

    def test_kth_withCurrentVersionAndValidIndex_shouldReturnQueueElementAtGivenIndex(self):
        # Should behave as ephemeral stack
        q = QueueTP()
        for i in range(1, 20):
            q.enqueue(i)

        for i in range(1, 20):
            self.assertEqual(i, q.kth(i))

    def test_kth_withDifferentVersionsAndValidIndex_shouldReturnStackElementAtGivenIndexAndGivenVersion(self):
        q = QueueTP()
        for i in range(1, 20):
            q.enqueue(i)

        for i in range(1, 20):
            # Version i = [i, ..., 1]
            for j in range(1, i):
                self.assertEqual(j, q.kth(j, i))

    def test_size_withInvalidVersionNumber_shouldRaiseValueError(self):
        q = QueueTP()
        for i in range(-20, 0):
            with self.assertRaises(ValueError):
                q.size(i)
        for i in range(1, 20):
            with self.assertRaises(ValueError):
                q.size(i)

    def test_size_withEmptyQueue_shouldReturnZero(self):
        q = QueueTP()
        self.assertEqual(0, q.size())

    def test_size_withCurrentVersionAndSequencesOfInsertAndDelete_shouldReturnCorrectSize(self):
        # Should behave as ephemeral stack
        q = QueueTP()
        for i in range(1, 20):
            q.enqueue(i)
            self.assertEqual(i, q.size())

        for i in range(19, 0, -1):
            q.dequeue()
            self.assertEqual(i - 1, q.size())

    def test_size_withDifferentVersions_shouldReturnCorrectSizeAtGivenVersion(self):
        q = QueueTP()
        for i in range(1, 20):
            q.enqueue(i)

        for i in range(0, 20):
            self.assertEqual(i, q.size(i))

    def test_print_withInvalidVersionNumber_shouldRaiseValueError(self):
        q = QueueTP()
        for i in range(1, 20):
            q.enqueue(i)

        for i in range(-20, 0):
            with self.assertRaises(ValueError):
                q.print(i)

        for i in range(20, 40):
            with self.assertRaises(ValueError):
                q.print(i)

    def test_print_withEmptyQueue_shouldReturnEmptyQueueRepresentation(self):
        self.assertEqual("[]", QueueTP().print())

    def test_print_withCurrentVersion_shouldReturnCurrentQueueRepresentation(self):
        expected = "[]"
        q = QueueTP()
        for i in range(1, 20):
            if i == 1:
                expected = expected.replace("[", "[{}".format(i))
            else:
                expected = expected.replace("]", ", {}]".format(i))

            q.enqueue(i)
            self.assertEqual(expected, q.print())

    def test_print_withDifferentVersions_shouldReturnQueueRepresentationAtGivenVersion(self):
        expected = "[]"
        version = list()
        version.append(expected)

        q = QueueTP()
        for i in range(1, 20):
            if i == 1:
                expected = expected.replace("[", "[{}".format(i))
            else:
                expected = expected.replace("]", ", {}]".format(i))
            version.append(expected)
            q.enqueue(i)

        for i in range(20):
            self.assertEqual(version[i], q.print(i))
