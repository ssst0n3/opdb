import sys

from opdb import db
from opdb.util import load_code_object


def debug(filename):
    code_object = load_code_object(filename)
    db.run(code_object, dict(globals()), dict(locals()))


if __name__ == '__main__':
    debug(filename=sys.argv[1])
