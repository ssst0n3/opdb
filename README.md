# opdb

opcode level debugger for python

## install 

* pip install https://github.com/ssst0n3/opdb/releases/download/v0.0.3/pystack.tar.gz
* pip install https://github.com/ssst0n3/opdb/releases/download/v0.0.3/opdb.tar.gz

## debug

```
from opdb.debug import debug
debug.debug('sample.cpython-38.pyc')
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
(opdb) 
[INFO] [do_step] [lasti] 12
[INFO] [do_stack] [stack] ['main', <code object main at 0x7f77015ec240, file "sample.py", line 1>]
[INFO] [disassemble_string] 12 MAKE_FUNCTION 0
> /home/ctf/notebook/sample.py(15)<module>()
(opdb) 
[INFO] [do_step] [lasti] 14
[INFO] [do_stack] [stack] [<function main at 0x7f7701d22280>]
[INFO] [disassemble_string] 14 STORE_NAME 1(main)
> /home/ctf/notebook/sample.py(17)<module>()
(opdb) 
[INFO] [do_step] [lasti] 16
[INFO] [do_stack] [stack] []
[INFO] [disassemble_string] 16 LOAD_NAME 2(__name__)
> /home/ctf/notebook/sample.py(19)<module>()
(opdb) 
[INFO] [do_step] [lasti] 18
[INFO] [do_stack] [stack] ['__main__']
[INFO] [disassemble_string] 18 LOAD_CONST 4 ('__main__') 
> /home/ctf/notebook/sample.py(21)<module>()
(opdb) 
[INFO] [do_step] [lasti] 20
[INFO] [do_stack] [stack] ['__main__', '__main__']
[INFO] [disassemble_string] 20 COMPARE_OP 2(==)
> /home/ctf/notebook/sample.py(23)<module>()
(opdb) 
[INFO] [do_step] [lasti] 22
[INFO] [do_stack] [stack] [True]
[INFO] [disassemble_string] 22 POP_JUMP_IF_FALSE 30
> /home/ctf/notebook/sample.py(25)<module>()
(opdb) 
[INFO] [do_step] [lasti] 24
[INFO] [do_stack] [stack] []
[INFO] [disassemble_string] 24 LOAD_NAME 1(main)
> /home/ctf/notebook/sample.py(27)<module>()
(opdb) 
[INFO] [do_step] [lasti] 26
[INFO] [do_stack] [stack] [<function main at 0x7f7701d22280>]
[INFO] [disassemble_string] 26 CALL_FUNCTION 0
--Call--
> /home/ctf/notebook/sample.py(1)main()
-> #!/usr/bin/env python
(opdb) 
[INFO] [do_step] [lasti] -1
[INFO] [do_stack] [stack] []
> /home/ctf/notebook/sample.py(1)main()
-> #!/usr/bin/env python
(opdb) 
[INFO] [do_step] [lasti] 0
[INFO] [do_stack] [stack] []
[INFO] [disassemble_string] 0 LOAD_GLOBAL 0(f)
> /home/ctf/notebook/sample.py(3)main()
-> import sys
(opdb) 
[INFO] [do_step] [lasti] 2
[INFO] [do_stack] [stack] [<function f at 0x7f7701bba1f0>]
[INFO] [disassemble_string] 2 CALL_FUNCTION 0
--Call--
> /home/ctf/notebook/sample.py(1)f()
-> #!/usr/bin/env python
(opdb) 
[INFO] [do_step] [lasti] -1
[INFO] [do_stack] [stack] []
> /home/ctf/notebook/sample.py(1)f()
-> #!/usr/bin/env python
(opdb) 
[INFO] [do_step] [lasti] 0
[INFO] [do_stack] [stack] []
[INFO] [disassemble_string] 0 LOAD_CONST 1 ((1, 0)) 
> /home/ctf/notebook/sample.py(3)f()
-> import sys
(opdb) 
[INFO] [do_step] [lasti] 2
[INFO] [do_stack] [stack] [(1, 0)]
[INFO] [disassemble_string] 2 UNPACK_SEQUENCE 2
> /home/ctf/notebook/sample.py(5)f()
-> 
(opdb) 
[INFO] [do_step] [lasti] 4
[INFO] [do_stack] [stack] [1, 0]
[INFO] [disassemble_string] 4 STORE_FAST 0(a)
> /home/ctf/notebook/sample.py(7)f()
(opdb) 
[INFO] [do_step] [lasti] 6
[INFO] [do_stack] [stack] [0]
[INFO] [disassemble_string] 6 STORE_FAST 1(b)
> /home/ctf/notebook/sample.py(9)f()
(opdb) 
[INFO] [do_step] [lasti] 8
[INFO] [do_stack] [stack] []
[INFO] [disassemble_string] 8 LOAD_FAST 0(a)
> /home/ctf/notebook/sample.py(11)f()
(opdb) 
[INFO] [do_step] [lasti] 10
[INFO] [do_stack] [stack] [1]
[INFO] [disassemble_string] 10 POP_JUMP_IF_TRUE 16
> /home/ctf/notebook/sample.py(17)f()
(opdb) 
[INFO] [do_step] [lasti] 16
[INFO] [do_stack] [stack] []
[INFO] [disassemble_string] 16 LOAD_FAST 0(a)
> /home/ctf/notebook/sample.py(19)f()
(opdb) 
[INFO] [do_step] [lasti] 18
[INFO] [do_stack] [stack] [1]
[INFO] [disassemble_string] 18 RETURN_VALUE None
--Return--
> /home/ctf/notebook/sample.py(19)f()->1
(opdb) 
[INFO] [do_step] [lasti] 18
[INFO] [do_stack] return so do not read stack
[INFO] [disassemble_string] 18 RETURN_VALUE None
> /home/ctf/notebook/sample.py(5)main()
-> 
(opdb) 
[INFO] [do_step] [lasti] 4
[INFO] [do_stack] [stack] [1]
[INFO] [disassemble_string] 4 STORE_FAST 0(res)
> /home/ctf/notebook/sample.py(7)main()
(opdb) 
[INFO] [do_step] [lasti] 6
[INFO] [do_stack] [stack] []
[INFO] [disassemble_string] 6 LOAD_GLOBAL 1(print)
> /home/ctf/notebook/sample.py(9)main()
(opdb) 
[INFO] [do_step] [lasti] 8
[INFO] [do_stack] [stack] [<built-in function print>]
[INFO] [disassemble_string] 8 LOAD_FAST 0(res)
> /home/ctf/notebook/sample.py(11)main()
(opdb) 
[INFO] [do_step] [lasti] 10
[INFO] [do_stack] [stack] [1, <built-in function print>]
[INFO] [disassemble_string] 10 CALL_FUNCTION 1
1
> /home/ctf/notebook/sample.py(13)main()
(opdb) 
[INFO] [do_step] [lasti] 12
[INFO] [do_stack] [stack] [None]
[INFO] [disassemble_string] 12 POP_TOP None
> /home/ctf/notebook/sample.py(15)main()
(opdb) 
[INFO] [do_step] [lasti] 14
[INFO] [do_stack] [stack] []
[INFO] [disassemble_string] 14 LOAD_CONST 0 (None) 
> /home/ctf/notebook/sample.py(17)main()
(opdb) 
[INFO] [do_step] [lasti] 16
[INFO] [do_stack] [stack] [None]
[INFO] [disassemble_string] 16 RETURN_VALUE None
--Return--
> /home/ctf/notebook/sample.py(17)main()->None
(opdb) 
[INFO] [do_step] [lasti] 16
[INFO] [do_stack] return so do not read stack
[INFO] [disassemble_string] 16 RETURN_VALUE None
> /home/ctf/notebook/sample.py(29)<module>()
(opdb) 
[INFO] [do_step] [lasti] 28
[INFO] [do_stack] [stack] [None]
[INFO] [disassemble_string] 28 POP_TOP None
> /home/ctf/notebook/sample.py(31)<module>()
(opdb) 
[INFO] [do_step] [lasti] 30
[INFO] [do_stack] [stack] []
[INFO] [disassemble_string] 30 LOAD_CONST 5 (None) 
> /home/ctf/notebook/sample.py(33)<module>()
(opdb) 
[INFO] [do_step] [lasti] 32
[INFO] [do_stack] [stack] [None]
[INFO] [disassemble_string] 32 RETURN_VALUE None
--Return--
> /home/ctf/notebook/sample.py(33)<module>()->None
(opdb) 
[INFO] [do_step] [lasti] 32
[INFO] [do_stack] return so do not read stack
[INFO] [disassemble_string] 32 RETURN_VALUE None
> /usr/local/lib/python3.8/bdb.py(584)run()
-> self.quitting = True
(opdb) 
```

