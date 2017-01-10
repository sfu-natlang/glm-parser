# -*- coding: utf-8 -*-
"""
Created on Wed Mar 05 17:35:29 2014

@author: Yulan
"""
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

extentions = [
    Extension('parser.ceisner', ["parser/ceisner.pyx"]),
    Extension('parser.ceisner3', ["parser/ceisner3.pyx"]),
    Extension('feature.feature_generator_base', ["feature/feature_generator_base.pyx"]),
    Extension('feature.english_1st_fgen', ["feature/english_1st_fgen.pyx"]),
    Extension('feature.english_2nd_fgen', ["feature/english_2nd_fgen.pyx"]),
    Extension('feature.feature_vector', ["feature/feature_vector.pyx"]),
]

setup(
    ext_modules=cythonize(extentions),
)
