import sys

import db
from util import load_code_object
from lib import lnotab


class Tracer(object):
    def __init__(self):
        self.last = -1
        self.filename = ''
        self.code_object = None

    def trace(self, frame, event, arg):
        if self.filename == frame.f_code.co_filename:
            return self.dispatch_all(frame)

    def dispatch_all(self, frame):
        lasti = frame.f_lasti
        code = frame.f_code.co_code
        varnames = frame.f_code.co_varnames
        names = frame.f_code.co_names
        constants = frame.f_code.co_consts
        op = db.util.load_op(code, lasti)
        oparg, nexti = db.util.load_op_arg(op, code, lasti)
        db.disassemble_string(code[lasti:nexti], lasti, varnames, names, constants)
        return self.trace

    def run(self, filename, globals, locals):
        code_object = load_code_object(filename)
        self.code_object = code_object
        code_object = lnotab.lnotab_all(code_object)
        self.filename = code_object.co_filename
        sys.settrace(self.trace)
        if globals is None:
            import __main__
            globals = __main__.__dict__
        if locals is None:
            locals = globals
        exec(code_object, globals, locals)


def trace(filename):
    Tracer().run(filename, None, None)


if __name__ == '__main__':
    trace(sys.argv[1])
