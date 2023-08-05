# -*- coding: utf-8 -*-
from setuptools import setup

__author__ = 'Martin Uhrin'
__license__ = 'LGPLv3'

about = {}
with open('atomsgraph/version.py') as f:
    exec(f.read(), about)  # pylint: disable=exec-used

setup(
    name='milad',
    version=about['__version__'],
    description='Python library for interacting with an atoms graph',
    long_description=open('README.rst').read(),
    url='https://github.com/muhrin/atomsgraph.git',
    author='Martin Uhrin',
    author_email='martin.uhrin.10@ucl.ac.uk',
    license=__license__,
    classifiers=[
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='machine learning, atomic descriptor, moment invariants',
    python_requires='>=3.6',
    install_requires=[
        'gremlinpython'
    ],
    extras_require={
        'dev': [
            'ipython',
            'pip',
            'pytest~=5.4',
            'pytest-cov',
            'pre-commit~=2.2',
            'prospector',
            'pylint==2.5.2',
            'twine',
            'yapf',
        ],
    },
    packages=[
        'atomsgraph'
    ],
    include_package_data=True,
    test_suite='test',
)
