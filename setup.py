import sys
from setuptools import setup, Extension

if sys.version_info < (3,):
    module = Extension('pystack', sources=['pystack/pystack2.cpp'])
else:
    module = Extension('pystack', sources=['pystack/pystack3.cpp'])

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name='opdb',
    version='0.1.1',
    description='opcode level python debugger',
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=['opdb', 'opdb.lib'],
    ext_modules=[module],
    include_package_data=True,
    author='ssst0n3',
    author_email='ssst0n3@gmail.com',
    url='https://github.com/ssst0n3/opdb',
    download_url='https://github.com/ssst0n3/opdb/releases/download/v0.1/opdb-0.1.tar.gz',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
