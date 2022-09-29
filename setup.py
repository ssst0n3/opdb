from distutils.core import setup

setup(name='opdb',
      version='1.0',
      description='opcode level python debugger',
      packages=['opdb', 'opdb.lib'],
      dependency_links=['https://github.com/ssst0n3/opdb/releases/download/v0.0.1/pystack.tar.gz'],
)
