#! /bin/csh -f

#source $MODULESHOME/init/bash
module load natlang
module load NL/LANG/PYTHON/Anaconda-2.3.0
module load NL/HADOOP/SPARK/1.2.1
cd ../src/

echo "Compile Cython classes ..."
#export PYTHONPATH=$PYTHONPATH:/cs/natlang-projects/glm-parser/Cython-0.20.1
python setup.py build_ext --inplace


echo "Compile hvector ..."
cd hvector
python setup.py install --install-lib .
cd ..

