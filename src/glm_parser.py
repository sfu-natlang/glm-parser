# -*- coding: utf-8 -*-

#
# Global Linear Model Parser
# Simon Fraser University
# NLP Lab
#
# Author: Yulan Huang, Ziqi Wang, Anoop Sarkar, Jetic Gu, Kingston Chen,
#         Andrei Vacariu
# (Please add on your name if you have authored this file)
#
import debug.debug
from data.file_io import fileRead, fileWrite
from data.data_pool import DataPool
from evaluate.evaluator import Evaluator
from weight.weight_vector import WeightVector
from pos_tagger import PosTagger
from logger.loggers import logging, init_logger

import time
import os
import sys
import importlib
import functools
from functools import partial
import argparse
import StringIO
from ConfigParser import SafeConfigParser

__version__ = '1.0'
if __name__ == "__main__":
    init_logger('glm_parser.log')
logger = logging.getLogger('PARSER')


class GlmParser():
    def __init__(self,
                 weightVectorLoadPath = None,
                 learner              = None,
                 parser               = None,
                 parallelFlag         = False,
                 sparkContext         = None):

        logger.info("Initialising Parser")
        if learner is None:
            raise ValueError("PARSER [ERROR]: Learner not specified")
        self.w_vector     = WeightVector(weightVectorLoadPath, sparkContext)
        self.evaluator    = Evaluator()

        if parallelFlag:
            self.learner = importlib.import_module('learn.' + learner).Learner()
        else:
            self.learner = importlib.import_module('learn.' + learner).Learner(self.w_vector)
        logger.info("Using learner: %s " % (self.learner.name))

        self.parser = importlib.import_module('parse.' + parser).EisnerParser()
        logger.info("Using parser: %s" % (parser))

        logger.info("Initialisation Complete")
        return

    def train(self,
              dataPool             = None,
              maxIteration         = None,
              weightVectorDumpPath = None,
              dumpFrequency        = 1,
              parallel             = False,
              shardNum             = None,
              sc                   = None,
              hadoop               = False):
        # Check values
        if not isinstance(dataPool, DataPool):
            raise ValueError("PARSER [ERROR]: dataPool for training is not an DataPool object")
        if maxIteration is None:
            logger.warn("Number of Iterations not specified, using 1")
            maxIteration = 1

        # Prepare the suitable argmax
        def parser_f_argmax(w_vector, sentence, parser):
            current_edge_set = parser.parse(sentence, w_vector.get_vector_score)
            current_global_vector = sentence.set_current_global_vector(current_edge_set)
            return current_global_vector
        f_argmax = functools.partial(parser_f_argmax, parser=self.parser)

        # Star Training Process
        logger.info("Starting Training Process")
        start_time = time.time()
        if not parallel:  # using sequential training
            logger.info("Using Sequential Training")
            self.w_vector = self.learner.sequential_learn(
                max_iter   = maxIteration,
                data_pool  = dataPool,
                f_argmax   = f_argmax,
                d_filename = weightVectorDumpPath,
                dump_freq  = dumpFrequency)
        else:  # using parallel training
            logger.info("Using Parallel Training")
            if shardNum is None:
                logger.warn("Number of shards not specified, using 1")
                shardNum = 1
            if sc is None:
                raise RuntimeError('PARSER [ERROR]: SparkContext not specified')

            parallelLearnClass = importlib.import_module('learn.spark_train').ParallelPerceptronLearner
            learner = parallelLearnClass(self.w_vector, maxIteration)
            self.w_vector = learner.parallel_learn(
                max_iter     = maxIteration,
                dataPool     = dataPool,
                f_argmax     = f_argmax,
                learner      = self.learner,
                d_filename   = weightVectorDumpPath,
                shards       = shardNum,
                sc           = sc,
                hadoop       = hadoop)

        end_time = time.time()
        logger.info("Total Training Time(seconds): %f" % (end_time - start_time,))
        return

    def evaluate(self, dataPool=None, tagger=None, sc=None, hadoop=None):
        logger.info("Starting evaluation process")
        start_time = time.time()
        if not isinstance(dataPool, DataPool):
            raise ValueError("PARSER [ERROR]: dataPool for evaluation is not an DataPool object")
        self.evaluator.evaluate(data_pool = dataPool,
                                parser    = self.parser,
                                w_vector  = self.w_vector,
                                tagger    = tagger,
                                sc        = sc,
                                hadoop    = hadoop)
        end_time = time.time()
        logger.info("Total evaluation Time(seconds): %f" % (end_time - start_time,))

