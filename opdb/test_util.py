import types
from unittest import TestCase
from util import load_code_object


class Test(TestCase):
    def test_load_code_object(self):
        code_object = load_code_object("../example/__pycache__/sample.cpython-38.pyc")
        assert isinstance(code_object, types.CodeType)
