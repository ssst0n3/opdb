import sys
import opcode

from opdb.lib import lnotab
from opdb import db
from opdb.util import load_code_object

FILENAME = ''
LAST = -1


def dispatch_all(frame):
    lasti = frame.f_lasti
    code = frame.f_code.co_code
    varnames = frame.f_code.co_varnames
    names = frame.f_code.co_names
    constants = frame.f_code.co_consts
    op = db.util.load_op(code, lasti)
    oparg, nexti = db.util.load_op_arg(op, code, lasti)
    db.disassemble_string(code[lasti:nexti], lasti, varnames, names, constants)
    return trace


def dispatch_line(frame):
    pass


def dispatch_call(frame, arg):
    pass


def dispatch_return(frame, arg):
    return trace


def dispatch_exception(frame, arg):
    return trace


def trace(frame, event, arg):
    global LAST
    if LAST == frame.f_lasti:
        LAST = frame.f_lasti
        return trace
    LAST = frame.f_lasti
    if FILENAME == frame.f_code.co_filename:
        if frame.f_code.co_name == '<module>':
            return
        print(frame.f_code.co_name)
        return dispatch_all(frame)
    # if event == 'line':
    #     return dispatch_line(frame)
    # elif event == 'call':
    #     pass
    #     # return dispatch_call(frame, arg)
    # elif event == 'return':
    #     return dispatch_return(frame, arg)
    # elif event == 'exception':
    #     return dispatch_exception(frame, arg)
    # elif event == 'c_call':
    #     pass
    # elif event == 'c_exception':
    #     pass
    # elif event == 'c_return':
    #     pass
    # else:
    #     print('bdb.Bdb.dispatch: unknown debugging event:', repr(event))
    return trace


def run(filename):
    global FILENAME
    code_object = load_code_object(filename)
    FILENAME = code_object.co_filename
    sys.settrace(trace)
    code_object = lnotab.lnotab_all(code_object)
    # print(code_object.co_)
    exec(code_object, globals(), locals())


def main():
    filename = sys.argv[1]
    run(filename)


if __name__ == '__main__':
    main()
