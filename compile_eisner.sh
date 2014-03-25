#!/bin/bash
#!/usr/bin/env python2.7
export PYTHONPATH=$PYTHONPATH:/cs/natlang-projects/glm-parser/Cython-0.20.1

python setup.py build_ext --inplace
