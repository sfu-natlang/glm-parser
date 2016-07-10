import os
from setuptools import setup, find_packages

setup(
    name = "module",
    version = "0.1",
    packages = find_packages(),
    package_data={'': ['*.so', '*.format']},
    py_modules=['pos_tagger'],
    include_package_data=True)
