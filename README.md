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
    
Before You Get Started
----------
If you are trying to use the config files under `src/config/`, now you have to specify the location of `glm-parser-data` by environment variable `NATLANG_DATA`. For example, if your `glm-parser-data` is here `~/data/glm-parser-data`:

    $ export NATLANG_DATA=~/data
    
If you are using Sequential Run or Spark Standalone mode to do the testing, all the file paths by default will be considered local paths. However, when using the Glm Parser in yarn mode, it will be from HDFS(Hadoop File System) by default, if you wish to use local directories, please add `file://` before the path. For example, for `/Data/A_Sample_Weight_Vector.db` in local directory will have to be `file:///Data/A_Sample_Weight_Vector.db`


Sequential run
----------

Here is a sample training run of the parser:

####Command Line:

    python glm_parser.py -i 5 -p ~/data/glm-parser-data/penn-wsj-deps/ --train="wsj_0[0-2][0-9][0-9].mrg.3.pa.gs.tab" --test="wsj_2[3-4][0-9][0-9].mrg.3.pa.gs.tab" -d `date "+%d-%m-%y"` -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --format=format/penn2malt.format config/default.config

In this example we are doing 5 iterations of training `-i 5` and using section 02 for training and testing on section 23 and section 24.
`-a` turns on time accounting.
`-d prefix` dumps the weight vector for each iteration as `prefix_Iter_i.db` for each iteration `i`.
The data for training is in the directory after `-p` and the data must be in the CoNLL format. The directory structure (if any) is the usual Penn Treebank directory structure. The format file parameter `--format` indicates the column structure of the CoNLL data.
The rest of the arguments load the actual filenames in `learn` and `feature` and `parser` respectively in order to configure the learning method, the feature generator and the parser which is used to find the argmax tree for each sentence.

####Using Config Files:

Format:

	$ python glm_parser.py CONFIG_FILE [options]

Example:

	$ python glm_parser.py config/default.config

Note that this will load the default settings from `config/default.config` which is almost identical to the command line commands above. Under default settings, `glm-parser-data` are stored at `~/data/glm-parser-data`. If your data is not stored under that folder, please add an option to specify the location:

	$ python glm_parser.py config/default.config -p YOUR_GLM_PARSER_DATA_LOCATION

Of course, you can also add other options here, for example iterations.

The training progress and the result on the testing section is saved to `glm_parser.log`

Parallel run
---------

The parallel run comes in two modes: spark standalone mode and spark yarn mode.

####Spark Standalone Mode
Please see `scripts/run_spark_linearb.sh` for example run. The command will need to use an additional option `-s NUMBER` or `--spark NUMBER`:

	$ spark-submit --driver-memory 4g --executor-memory 4g --master 'local[*]' glm_parser.py -s 4 config/default.config

####Spark Yarn Mode
When running on yarn mode, by default the glm_parser reads data, config, and format from HDFS(Hadoop file system). Reading these files from local directories will require the using of proper path, for example:

    file:///Users/jetic/Data/penn-wsj-deps

Please note that when running on yarn mode, environment variables could not be read in config files. Also, running the programme on yarn mode would require the `driver datanode` to possess access to the `glm-parser-data`, and the config file in local directories. Support for reading data directly from HDFS has not been implemented yet. Also, dumping weight vector for yarn mode has not been implemented either.

The difference with command line options is that you need to use a `--hadoop` option in addition to `--spark NUMBER`. This will tell the glm_parser to upload the data to HDFS instead of preparing it in a local directory.

######NOTE: Please do not use the same data for testing and training, HDFS doesn't support overwriting existing data by default.  

For the command of launching the glm_parser in yarn mode, please refer to `scripts/run_spark_hadoop.sh` for detail.

    $ python setup_module.py bdist_egg
	$ mv dist/module-0.1-py2.7.egg module.egg

	$ spark-submit --master yarn-cluster --num-executors 9 --driver-memory 7g --executor-memory 7g --executor-cores 3 --py-files module.egg glm_parser.py -s 8 -i 1 --hadoop config/default.config
	
Training with Part of Speech Tagger (POS Tagger)
----------------
You can use the same config file for the GLM Parser for training the POS Tagger, for example:

	$ python pos_tagger.py config/default.config
	
Additional options could be found by using `--help` option.

The POS Tagger now can only be run in sequential mode, parallel training with spark is still in development.
	
Using GLM Parser with Part of Speech Tagger
----------------
You can use our Part of Speech Tagger(POS Tagger) while running evaluations for the GLM Parser, but first you need to train the tagger, and retrieve a weight vector file dumped by the POS Tagger, then use `--tagger-w-vector` option to load it while executing `glm_parser.py`. For example:

	$ python glm_parser.py --tagger-w-vector config/default.config
	
Notice that a `tag_file` containing all the tags must also be specified, a sample one is providied in `src/tagset.txt`

Running Tests for SFU NatLang Lab
----------------

Please use configs to load the default setting for each language you are testing. After testing, use `scripts/proc_log.sh` to process the log file.

When submitting the log file, you must follow our format:

	Machine: MACHINE-NAME
	\n
	Branch: BRANCH-NAME
	\n
	Command:
	COMMAND_OR_SCRIPT_YOU_USED
	\n
	Result:
	COPY THE PROCESSED LOG CONTENTS HERE

Getting started on development
----------------

Read the file `getting-started.md` in the `docs` directory.


Contributing
------------

Before contributing to this project, please read `docs/development.md` which
explains the development model we use. TL;DR, it's a somewhat simplified git
flow model, using the regular git commit message convention, and `flake8` for
checking your code.
