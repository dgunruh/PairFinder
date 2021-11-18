#!/usr/bin/env python
"""
setup.py: Pair finder setup
"""
from setuptools import setup, find_packages

__author__ = "Chaitanya Kolluru, Davis Unruh, Luqing Wang, " +\
    "Samantha Tetef, Yiming Chen"
__version__ = "0.1.0"

setup(
    name='pairfinder',
    version=__version__,
    url='https://github.com/dgunruh/PairFinder',
    author=__author__,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Operating System :: OS Independant',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering'
    ],
    description='Algorithm for pairing up N particles in D dimensional ' +
                'space that minimizes overall distance between pairs.',
    keywords=[
        'Particle physics',
        'Computational physics'
    ],
    packages=find_packages(exclude="test"),
    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.19.1',
        'pandas>=1.2.0',
        'scipy>=1.6.0'
    ]
)
