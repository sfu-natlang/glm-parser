#!/bin/bash

# Use before setup_env.sh is run to make sure environment is ready

echo "Cleaning up directories..."

rm ../docs/*.log
rm ../docs/*.aux
rm ../docs/*.pdf
rm ../src/*.log
rm ../src/feature/english_1st_fgen.c
rm ../src/feature/english_2nd_fgen.c
rm ../src/feature/feature_generator_base.c
rm ../src/feature/feature_vector.c
rm ../src/parse/ceisner.cpp
rm ../src/parse/ceisner3.cpp
rm ../src/*.db

rm -r ../src/build/*
rm -r ../src/hvector/build/*
