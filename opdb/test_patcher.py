import os
import sys
from unittest import TestCase
# print(sys.path)
from patcher import co_id


class Test(TestCase):
    def test_co_id(self):
        def f():
            print('hello world')

        key = co_id(f.__code__)
        print(key)
        assert (len(key) == 32)

    def runTest(self):
        self.test_co_id()


if __name__ == '__main__':
    Test()
