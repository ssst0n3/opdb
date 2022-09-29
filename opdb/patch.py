import opcode
import sys
import types

from opdb import db
from opdb.lib import lnotab
from opdb.trace import Tracer

FILENAME = ''
LAST = -1


def co_id(co):
    assert isinstance(co, types.CodeType)
    return co.co_code


class Patcher(Tracer):
    def __init__(self):
        super().__init__()
        self.codes = {}

    def dispatch_all(self, frame):
        lasti = frame.f_lasti
        code = frame.f_code.co_code
        op = db.util.load_op(code, lasti)
        oparg, nexti = db.util.load_op_arg(op, code, lasti)
        key = co_id(frame.f_code)
        if key not in self.codes:
            self.codes[key] = {}
        self.codes[key][lasti] = code[lasti:nexti]
        return self.trace

    @classmethod
    def patch_jump_nop(cls, code_object):
        i = 0
        jump = False
        jump_from = None
        co_code = code_object.co_code
        while i < len(co_code):
            op = db.util.load_op(co_code, i)
            _, next_i = db.util.load_op_arg(op, co_code, i)
            if jump:
                jump = False
                if 'NOP' == opcode.opname[op]:
                    print("patch jump-nop", jump_from)
                    co_code = co_code[:jump_from[0]] + b"\x09" * (jump_from[1] - jump_from[0]) + co_code[jump_from[1]:]
                    code_object = lnotab.new_code(code_object, code=co_code)
            if opcode.opname[op] in ['JUMP_FORWARD']:
                jump = True
                jump_from = (i, next_i)
            i = next_i
        return code_object

    @classmethod
    def fix_extend_arg(cls, old_code_object, new_code_object):
        i = 0
        extend = False
        co_code = new_code_object.co_code
        while i < len(co_code):
            op = db.util.load_op(co_code, i)
            _, next_i = db.util.load_op_arg(op, co_code, i)
            if extend:
                extend = False
                if 'NOP' == opcode.opname[op]:
                    print("fix EXTENDED_ARG")
                    co_code = co_code[:i] + old_code_object.co_code[i:next_i] + co_code[next_i:]
                    new_code_object = lnotab.new_code(new_code_object, code=co_code)
            if opcode.opname[op] in ['EXTENDED_ARG']:
                extend = True
            i = next_i
        return new_code_object

    @classmethod
    def fix_exception(cls, old_code_object, new_code_object):
        i = 0
        co_code = new_code_object.co_code
        while i < len(co_code):
            op = db.util.load_op(co_code, i)
            _, next_i = db.util.load_op_arg(op, co_code, i)
            if opcode.opname[op] in ['DUP_TOP']:
                print("DUP_TOP found")
                j = i - 1
                while co_code[j] < len(opcode.opname) and opcode.opname[co_code[j]] == 'NOP':
                    print("fix NOP before DUP_TOP")
                    co_code = co_code[:j] + old_code_object.co_code[j:j + 1] + co_code[j + 1:]
                    new_code_object = lnotab.new_code(new_code_object, code=co_code)
                    j -= 1
            i = next_i
        return new_code_object

    def do_patch(self, code_object):
        co_code = b'\x09' * len(code_object.co_code)
        new_code_object = code_object
        for i, code in self.codes[co_id(code_object)].items():
            co_code = co_code[:i] + code + co_code[i + len(code):]
            new_code_object = lnotab.new_code(code_object, code=co_code)
        new_code_object = self.patch_jump_nop(new_code_object)
        new_code_object = self.fix_extend_arg(code_object, new_code_object)
        new_code_object = self.fix_exception(code_object, new_code_object)
        return new_code_object

    def patch(self, code_object=None):
        if code_object is None:
            code_object = self.code_object
        print("patch:", code_object)
        code_object = self.do_patch(code_object)
        for i in range(len(code_object.co_consts)):
            const = code_object.co_consts[i]
            if isinstance(const, types.CodeType):
                const = self.patch(const)
                new_consts = code_object.co_consts[:i] + (const,) + code_object.co_consts[i + 1:]
                code_object = lnotab.new_code(code_object, consts=new_consts)
        return code_object


def main():
    filename = sys.argv[1]
    patcher = Patcher()
    try:
        patcher.run(filename, None, None)
    except SystemExit:
        print("exiting")
    # finally:
    # print("code:", patcher.codes.keys())
    # print("code:", patcher.codes['<module>'])
    patched = patcher.patch()
    import marshal
    with open("patcher_patched.pyc", "wb") as f:
        f.write(open(filename, "rb").read()[:16] + marshal.dumps(patched))
    # import dis
    # dis.disassemble(patched.co_consts[6].co_consts[-3])


if __name__ == '__main__':
    main()