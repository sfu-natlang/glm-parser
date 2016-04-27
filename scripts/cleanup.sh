#!/bin/bash

# Use before setup_env.sh is run to make sure environment is ready

echo "Cleaning up directories..."

rm -f ../docs/*.log
rm -f ../docs/*.aux
rm -f ../docs/*.pdf
rm -f ../src/*.log
rm -f ../src/feature/english_1st_fgen.c
rm -f ../src/feature/english_2nd_fgen.c
rm -f ../src/feature/feature_generator_base.c
rm -f ../src/feature/feature_vector.c
rm -f ../src/parse/ceisner.cpp
rm -f ../src/parse/ceisner3.cpp
rm -f ../src/*.db

rm -r ../src/build/*
rm -r ../src/hvector/build/*
