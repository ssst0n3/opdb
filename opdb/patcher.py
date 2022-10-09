import opcode
import sys
import hashlib
import types

import db
from lib import lnotab
from lib.pyc import file_header_length
from tracer import Tracer

FILENAME = ''
LAST = -1


def co_id(co):
    assert isinstance(co, types.CodeType)
    key = hashlib.md5(co.co_code).hexdigest()
    return key


class Patcher(Tracer):
    def __init__(self):
        super(Patcher, self).__init__()
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
    def patch_pop_jump(cls, code_object):
        """
        replace POP_JUMP_IF_FALSE to POP if the target is nop
        """
        i = 0
        co_code = code_object.co_code
        while i < len(co_code):
            op = db.util.load_op(co_code, i)
            arg, next_i = db.util.load_op_arg(op, co_code, i)
            if opcode.opname[op] in ['POP_JUMP_IF_FALSE']:
                target_op = db.util.load_op(co_code, arg)
                if opcode.opname[target_op] == 'NOP':
                    print("patch pop_jump")
                    co_code = co_code[:i] + chr(opcode.opmap['POP_TOP']) + b"\x09"*(next_i-i-1) + co_code[next_i:]
                    code_object = lnotab.new_code(code_object, code=co_code)
            i = next_i
        return code_object

    @classmethod
    def patch_pop_jump_nop(cls, code_object):
        """
        replace POP_JUMP_IF_FALSE to POP if the code before target is nop

            POP_JUMP_IF_FALSE <TARGET>
            NOP
            NOP
            NOP
            <TARGET>
        ====>
            POP
            NOP
            NOP
            NOP
            <TARGET>
        """
        i = 0
        co_code = code_object.co_code
        while i < len(co_code):
            op = db.util.load_op(co_code, i)
            arg, next_i = db.util.load_op_arg(op, co_code, i)
            if opcode.opname[op] in ['POP_JUMP_IF_FALSE']:
                if co_code[next_i:arg] == (arg-next_i)*b'\x09':
                    print("patch pop_jump_nop")
                    co_code = co_code[:i] + chr(opcode.opmap['POP_TOP']) + b"\x09"*(next_i-i-1) + co_code[next_i:]
                    code_object = lnotab.new_code(code_object, code=co_code)
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
            if opcode.opname[op] in ['DUP_TOP', 'POP_BLOCK']:
                print("DUP_TOP/POP_BLOCK found")
                j = i - 1
                while co_code[j] < len(opcode.opname) and opcode.opname[co_code[j]] == 'NOP':
                    print("fix NOP before DUP_TOP {} {}=>{}".format(j, co_code[j], old_code_object.co_code[j]))
                    co_code = co_code[:j] + old_code_object.co_code[j:j + 1] + co_code[j + 1:]
                    j -= 1
                new_code_object = lnotab.new_code(new_code_object, code=co_code)
            i = next_i
        return new_code_object

    @classmethod
    def fix_finally(cls, old_code_object, new_code_object):
        i = 0
        co_code = new_code_object.co_code
        old_co_code = old_code_object.co_code
        while i < len(old_co_code):
            op = db.util.load_op(old_co_code, i)
            _, next_i = db.util.load_op_arg(op, old_co_code, i)
            if opcode.opname[op] in ['END_FINALLY'] and opcode.opname[co_code[i]] == 'NOP':
                print("fix END_FINALLY", i)
                co_code = co_code[:i] + old_co_code[i:next_i] + co_code[next_i:]
                new_code_object = lnotab.new_code(new_code_object, code=co_code)
            i = next_i
        return new_code_object

    def do_patch(self, code_object):
        co_code = b'\x09' * len(code_object.co_code)
        # new_code_object = code_object.replace(co_code=co_code)
        new_code_object = lnotab.new_code(code_object, code=co_code)
        if co_id(code_object) not in self.codes:
            return None
        for i, code in self.codes[co_id(code_object)].items():
            if i >= 0:
                co_code = co_code[:i] + code + co_code[i + len(code):]
                # new_code_object = new_code_object.replace(co_code=co_code)
                new_code_object = lnotab.new_code(new_code_object, code=co_code)
        new_code_object = self.patch_jump_nop(new_code_object)
        new_code_object = self.patch_pop_jump(new_code_object)
        new_code_object = self.patch_pop_jump_nop(new_code_object)
        new_code_object = self.fix_extend_arg(code_object, new_code_object)
        new_code_object = self.fix_exception(code_object, new_code_object)
        new_code_object = self.fix_finally(code_object, new_code_object)
        return new_code_object

    def patch(self, code_object=None):
        if code_object is None:
            code_object = self.code_object
        print("patch:", code_object)
        patched = self.do_patch(code_object)
        if patched is not None:
            code_object = patched
        for i in range(len(code_object.co_consts)):
            const = code_object.co_consts[i]
            if isinstance(const, types.CodeType):
                const = self.patch(const)
                new_consts = code_object.co_consts[:i] + (const,) + code_object.co_consts[i + 1:]
                code_object = lnotab.new_code(code_object, consts=new_consts)
        return code_object


def patch(filename, globals=None, locals=None):
    patcher = Patcher()
    try:
        patcher.run(filename, globals, locals)
    except SystemExit:
        print("exiting")
    patched = patcher.patch()
    import marshal
    patched_file = "{}_patched.pyc".format(filename)
    print("patched_file:", patched_file)
    with open(patched_file, "wb") as pf:
        with open(filename, "rb") as of:
            pf.write(of.read()[:file_header_length()] + marshal.dumps(patched))
    return patched_file


if __name__ == '__main__':
    patch(sys.argv[1])
