import bdb
import inspect
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


def static_analysis(code, varnames, names, constants):
    i = 0
    while i < len(code):
        op = util.load_op(code, i)
        oparg, next_i = util.load_op_arg(op, code, i)
        disassemble_string(code[i:next_i], i, varnames, names, constants)

        i = next_i


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
            # logger.info("[predict]")
            # disassemble_string(code[lasti_end:lasti_end + 2], lasti_end, varnames, names, constants)
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
                    # print('[debug] ??????????')
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
        logger.debug("size: {} {}".format(size, self.curframe.f_code.co_stacksize))
        if '__return__' in self.curframe.f_locals:
            logger.info('return so do not read stack')
            return
        if '__exception__' in self.curframe.f_locals:
            logger.info('exception {} so do not read stack'.format(self.curframe.f_locals['__exception__']))
            return
        if size > self.curframe.f_code.co_stacksize:
            logger.warn('size bigger than stacksize {} {}'.format(size, self.curframe.f_code.co_stacksize))
            return
        for i in range(size):
            # logger.info("[stack] {}".format(pystack.getStackItem(self.curframe, i)))
            stack.append(pystack.getStackItem(self.curframe, i))
        logger.info("[stack] {}".format(stack))

    def do_inspect_frame(self, arg):
        logger.debug('[debug] inspect frame')
        logger.info(inspect.getmembers(self.curframe))

    def do_list_locals(self, arg):
        print('[locals]')
        for k, v in self.curframe.f_locals.items():
            if k not in self.fake_locals:
                print(k, '=', v)

    do_ll = do_list_locals

    def do_list_globals(self, arg):
        print('[globals]')
        for k, v in self.curframe.f_globals.items():
            if k not in self.fake_globals:
                print(k, '=', v)

    do_lg = do_list_globals

    def do_break(self, arg, temporary=0):
        if not arg:
            if self.breaks:  # There's at least one
                print("Num Type         Disp Enb   Where")
                for bp in bdb.Breakpoint.bpbynumber:
                    if bp:
                        bp.bpprint(self.stdout)
            return
        # parse arguments; comma has lowest precedence
        # and cannot occur in filename
        filename = None
        lineno = None
        cond = None
        comma = arg.find(',')
        if comma > 0:
            # parse stuff after comma: "condition"
            cond = arg[comma + 1:].lstrip()
            arg = arg[:comma].rstrip()
        # parse stuff before comma: [filename:]lineno | function
        colon = arg.rfind(':')
        funcname = None
        if colon >= 0:
            filename = arg[:colon].rstrip()
            f = self.lookupmodule(filename)
            if not f:
                print(self.stdout, '*** ', repr(filename))
                print(self.stdout, 'not found from sys.path')
                return
            else:
                filename = f
            arg = arg[colon + 1:].lstrip()
            try:
                lineno = int(arg)
            except ValueError as msg:
                print(self.stdout, '*** Bad lineno:', arg)
                return
        else:
            # no colon; can be lineno or function
            try:
                lineno = int(arg)
            except ValueError:
                try:
                    func = eval(arg,
                                self.curframe.f_globals,
                                self.curframe_locals)
                except:
                    func = arg
                try:
                    if hasattr(func, 'im_func'):
                        func = func.im_func
                    code = func.func_code
                    # use co_name to identify the bkpt (function names
                    # could be aliased, but co_name is invariant)
                    funcname = code.co_name
                    lineno = code.co_firstlineno
                    filename = code.co_filename
                except:
                    # last thing to try
                    (ok, filename, ln) = self.lineinfo(arg)
                    if not ok:
                        print('*** The specified object')
                        print(repr(arg))
                        print('is not a function')
                        print('or was not found along sys.path.')
                        return
                    funcname = ok  # ok contains a function name
                    lineno = int(ln)
        if not filename:
            filename = self.defaultFile()
        # Check for reasonable breakpoint
        # line = self.checkline(filename, lineno)
        line = lineno
        if line:
            # now set the break point
            # err = self.set_break(filename, line, temporary, cond, funcname)

            filename = self.canonic(filename)
            import linecache  # Import as late as possible
            # line = linecache.getline(filename, lineno)
            # if not line:
            #     err = 'Line %s:%d does not exist' % (filename,
            #                                           lineno)
            if not filename in self.breaks:
                self.breaks[filename] = []
            list = self.breaks[filename]
            if not lineno in list:
                list.append(lineno)
            bp = bdb.Breakpoint(filename, lineno, temporary, cond, funcname)

            # if err: print >>self.stdout, '***', err
            # else:
            bp = self.get_breaks(filename, line)[-1]
            print("Breakpoint %d at %s:%d" % (bp.number,
                                              bp.file,
                                              bp.line))

    do_b = do_break

    def do_break_until(self, arg):
        self.clear_all_breaks()
        return self.do_break(arg)


def disassemble_string(code, lasti=-1, varnames=None, names=None, constants=None):
    n = len(code)
    i = 0
    while i < n:
        c = code[i]
        op = util.load_op(code, i)
        # print(repr(i + lasti).rjust(4), opname[op].ljust(15))
        oparg, next_i = util.load_op_arg(op, code, i)
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
                    info += "{}".format(oparg)
            elif op in hasname:
                if names is not None:
                    # print('(' + names[oparg] + ')')
                    info += '(' + names[oparg] + ')'
                else:
                    # print('(%d)' % oparg)
                    info += "{}".format(oparg)
            elif op in hasjrel:
                # print('(to ' + repr(i + lasti + oparg) + ')')
                info += '(to ' + repr(i + lasti + oparg) + ')'
            elif op in haslocal:
                if varnames:
                    # print('(' + varnames[oparg] + ')')
                    info += '(' + varnames[oparg] + ')'
                else:
                    # print('(%d)' % oparg)
                    info += "{}".format(oparg)
            elif op in hascompare:
                # print('(' + cmp_op[oparg] + ')')
                info += '(' + cmp_op[oparg] + ')'
        # print()
        logger.info(info)
        i = next_i
