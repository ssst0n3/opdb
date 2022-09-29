import sys
from distutils.core import setup, Extension

if sys.version_info < (3,):
    module = Extension('pystack', sources=['pystack2.cpp'])
else:
    module = Extension('pystack', sources=['pystack3.cpp'])

setup(name='pystack',
      version='1.0',
      description='pystack',
      ext_modules=[module])
