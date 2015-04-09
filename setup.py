# -*- coding: utf-8 -*-
"""
setup.py
========

"""

from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys


class Tox(TestCommand):
    """ Tox """

    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        import shlex
        if self.tox_args:
            errno = tox.cmdline(args=shlex.split(self.tox_args))
        else:
            errno = tox.cmdline(self.tox_args)
        sys.exit(errno)


classifiers = [
    "Development Status :: 3 - Alpha",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: System :: Networking",
    "Topic :: System :: Networking :: Monitoring",
]

requires = ['sphinx']

with open('requirements.txt', 'w') as _file:
    _file.write('\n'.join(requires))

setup(
    name="rancidcmd",
    version="0.1.0",
    description='Rancid Command Wrapper Tool',
    long_description='',
    author='mtoshi',
    author_email='mtoshi.g@gmail.com',
    url='https://github.com/mtoshi/rancidcmd',
    license='MIT',
    classifiers=classifiers,
    packages=['rancidcmd'],
    data_files=[],
    install_requires=requires,
    include_package_data=True,
    tests_require=['tox'],
    cmdclass={'test': Tox},
)
