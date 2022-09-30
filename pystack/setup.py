import sys
from distutils.core import setup, Extension

if sys.version_info < (3,):
    module = Extension('pystack', sources=['pystack2.cpp'])
else:
    module = Extension('pystack', sources=['pystack3.cpp'])

setup(
    name='pystack',
    version='0.1',
    description='pystack',
    ext_modules=[module],
    author='ssst0n3',
    author_email='ssst0n3@gmail.com',
    url='https://github.com/ssst0n3/opdb',
    download_url='https://github.com/ssst0n3/opdb/releases/download/v0.1/pystack-0.1.tar.gz',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