## trace

```
from opdb.trace import trace
trace.trace('sample.cpython-38.pyc')
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
[INFO] [disassemble_string] 22 POP_JUMP_IF_FALSE 30
[INFO] [disassemble_string] 24 LOAD_NAME 1(main)
[INFO] [disassemble_string] 26 CALL_FUNCTION 0
[INFO] [disassemble_string] 0 LOAD_GLOBAL 0(f)
[INFO] [disassemble_string] 2 CALL_FUNCTION 0
[INFO] [disassemble_string] 0 LOAD_CONST 1 ((1, 0)) 
[INFO] [disassemble_string] 2 UNPACK_SEQUENCE 2
[INFO] [disassemble_string] 4 STORE_FAST 0(a)
[INFO] [disassemble_string] 6 STORE_FAST 1(b)
[INFO] [disassemble_string] 8 LOAD_FAST 0(a)
[INFO] [disassemble_string] 10 POP_JUMP_IF_TRUE 16
[INFO] [disassemble_string] 16 LOAD_FAST 0(a)
[INFO] [disassemble_string] 18 RETURN_VALUE None
[INFO] [disassemble_string] 18 RETURN_VALUE None
[INFO] [disassemble_string] 4 STORE_FAST 0(res)
[INFO] [disassemble_string] 6 LOAD_GLOBAL 1(print)
[INFO] [disassemble_string] 8 LOAD_FAST 0(res)
[INFO] [disassemble_string] 10 CALL_FUNCTION 1
1
[INFO] [disassemble_string] 12 POP_TOP None
[INFO] [disassemble_string] 14 LOAD_CONST 0 (None) 
[INFO] [disassemble_string] 16 RETURN_VALUE None
[INFO] [disassemble_string] 16 RETURN_VALUE None
[INFO] [disassemble_string] 28 POP_TOP None
[INFO] [disassemble_string] 30 LOAD_CONST 5 (None) 
[INFO] [disassemble_string] 32 RETURN_VALUE None
[INFO] [disassemble_string] 32 RETURN_VALUE None
```

## patch

Patch unreachable code to 'NOP' automatically.

```
from opdb.patch import patch
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