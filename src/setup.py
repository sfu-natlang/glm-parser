# -*- coding: utf-8 -*-
"""
Created on Wed Mar 05 17:35:29 2014

@author: Yulan

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

extentions = [
    Extension('parse.ceisner',["parse/ceisner.pyx"]),
    Extension('parse.ceisner3',["parse/ceisner3.pyx"]),
    Extension('feature.feature_generator_base', ["feature/feature_generator_base.pyx"]),
    Extension('feature.english_1st_fgen', ["feature/english_1st_fgen.pyx"]),
    Extension('feature.english_2nd_fgen', ["feature/english_2nd_fgen.pyx"]),
    Extension('feature.feature_vector', ["feature/feature_vector.pyx"]),
]

setup(
    ext_modules=cythonize(extentions),
)
'"""

 
from setuptools import setup, find_packages
 
setup(
    name = "glm",
    version = "0.1",
    packages = find_packages(),
    package_data={'': ['__main__.py','glm_parser.py'],'feature':['feature_generator_base.so','english_1st_fgen.so','english_2nd_fgen.so','feature_vector.so'],'parse':['ceisner3.so','ceisner.so'],'hvector':['_mycollections.so','mydouble.so']},
    include_package_data=True
    )