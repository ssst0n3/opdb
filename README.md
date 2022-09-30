# opdb

opcode level debugger for python

## install 

* pip install https://github.com/ssst0n3/opdb/releases/download/v0.0.3/pystack.tar.gz
* pip install https://github.com/ssst0n3/opdb/releases/download/v0.0.3/opdb.tar.gz

## debug

```
python debug.py xxx.pyc
```

OR

```
from opdb.debug import debug
debug.debug('xxx.pyc')
```

## trace

```
python trace.py xxx.pyc
```

OR

```
from opdb.trace import trace
trace.trace('xxx.pyc')
```

## patch

Patch unreachable code to 'NOP' automatically.

```
python patch.py xxx.pyc
```

OR

```
from opdb.patch import patch
patched = patch('xxx.pyc')
decompile(patched)
```