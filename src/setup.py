# -*- coding: utf-8 -*-
"""
Created on Wed Mar 05 17:35:29 2014

@author: Yulan
"""

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

extentions = [
    Extension('ceisner',["ceisner.pyx"])
]

setup(
    ext_modules=cythonize(extentions),
)

