#!/usr/bin/env python

import sys
from opdb.patch import patch

patched = patch(filename=sys.argv[1])
print("patched:", patched)
