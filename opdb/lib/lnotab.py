import sys
import types


def new_code(co, argcount=None, nlocals=None, stacksize=None, flags=None, code=None, consts=None, names=None,
             varnames=None, filename=None, name=None, firstlineno=None, lnotab=None):
    argcount = co.co_argcount if argcount is None else argcount
    nlocals = co.co_nlocals if nlocals is None else nlocals
    stacksize = co.co_stacksize if stacksize is None else stacksize
    flags = co.co_flags if flags is None else flags
    code = co.co_code if code is None else code
    consts = co.co_consts if consts is None else consts
    names = co.co_names if names is None else names
    varnames = co.co_varnames if varnames is None else varnames
    filename = co.co_filename if filename is None else filename
    # firstlineno = co.co_firstlineno if firstlineno is None else firstlineno
    # todo: change it to 0
    firstlineno = 1
    name = co.co_name if name is None else name
    lnotab = co.co_lnotab if lnotab is None else lnotab
    # noinspection PyArgumentList
    if sys.version_info < (2, 8):
        new_co = types.CodeType(
            argcount,
            nlocals,
            stacksize,
            flags,
            code,
            consts,
            names,
            varnames,
            filename,
            name,
            firstlineno,
            lnotab,
        )
    else:
        new_co = co.replace(
            co_argcount=argcount,
            co_nlocals=nlocals,
            co_stacksize=stacksize,
            co_flags=flags,
            co_code=code,
            co_consts=consts,
            co_names=names,
            co_varnames=varnames,
            co_filename=filename,
            co_firstlineno=firstlineno,
            co_name=name,
            co_lnotab=lnotab,
        )
    return new_co


def get_first_offset(co):
    print('[debug]', co.co_firstlineno)
    print('[debug] lnotab', co.co_name, repr(co.co_lnotab))
    lineno = 1
    offset = 0
    i = 0
    while i < len(co.co_lnotab) / 2 and lineno < co.co_firstlineno:
        offset += ord(co.co_lnotab[2 * i])
        lineno += ord(co.co_lnotab[2 * i + 1])
        i += 1
    print(lineno, offset, i)


# noinspection SpellCheckingInspection
def new_lnotab(co):
    lnotab = b'\x01\x01' * len(co.co_code)
    return new_code(co, lnotab=lnotab)


# noinspection SpellCheckingInspection
def lnotab_all(co):
    co = new_lnotab(co)
    new_consts = []
    for const in co.co_consts:
        if isinstance(const, types.CodeType):
            const = lnotab_all(const)
            new_consts.append(const)
        else:
            new_consts.append(const)
    return new_lnotab(new_code(co, consts=tuple(new_consts)))
