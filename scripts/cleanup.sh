#!/bin/bash

# Use before setup_env.sh is run to make sure environment is ready

cd "$( dirname "$0" )"

echo "Cleaning up directories..."

rm -f ../docs/*.log
rm -f ../docs/*.aux
rm -f ../docs/*.pdf
rm -f ../src/*.log
rm -f ../src/*.log.bak
rm -f ../src/feature/english_1st_fgen.c
rm -f ../src/feature/english_2nd_fgen.c
rm -f ../src/feature/feature_generator_base.c
rm -f ../src/feature/feature_vector.c
rm -f ../src/parser/ceisner.cpp
rm -f ../src/parser/ceisner3.cpp
rm -f ../src/*.db

rm -r ../src/build
rm -r ../src/hvector/build

rm -f ../src/*/*.pyc
rm -f ../src/*.pyc
rm -f ../src/*.pyv
rm -f ../src/hvector/*.egg-info
rm -f ../src/*/*.so
rm -r ../src/data/prep
rm -f ../src/*.egg
rm -r ../src/*.egg-info
rm -r ../src/dist
