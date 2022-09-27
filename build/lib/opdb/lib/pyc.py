import sys


# def _file_header_length(python_version: Tuple[int, int, int, str, int]):
def _file_header_length(python_version):
    if python_version >= (3,):
        # https://github.com/python/cpython/blob/3.8/Lib/importlib/_bootstrap_external.py#L651-L669
        return 16
    elif python_version >= (2,):
        # https://github.com/python/cpython/blob/v2.7.18/Lib/py_compile.py#L123-L129
        return 8


def file_header_length():
    current_version = sys.version_info
    return _file_header_length(current_version)
