from distutils.core import setup, Extension

module1 = Extension('pystack', sources=['pystack3.cpp'])

setup(name='pystack',
      version='1.0',
      description='pystack',
      ext_modules=[module1])
