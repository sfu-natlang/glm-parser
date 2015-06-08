glm-parser
==========

This project implements a parser for natural language that uses a general linear model over higher-order dependencies between words. Training the model is done using a (margin-aware) Perceptron algorithm. The dependencies between words are created using tree-adjoining grammar derivations where each word lexicalizes an elementary tree and a full sentence parse is the combination of these elementary trees. Search is done using the Eisner dependency parsing algorithm augmented with search over higher-order dependencies. The parser uses Penn Treebank style trees for training data.

Part of the system replicates the following paper:

Xavier Carreras, Michael Collins, and Terry Koo. TAG, Dynamic Programming and the Perceptron for Efficient, Feature-rich Parsing. In Proceedings of CONLL 2008. http://www.cs.columbia.edu/~mcollins/papers/conll.final.pdf

Get started
-----------

Install a version of Python 2.x that includes Cython such as the anaconda Python distribution (or install Python 2.x and then Cython).

Set up the Cython libraries and classes:

    cd src
    echo "Compile Cython classes ..."
    python setup.py build_ext --inplace


    echo "Compile hvector ..."
    cd hvector
    python setup.py install --install-lib .
    cd ../..

Or if you are on a RCG machine such as `linux.cs.sfu.ca` or `queen.rcg.sfu.ca` then do:

    sh scripts/setup_env.sh
