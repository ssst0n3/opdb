from distutils.core import setup

setup(name='opdb',
      version='1.0',
      description='opcode level python debugger',
      packages=['opdb', 'opdb.lib'],
      dependency_links=['http://github.com/user/repo/tarball/master#egg=package-1.0'],
)
