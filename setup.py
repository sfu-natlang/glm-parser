# -*- coding: utf-8 -*-
"""
Created on Wed Mar 05 17:35:29 2014

@author: Yulan
"""

from distutils.core import setup
from Cython.Build import cythonize

setup(
    name = 'ceisner',
    ext_modules = cythonize("*.pyx"),
)