if __name__ == "__main__":
    __logger = logging.getLogger('MAIN')
    # Default values
    config = {
        'train':             None,
        'test':              None,
        'iterations':        1,
        'data_path':         None,
        'load_weight_from':  None,
        'dump_weight_to':    None,
        'dump_frequency':    1,
        'spark_shards':      1,
        'prep_path':         'data/prep',
        'learner':           'average_perceptron',
        'parser':            'ceisner',
        'feature_generator': 'english_1st_fgen',
        'format':            'format/penn2malt.format',
        'tagger_w_vector':   None,
        'tag_file':          None
    }

    glm_parser = GlmParser

    # Dealing with arguments here
    if True:  # Adding arguments
        arg_parser = argparse.ArgumentParser(description="""Global Linear Model (GLM) Parser
            Version %s""" % __version__)
        arg_parser.add_argument('config', metavar='CONFIG_FILE', nargs='?',
            help="""specify the config file. This will load all the setting from the config file,
            in order to avoid massive command line inputs. Please consider using config files
            instead of manually typing all the options.

            Additional options by command line will override the settings in the config file.

            Officially provided config files are located in src/config/
            """)
        arg_parser.add_argument('--train', metavar='TRAIN_FILE_PATTERN',
            help="""specify the data for training with regular expression
            """)
        arg_parser.add_argument('--test', metavar='TEST_FILE_PATTERN',
            help="""specify the data for testing with regular expression
            """)
        arg_parser.add_argument('--feature-generator',
            choices=['english_1st_fgen', 'english_2nd_fgen'],
            help="""specify feature generation facility by a python file name (mandatory).
            The file will be searched under /feature directory, and the class
            object that has a get_local_vector() interface will be recognised
            as the feature generator and put into use automatically.

            If multiple eligible objects exist, an error will be reported.

            For developers: please make sure there is only one such class object
            under fgen source files. Even import statement may introduce other
            modules that is eligible to be an fgen. Be careful.

            default "english_1nd_fgen"; alternative "english_2nd_fgen"
            """)
        arg_parser.add_argument('--learner',
            choices=['average_perceptron', 'perceptron'],
            help="""specify a learner for weight vector training
            default "average_perceptron"; alternative "perceptron"
            """)
        arg_parser.add_argument('--parser',
            choices=['ceisner', 'ceisner3'],
            help="""specify the parser using parser module name (i.e. .py file name without suffix).
            The recognition rule is the same as --fgen switch. A valid parser object
            must possess "parse" attribute in order to be recognised as a parser
            implementation.

            Some parser might not work correctly with the infrastructure, which keeps
            changing all the time. If this happens please file an issue on github page

            default "ceisner"; alternative "ceisner3"
            """)
        arg_parser.add_argument('--format', metavar='FORMAT_FILE',
            help="""specify the format file for the training and testing files.
            Officially supported format files are located in src/format/
            """)
        arg_parser.add_argument('--max-sentences', metavar='N', type=int,
            help="""run the first [int] sentences only. Usually combined with option -a to gather
            time usage information
            If combined with -a, then time usage information is available, and it will print
            out average time usage after each iteration
            *** Caution: Overrides -t (no evaluation will be conducted), and partially
            overrides -b -e (Only run specified number of sentences) -i (Run forever)
            """)
        arg_parser.add_argument('--log-feature-request', action='store_true',
            help="""log each feature request based on feature type. This is
            helpful for analysing feature usage and building feature caching
            utility.
            Upon exiting the main program will dump feature request information
            into a file named "feature_request.log"
            """)
        arg_parser.add_argument('--spark-shards', '-s', metavar='SHARDS_NUM', type=int,
            help='train using parallelisation with spark')
        arg_parser.add_argument('--prep-path',
            help="""specify the directory in which you would like to store the
            prepared data files after partitioning. For yarn mode the directory
            will be on HDFS.
            """)
        arg_parser.add_argument('--data-path', '-p', metavar='DATA_PATH',
            help="""Path to data files (to the parent directory for all sections)
            default "./penn-wsj-deps/"
            """)
        arg_parser.add_argument('--load-weight-from', '-l', metavar='FILENAME',
            help="""Path to an existing weight vector dump file
            example: "./Weight.db"
            """)
        arg_parser.add_argument('--dump-weight-to', '-d', metavar='PREFIX',
            help="""Path for dumping weight vector. Please also specify a
            prefix of file names, which will be added with iteration count and
            ".db" suffix when dumping the file

            example: "./weight_dump", and the resulting files could be:
            "./weight_dump_Iter_1.db",
            "./weight_dump_Iter_2.db"...
            """)
        arg_parser.add_argument('--dump-frequency', '-f', type=int,
            help="""Frequency of dumping weight vector. This option is only
            valid with option dump-weight-to. The weight vector of last
            iteration will always be dumped.
            example: "-i 6 -f 2"
            weight vector will be dumped at iteration 0, 2, 4, 5.
            """)
        arg_parser.add_argument('--iterations', '-i', metavar='ITERATIONS',
            type=int, help="""Number of iterations
            default 1
            """)
        arg_parser.add_argument('--timing', '-a', action='store_true',
            help="""turn on the timer (output time usage for each sentence)
            If combined with --debug-run-number then before termination it also
            prints out average time usage
            """)
        arg_parser.add_argument('--hadoop', '-c', action='store_true',
            help="""Using Glm Parser in Spark Yarn Mode""")
        arg_parser.add_argument('--tagger-w-vector', metavar='FILENAME',
            help="""Path to an existing w-vector for tagger. Use this option if
            you need to evaluate the glm_parser with a trained tagger.
            """)
        arg_parser.add_argument('--tag-file', metavar='TAG_TARGET', help="""
            specify the file containing the tags we want to use.
            This option is only valid while using option tagger-w-vector.
            Officially provided TAG_TARGET file is src/tagset.txt
            """)

        args = arg_parser.parse_args()

    # Initialise sparkcontext
    sparkContext = None
    yarn_mode  = True if args.hadoop       else False
    spark_mode = True if args.spark_shards else False

    if spark_mode or yarn_mode:
        from pyspark import SparkContext, SparkConf
        conf = SparkConf()
        sparkContext = SparkContext(conf=conf)

    # Process debug options
    if args.max_sentences:
        debug.debug.run_first_num = int(args.max_sentences)
        if debug.debug.run_first_num <= 0:
            __logger.error("Illegal integer: %s\n" % debug.debug.run_first_num)
            sys.exit(1)
        else:
            __logger.info("Debug run number = %d" % (debug.debug.run_first_num, ))
    if args.log_feature_request:
        debug.debug.log_feature_request_flag = True
        __logger.info("Enable feature request log")
    if args.timing:
        debug.debug.time_accounting_flag = True

    # Process config
    if args.config:
        # Check local config path
        if (not os.path.isfile(args.config)) and (not yarn_mode):
            __logger.error("The config file doesn't exist: %s\n" % args.config)
            sys.exit(1)

        # Initialise the config parser
        __logger.info("Reading configurations from file: %s" % (args.config))
        config_parser = SafeConfigParser(os.environ)

        # Read contents of config file
        if yarn_mode:
            listContent = fileRead(args.config, sparkContext)
        else:
            if not args.config.startswith("file://") and not args.config.startswith("hdfs://"):
                listContent = fileRead('file://' + args.config, sparkContext)
            else:
                listContent = fileRead(args.config, sparkContext)

        tmpStr = ''.join(str(e) + "\n" for e in listContent)
        stringIOContent = StringIO.StringIO(tmpStr)
        config_parser.readfp(stringIOContent)

        # Process the contents of config file
        for option in ['train', 'test', 'data_path',
                       'prep_path', 'format', 'tag_file']:
            if config_parser.get('data', option) != '':
                config[option] = config_parser.get('data', option)

        for option in ['load_weight_from', 'dump_weight_to', 'tagger_w_vector']:
            if config_parser.get('option', option) != '':
                config[option] = config_parser.get('option', option)

        for int_option in ['iterations', 'dump_frequency', 'spark_shards']:
            if config_parser.get('option', int_option) != '':
                config[int_option] = config_parser.getint('option', int_option)

        for option in ['learner', 'feature_generator', 'parser']:
            if config_parser.get('core', option) != '':
                config[option] = config_parser.get('core', option)

        try:
            config['data_path'] = cf.get('data', 'data_path')
        except:
            __logger.warn("Encountered exception while attempting to read " +
                          "data_path from config file. It could be caused by the " +
                          "environment variable settings, which is not supported " +
                          "when running in yarn mode")

    # we do this here because we want the defaults to include our config file
    arg_parser.set_defaults(**config)
    args = arg_parser.parse_args()

    # we want to the CLI parameters to override the config file
    config.update(vars(args))

    # Check values of config[]
    if not spark_mode:
        config['spark_shards'] = 1

    if not yarn_mode:
        for option in [
                'data_path',
                'load_weight_from',
                'dump_weight_to',
                'format',
                'tagger_w_vector',
                'tag_file']:
            if config[option] is not None:
                if (not config[option].startswith("file://")) and \
                        (not config[option].startswith("hdfs://")):
                    config[option] = 'file://' + config[option]

    # Initialise Parser
    gp = glm_parser(weightVectorLoadPath = config['load_weight_from'],
                    learner              = config['learner'],
                    parser               = config['parser'],
                    parallelFlag         = spark_mode,
                    sparkContext         = sparkContext)

    # Initialise Tagger
    if config['tagger_w_vector'] is not None:
        __logger.info("Using Tagger weight vector: " + config['tagger_w_vector'])
        if config['tag_file'] is None:
            __logger.error("The tag_file has not been specified")
            sys.exit(1)
        tagger = PosTagger(weightVectorLoadPath = config['tagger_w_vector'],
                           tag_file             = config['tag_file'],
                           sparkContext         = sparkContext)
        __logger.info("Tagger weight vector loaded")
    else:
        tagger = None

    # Run training
    if config['train']:
        trainDataPool = DataPool(section_regex = config['train'],
                                 data_path     = config['data_path'],
                                 fgen          = config['feature_generator'],
                                 format_path   = config['format'],
                                 shardNum      = config['spark_shards'],
                                 sc            = sparkContext,
                                 hadoop        = yarn_mode)

        gp.train(dataPool             = trainDataPool,
                 maxIteration         = config['iterations'],
                 weightVectorDumpPath = config['dump_weight_to'],
                 dumpFrequency        = config['dump_frequency'],
                 shardNum             = config['spark_shards'],
                 parallel             = spark_mode,
                 sc                   = sparkContext,
                 hadoop               = yarn_mode)

    # Run evaluation
    if config['test']:
        testDataPool = DataPool(section_regex = config['test'],
                                data_path     = config['data_path'],
                                fgen          = config['feature_generator'],
                                format_path   = config['format'],
                                sc            = sparkContext,
                                hadoop        = yarn_mode)

        gp.evaluate(dataPool = testDataPool,
                    tagger   = tagger,
                    sc       = sparkContext,
                    hadoop   = yarn_mode)

    # Finalising, shutting down spark
    if spark_mode:
        sparkContext.stop()
