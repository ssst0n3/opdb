import sys

from opdb import db
from opdb.util import load_code_object
from opdb.lib import lnotab


class Tracer:
    def __init__(self):
        self.last = -1
        self.filename = ''
        self.code_object = None

    def trace(self, frame, event, arg):
        # print(frame, event, arg)
        if self.filename == frame.f_code.co_filename:
            return self.dispatch_all(frame)
        #
        # if self.last == frame.f_lasti:
        #     return self.trace
        # self.last = frame.f_lasti
        # if self.filename == frame.f_code.co_filename:
        #     # if frame.f_code.co_name == '<module>':
        #     #     return self.trace
        #     print(frame.f_code.co_name)
        #     return self.dispatch_all(frame)
        # return self.trace

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
        code_object = lnotab.lnotab_all(code_object)
        self.code_object = code_object
        self.filename = code_object.co_filename
        sys.settrace(self.trace)
        if globals is None:
            import __main__
            globals = __main__.__dict__
        if locals is None:
            locals = globals
        exec(code_object, globals, locals)


def main():
    filename = sys.argv[1]
    Tracer().run(filename, None, None)


if __name__ == '__main__':
    main()
