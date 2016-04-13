import os
from setuptools import setup, find_packages
 
setup(
    name = "module",
    version = "0.1",
    packages = find_packages(),
    package_data={'feature':['feature_generator_base.so','english_1st_fgen.so','english_2nd_fgen.so','feature_vector.so'],'parse':['ceisner3.so','ceisner.so'],'hvector':['_mycollections.so','mydouble.so']},
    include_package_data=True
    ) 
