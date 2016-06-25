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

Notice the config file is mandatory now. This issue has not been resolved yet.

####Using Config Files:



Format:

	$ python glm_parser.py CONFIG_FILE [options]

Example:

	$ python glm_parser.py config/default.config

Note that this will load the default settings from `config/default.config` which is almost identical to the command line commands above. Under default settings, `glm-parser-data` are stored at `~/data/glm-parser-data`. If your data is not stored under that folder, please add an option to specify the location:

	$ python glm_parser.py config/default.config -p YOUR_GLM_PARSER_DATA_LOCATION

Of course, you can also add other options here, for example iterations.

Note: if you are trying to use the config files under `src/config/`, now you have to specify the location of `glm-parser-data` by environment variable `NATLANG_DATA`. For example, if your `glm-parser-data` is here `~/data/glm-parser-data`:

    $ export NATLANG_DATA=~/data

The training progress and the result on the testing section is saved to `glm_parser.log`

Parallel run
---------

The parallel run comes in two modes: spark standalone mode and spark yarn mode.

####Spark Standalone Mode
Please see `scripts/run_spark_linearb.sh` for example run. The command will need to use an additional option `-s NUMBER` or `--spark NUMBER`:

	$ spark-submit --driver-memory 4g --executor-memory 4g --master 'local[*]' glm_parser.py -s 4 config/default.config
	
####Spark Yarn Mode
Please note that when running on yarn mode, environment variables could not be read in config files. Also, running the programme on yarn mode would require the `driver datanode` to possess access to the `glm-parser-data`, and the config file in local directories. Support for reading data directly from HDFS has not been implemented yet. Also, dumping weight vector for yarn mode has not been implemented either.

The difference with command line options is that you need to use a `--hadoop` option in addition to `--spark NUMBER`. This will tell the glm_parser to upload the data to HDFS instead of preparing it in a local directory. 

######NOTE: Please do not use the same data for testing and training, HDFS doesn't support overwriting existing data by default.  

For the command of launching the glm_parser in yarn mode, please refer to `scripts/run_spark_hadoop.sh` for detail.

    $ python setup_module.py bdist_egg
	$ mv dist/module-0.1-py2.7.egg module.egg

	$ spark-submit --master yarn-cluster --num-executors 9 --driver-memory 7g --executor-memory 7g --executor-cores 3 --py-files module.egg glm_parser.py -s 8 -i 1 --hadoop ~/Daten/glm-parser-config/default.config	

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

Before merging your branch
-----------------

Things to do before merging your branch to previous branch or master:

1. Check the performance on penn-wsj-deps dataset (use linearb or other school servers).
1. Check indentations using [tabnanny](https://pymotw.com/2/tabnanny)
