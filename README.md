# opdb

opcode level debugger for python

## install 

* pip install opdb

## debug

```
from opdb.debugger import debug
debug('sample.cpython-38.pyc')
```

OR

```
$ python debug.py sample.cpython-38.pyc

> /home/ctf/notebook/sample.py(1)<module>()
-> #!/usr/bin/env python
(opdb) s
[INFO] [do_step] [lasti] 0
[INFO] [do_stack] [stack] []
[INFO] [disassemble_string] 0 LOAD_CONST 0 (<code object f at 0x7f77015ec190, file "sample.py", line 1>) 
> /home/ctf/notebook/sample.py(3)<module>()
-> import sys
(opdb) 
[INFO] [do_step] [lasti] 2
[INFO] [do_stack] [stack] [<code object f at 0x7f77015ec190, file "sample.py", line 1>]
[INFO] [disassemble_string] 2 LOAD_CONST 1 ('f') 
> /home/ctf/notebook/sample.py(5)<module>()
-> 
(opdb) 
[INFO] [do_step] [lasti] 4
[INFO] [do_stack] [stack] ['f', <code object f at 0x7f77015ec190, file "sample.py", line 1>]
[INFO] [disassemble_string] 4 MAKE_FUNCTION 0
> /home/ctf/notebook/sample.py(7)<module>()
(opdb) 
[INFO] [do_step] [lasti] 6
[INFO] [do_stack] [stack] [<function f at 0x7f7701bba1f0>]
[INFO] [disassemble_string] 6 STORE_NAME 0(f)
> /home/ctf/notebook/sample.py(9)<module>()
(opdb) 
[INFO] [do_step] [lasti] 8
[INFO] [do_stack] [stack] []
[INFO] [disassemble_string] 8 LOAD_CONST 2 (<code object main at 0x7f77015ec240, file "sample.py", line 1>) 
> /home/ctf/notebook/sample.py(11)<module>()
(opdb) 
[INFO] [do_step] [lasti] 10
[INFO] [do_stack] [stack] [<code object main at 0x7f77015ec240, file "sample.py", line 1>]
[INFO] [disassemble_string] 10 LOAD_CONST 3 ('main') 
> /home/ctf/notebook/sample.py(13)<module>()
...
(opdb) 
```

## trace

```
from opdb.tracer import trace
trace('sample.cpython-38.pyc')
```

OR 

```
$ python trace.py sample.cpython-38.pyc 
[INFO] [disassemble_string] 0 LOAD_CONST 0 (<code object f at 0x7f36cca59ea0, file "sample.py", line 1>) 
[INFO] [disassemble_string] 2 LOAD_CONST 1 ('f') 
[INFO] [disassemble_string] 4 MAKE_FUNCTION 0
[INFO] [disassemble_string] 6 STORE_NAME 0(f)
[INFO] [disassemble_string] 8 LOAD_CONST 2 (<code object main at 0x7f36cca60500, file "sample.py", line 1>) 
[INFO] [disassemble_string] 10 LOAD_CONST 3 ('main') 
[INFO] [disassemble_string] 12 MAKE_FUNCTION 0
[INFO] [disassemble_string] 14 STORE_NAME 1(main)
[INFO] [disassemble_string] 16 LOAD_NAME 2(__name__)
[INFO] [disassemble_string] 18 LOAD_CONST 4 ('__main__') 
[INFO] [disassemble_string] 20 COMPARE_OP 2(==)
...
```

## patch

Patch unreachable code to 'NOP' automatically.

```
from opdb.patcher import patch
patched = patch('sample.cpython-38.pyc')
decompile(patched)
```

OR

```
$ python patch.py sample.cpython-38.pyc 
1
patch: <code object <module> at 0x7fa6960c4df0, file "sample.py", line 1>
patch: <code object f at 0x7fa6964e9f50, file "sample.py", line 1>
patch: <code object main at 0x7fa6963ed920, file "sample.py", line 7>
patched_file: sample.cpython-38.pyc_patched.pyc
```