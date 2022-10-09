#!/usr/bin/env python

import sys
from opdb.patcher import patch

patched = patch(filename=sys.argv[1])
print("patched:", patched)
