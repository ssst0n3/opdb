import sys

import opdb
from util import load_code_object

filename = sys.argv[1]
code_object = load_code_object(filename)
opdb.run(code_object, dict(globals()), dict(locals()))
