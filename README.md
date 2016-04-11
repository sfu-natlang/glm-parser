glm-parser
==========

This project implements a parser for natural language that uses a general linear model over higher-order dependencies between words. It works on any language that is in the CoNLL format. 

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

