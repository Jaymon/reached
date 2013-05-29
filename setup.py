#!/usr/bin/env python
# I shamefully ripped most of this off from fbconsole
# http://docs.python.org/distutils/setupscript.html
# http://docs.python.org/2/distutils/examples.html

import sys
import os
from setuptools import setup
import ast

version = ''
with open(os.path.join('reached', '__init__.py'), 'rU') as f:
    for node in (n for n in ast.parse(f.read()).body if isinstance(n, ast.Assign)):
        name = node.targets[0]
        if isinstance(name, ast.Name) and name.id.startswith('__version__'):
            version = node.value.s
            break

if not version:
    raise RuntimeError('Unable to find version number')

setup(
    name='reached',
    version=version,
    description='command line search and replace',
    author='Jay Marcyes',
    author_email='jay@marcyes.com',
    url='http://github.com/Jaymon/reached',
    packages=['reached'],
    license="MIT",
    classifiers=[
        'Development Status :: {}'.format(version),
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: MIT',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
    ],
    #test_suite = "test_pout",
    entry_points = {
        'console_scripts': ['reached = reached:console']
    }
)
