import dis
import marshal
import opcode
import sys
from lib.pyc import file_header_length
from log import logger

EXTENDED_ARG27 = 0
EXTENDED_ARG3 = 0


def load_code_object(filename):
    """
    load code object from pyc file
    :param filename: the file path of pyc
    :return: The type for code objects such as returned by compile().
            https://docs.python.org/3/library/functions.html#compile
    """
    f = open(filename, 'rb')
    f.seek(file_header_length())
    code_object = marshal.load(f)
    f.close()
    return code_object


def load_op(code, index):
    op = code[index]
    if not isinstance(op, int):
        op = ord(op)
    return op


def _load_op_arg38(op, code, i):
    global EXTENDED_ARG3
    if op >= opcode.HAVE_ARGUMENT:
        arg = code[i + 1] | EXTENDED_ARG3
        EXTENDED_ARG3 = (arg << 8) if op == opcode.EXTENDED_ARG else 0
    else:
        arg = None
    return arg, i + 2


def _load_op_arg27(op, code, i):
    i += 1
    global EXTENDED_ARG27
    if op >= opcode.HAVE_ARGUMENT:
        oparg = ord(code[i]) + ord(code[i + 1]) * 256 + EXTENDED_ARG27
        EXTENDED_ARG27 = oparg * 65536 if op == opcode.EXTENDED_ARG else 0
        i += 2
    else:
        oparg = None
    return oparg, i


def load_op_arg(op, code, i):
    if sys.version_info < (3,):
        oparg, next_i = _load_op_arg27(op, code, i)
    elif sys.version_info >= (3,):
        oparg, next_i = _load_op_arg38(op, code, i)
    else:
        return
    logger.debug("index:{} opname:{} oparg:{}".format(i, opcode.opname[op], oparg))
    return oparg, next_i
