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

Sample run
----------

Here is a sample training run of the parser:

    python glm_parser.py -i 5 -b 2 -e 2 -t 0 -p ~/data/glm-parser-data/penn-wsj-deps/ -d 05-11-2015 -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner

In this example we are doing 5 iterations of training `-i 5` and starting at section 02 for training `-b 2` and ending at section 02 `-e 2`. 
We are testing on section 0 using `-t 0`. 
`-a` turns on time accounting.
`-d prefix` dumps the weight vector for each iteration as `prefix_Iter_i.db` for each iteration `i`.
The data for training is in the directory after `-p`. It assumes the usual Penn Treebank directory structure.
The rest of the arguments load the actual filenames in `learn` and `feature` and `parser` respectively in order to configure the learning method, the feature generator and the parser which is used to find the argmax tree for each sentence.

The training progress and the result on the testing section is saved to `glm_parser.log`

Spark run
---------

    spark-submit glm_parser.py -i 2 -b 1 -e 4 -t 0 -p /cs/natlang-projects/glm-parser/penn-wsj-deps/ --learner=spark_perceptron --fgen=english_1st_fgen --parser=ceisner

