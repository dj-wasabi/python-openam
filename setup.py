# coding=utf-8

from __future__ import print_function
from setuptools.command.test import test as TestCommand
from distutils.core import setup, Command
import subprocess
import os
import sys
import ast

here = os.path.abspath(os.path.dirname(__file__))

with open('README.rst') as file:
    long_description = file.read()


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


class Pep(Command):
    description = "Running pep commands to verify standards"
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        list_of_peps = ['pep8', 'pep257']
        for pep in list_of_peps:
            command = [pep + " openam"]
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            proc.wait()

            if proc.returncode != 0:
                print(proc.stdout.read())


class Coverage(Command):
    description = "Creating the coverage svg file."
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        command = ["coverage-badge -o coverage.svg"]
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        proc.wait()


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
      long_description=long_description,
      install_requires = [
        'requests'
      ],
      tests_require=['pytest'],
      cmdclass={
          'test': PyTest,
          'pep': Pep,
          'cov': Coverage
      },
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
