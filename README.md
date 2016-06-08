glm-parser
==========

Installation
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

Old:

    python glm_parser.py -i 5 -b 2 -e 2 -t 0 -p ~/data/glm-parser-data/penn-wsj-deps/ -d 05-11-2015 -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner

New:

    python glm_parser.py -i 5 -p ~/data/glm-parser-data/penn-wsj-deps/ --train="wsj_0[0-2][0-9][0-9].mrg.3.pa.gs.tab" --test="wsj_2[3-4][0-9][0-9].mrg.3.pa.gs.tab" -d `date "+%d-%m-%y"` -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --format=format/penn2malt.format

In this example we are doing 5 iterations of training `-i 5` and using section 02 for training and testing on section 23 and section 24. 
`-a` turns on time accounting.
`-d prefix` dumps the weight vector for each iteration as `prefix_Iter_i.db` for each iteration `i`.
The data for training is in the directory after `-p` and the data must be in the CoNLL format. The directory structure (if any) is the usual Penn Treebank directory structure. The format file parameter `--format` indicates the column structure of the CoNLL data.
The rest of the arguments load the actual filenames in `learn` and `feature` and `parser` respectively in order to configure the learning method, the feature generator and the parser which is used to find the argmax tree for each sentence.

The training progress and the result on the testing section is saved to `glm_parser.log`

Spark run
---------

    spark-submit glm_parser.py -i 2 -b 1 -e 4 -t 0 -p /cs/natlang-projects/glm-parser/penn-wsj-deps/ --learner=spark_perceptron --fgen=english_1st_fgen --parser=ceisner

Getting started on development
----------------

Read the file `getting-started.md` in the `docs` directory.

Before merging your branch
-----------------

Things to do before merging your branch to previous branch or master:

1. Check the performance on penn-wsj-deps dataset (use linearb or other school servers).
1. Check indentations using [tabnanny](https://pymotw.com/2/tabnanny)

