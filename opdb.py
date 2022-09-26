import opcode
from dis import opname, HAVE_ARGUMENT, hasconst, hasname, hasjrel, haslocal, hascompare, cmp_op
from pdb import Pdb
import pystack
from log import logger

import deobfuscator
import util
from lib.lnotab import lnotab_all


# noinspection PyShadowingBuiltins
def run(statement, fake_globals, fake_locals, globals=None, locals=None):
    new_code_object = lnotab_all(statement)
    OPdb(new_code_object.co_filename, fake_globals, fake_locals).run(new_code_object, globals, locals)


class OPdb(Pdb):
    def __init__(self, filename, fake_globals, fake_locals, completekey='tab', stdin=None, stdout=None, skip=None):
        self.filename = filename
        self.fake_globals = fake_globals
        self.fake_locals = fake_locals
        Pdb.__init__(self, completekey, stdin, stdout, skip)
        self.prompt = self.prompt.replace('Pdb', 'opdb')

    def do_step(self, arg):
        if self.curframe.f_code.co_filename == self.filename:
            lasti = self.curframe.f_lasti
            code = self.curframe.f_code.co_code
            varnames = self.curframe.f_code.co_varnames
            names = self.curframe.f_code.co_names
            constants = self.curframe.f_code.co_consts
            logger.info('[lasti] {}'.format(lasti))
            self.do_stack(arg)
            op = util.load_op(code, lasti)
            _, lasti_end = util.load_op_arg(op, code, lasti)
            if op < opcode.HAVE_ARGUMENT:
                disassemble_string(code[lasti:lasti_end], lasti, varnames, names, constants)
                Pdb.do_step(self, arg)
            else:
                if op in deobfuscator.JUMP or op == opcode.opmap['LOAD_CONST']:
                    target = deobfuscator.bypass(self.curframe)
                    if target != lasti:
                        self.clear_all_breaks()
                        self.do_break(str(target + 1))
                        self._set_stopinfo(self.curframe, self.curframe, -1)
                        return 1
                elif op == opcode.opmap['FOR_ITER']:
                    print('[debug] ??????????')
                    disassemble_string(code[lasti:lasti_end], lasti, varnames, names, constants)
                    target = deobfuscator.bypass_for_iter(code, lasti)
                    self.clear_all_breaks()
                    self.do_break(str(target + 1))
                    self._set_stopinfo(self.curframe, self.curframe, -1)
                    return 1
                disassemble_string(code[lasti:lasti_end], lasti, varnames, names, constants)
                Pdb.do_step(self, arg)
            return Pdb.do_step(self, arg)
        else:
            return Pdb.do_return(self, arg)

    do_s = do_step

    def do_stack(self, arg):
        stack = []
        size = pystack.getStackSize(self.curframe)
        logger.debug("size: {}".format(size))
        if '__return__' in self.curframe.f_locals:
            logger.debug('return but not get stack')
            return
        for i in range(size):
            stack.append(pystack.getStackItem(self.curframe, i))
        logger.info("[stack] {}".format(stack))


def disassemble_string(code, lasti=-1, varnames=None, names=None, constants=None):
    n = len(code)
    i = 0
    while i < n:
        c = code[i]
        op = util.load_op(code, i)
        # print(repr(i + lasti).rjust(4), opname[op].ljust(15))
        oparg, i = util.load_op_arg(op, code, i)
        info = "{} {} {}".format(i + lasti, opname[op], oparg)
        # i = i + 1
        if op >= HAVE_ARGUMENT:
            # oparg = util.load_op_arg(op, code, i-1)
            # i = i + 2
            # print(repr(oparg).rjust(5), )
            if op in hasconst:
                if constants:
                    # print('(' + repr(constants[oparg]) + ')')
                    info += " ({}) ".format(repr(constants[oparg]))
                else:
                    # print('(%d)' % oparg)
                    info += "%d".format(oparg)
            elif op in hasname:
                if names is not None:
                    # print('(' + names[oparg] + ')')
                    info += '(' + names[oparg] + ')'
                else:
                    # print('(%d)' % oparg)
                    info += "%d".format(oparg)
            elif op in hasjrel:
                # print('(to ' + repr(i + lasti + oparg) + ')')
                info += '(to ' + repr(i + lasti + oparg) + ')'
            elif op in haslocal:
                if varnames:
                    # print('(' + varnames[oparg] + ')')
                    info += '(' + varnames[oparg] + ')'
                else:
                    # print('(%d)' % oparg)
                    info += "%d".format(oparg)
            elif op in hascompare:
                # print('(' + cmp_op[oparg] + ')')
                info += '(' + cmp_op[oparg] + ')'
        # print()
        logger.info(info)
