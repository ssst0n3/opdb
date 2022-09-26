import os
import uuid
from unittest import TestCase
from pyc import _file_header_length, file_header_length
import py_compile


class Test(TestCase):
    def test__pyc_file_header_length(self):
        length = _file_header_length((3, 8, 5, "final", 0))
        assert length == 16
        length = _file_header_length((2, 7, 17, "final", 0))
        assert length == 8

    def test_file_header_length(self):
        length = file_header_length
        filename = str(uuid.uuid4())
        py_path = "/tmp/" + filename + ".py"
        pyc_path = py_path + "c"
        open(py_path, "wb").close()
        compiled_pyc_path = py_compile.compile(py_path)
        if compiled_pyc_path is not None:
            pyc_path = compiled_pyc_path
        print("pyc_path: ", pyc_path)
        with open(pyc_path, "rb") as f:
            # https://github.com/python/cpython/blob/v3.8.0/Python/marshal.c#L67
            flag_ref = 0x80
            # print("read:", c.read()[file_header_length()])
            type_code = f.read()[file_header_length()]
            if not isinstance(type_code, int):
                type_code = ord(type_code)
            assert type_code in [ord('c'), flag_ref | ord('c')]
        os.remove(py_path)
        os.remove(pyc_path)
