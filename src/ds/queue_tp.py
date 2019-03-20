from src.ds.deque_tp import DequeTP


class QueueTP:

    def __init__(self):
        self.__deque = DequeTP()

    def enqueue(self, value, version=None):
        self.__deque.push_back(value, version)

    def dequeue(self, version=None):
        return self.__deque.pop_front(version)

    def size(self, version=None):
        return self.__deque.size(version)

    def first(self, version=None):
        return self.__deque.front(version)

    def kth(self, k, version=None):
        return self.__deque.kth(k, version)

    def print(self, version=None):
        return self.__deque.print(version)
