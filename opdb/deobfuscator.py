import opcode
import util
from log import logger

JUMP = [opcode.opmap['JUMP_ABSOLUTE'], opcode.opmap['JUMP_FORWARD']]
POP_JUMP = [opcode.opmap['POP_JUMP_IF_TRUE'], opcode.opmap['POP_JUMP_IF_FALSE']]
DIVIDER = -1


def jump_until_target(code, i):
    op = util.load_op(code, i)
    if op >= opcode.HAVE_ARGUMENT:
        oparg, next_i = util.load_op_arg(op, code, i)
        if op == opcode.opmap['JUMP_ABSOLUTE']:
            return jump_until_target(code, oparg)
        elif op == opcode.opmap['JUMP_FORWARD']:
            return jump_until_target(code, next_i + oparg)
    # i dont know why only i+1 can trigger bp
    return i


def check_divider_jump(op, const, divider):
    return (const == divider) == (POP_JUMP.index(op) == 0)


def bypass_divider_continuous(code, lasti, varnames, consts):
    global DIVIDER
    lasti = jump_until_target(code, lasti)
    i = lasti
    op = util.load_op(code, i)
    if op >= opcode.HAVE_ARGUMENT and op == opcode.opmap['LOAD_CONST']:
        oparg, i = util.load_op_arg(op, code, i)
        const = consts[oparg]
        logger.debug(const)

        i = jump_until_target(code, i)
        op = util.load_op(code, i)
        if op >= opcode.HAVE_ARGUMENT and op == opcode.opmap['STORE_FAST']:
            oparg, i = util.load_op_arg(op, code, i)
            if varnames[oparg] == 'DIVIDER':
                DIVIDER = const
                return bypass_divider_continuous(code, i, varnames, consts)
        elif op >= opcode.HAVE_ARGUMENT and op == opcode.opmap['LOAD_FAST']:
            oparg, next_i = util.load_op_arg(op, code, i)
            if varnames[oparg] == 'DIVIDER':
                i = next_i
                i = jump_until_target(code, i)
                op = ord(code[i])
                if op >= opcode.HAVE_ARGUMENT and op == opcode.opmap['COMPARE_OP']:
                    oparg, next_i = util.load_op_arg(op, code, i)
                    if oparg == 2:
                        i = next_i

                        i = jump_until_target(code, i)
                        op = ord(code[i])
                        if op >= opcode.HAVE_ARGUMENT and op in POP_JUMP:
                            oparg, i = util.load_op_arg(op, code, i)
                            if check_divider_jump(op, const, DIVIDER):
                                return bypass_divider_continuous(code, oparg, varnames, consts)
                                # return oparg + 1
                            else:
                                return bypass_divider_continuous(code, i, varnames, consts)
                                # return i + 1
    return lasti


def bypass_store_divider(code, lasti, consts):
    global DIVIDER
    lasti = jump_until_target(code, lasti)
    i = lasti
    op = ord(code[i])
    if op >= opcode.HAVE_ARGUMENT and op == opcode.opmap['LOAD_CONST']:
        oparg, i = util.load_op_arg(op, code, i)
        const = consts[oparg]
        logger.debug(const)

        i = jump_until_target(code, i)
        op = ord(code[i])
        if op >= opcode.HAVE_ARGUMENT and op == opcode.opmap['STORE_FAST']:
            pass

    return


def bypass(frame):
    global DIVIDER
    co = frame.f_code
    code = co.co_code
    lasti = frame.f_lasti
    varnames = co.co_varnames
    consts = co.co_consts
    DIVIDER = frame.f_locals['DIVIDER'] if 'DIVIDER' in frame.f_locals else None

    # jump
    i = jump_until_target(code, lasti)
    i = bypass_divider_continuous(code, i, varnames, consts)
    return i


def bypass_for_iter(code, i):
    op = util.load_op(code, i)
    oparg, next_i = util.load_op_arg(op, code, i)
    target = next_i + oparg
    logger.info(target)
    return target
