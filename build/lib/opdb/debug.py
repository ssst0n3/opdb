import sys

from opdb import db
from opdb.util import load_code_object

filename = sys.argv[1]
code_object = load_code_object(filename)
db.run(code_object, dict(globals()), dict(locals()))
