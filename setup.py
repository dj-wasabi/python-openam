# coding=utf-8

from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import codecs
import os
import sys
import re
import ast

here = os.path.abspath(os.path.dirname(__file__))


def get_info(filename):
    info = {}
    with open(filename) as _file:
        data = ast.parse(_file.read())
        for node in data.body:
            if type(node) != ast.Assign:
                continue
            if type(node.value) not in [ast.Str, ast.Num]:
                continue
            name = None
            for target in node.targets:
                name = target.id
            if type(node.value) == ast.Str:
                info[name] = node.value.s
            elif type(node.value) == ast.Num:
                info[name] = node.value.n
    return info

file_with_packageinfo = "openam/__init__.py"
info = get_info(file_with_packageinfo)

here = os.path.abspath(os.path.dirname(__file__))

requires = [
]


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--strict', '--verbose', '--tb=long', '--cov-report', 'term-missing', '--junitxml=docs/results.xml', '--cov=openam', 'tests']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(name='python-openam',
      version=info.get('__version__', '0.0.0'),
      description='Managing OpenAM via rest API',
      keywords='openam',
      url='http://python-openam.readthedocs.io/en/latest/',
      download_url='http://github.com/dj-wasabi/python-openam',
      author=info.get('__author__', ''),
      author_email=info.get('__email__', 'me@home.nl'),
      license=info.get('__license__', '0.0.0'),
      packages=['openam'],
      install_requires = [
            'requests',
            'pytest-cov',
      ],
      tests_require=['pytest'],
      cmdclass={'test': PyTest},
      platforms='any',
      test_suite='openam.tests.test_openam',
      extras_require={
        'testing': ['pytest'],
      },
      zip_safe=False,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
      ],
      )