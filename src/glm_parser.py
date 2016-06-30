# -*- coding: utf-8 -*-

#
# Global Linear Model Parser
# Simon Fraser University
# NLP Lab
#
# Author: Yulan Huang, Ziqi Wang, Anoop Sarkar, Jetic Gu
# (Please add on your name if you have authored this file)
#
from feature import feature_vector

from data.data_pool import *

from evaluate.evaluator import *

from weight.weight_vector import *

from data.file_io import *

import debug.debug

import timeit
import time
import os
import sys
import logging
import importlib

import argparse
import StringIO
from ConfigParser import SafeConfigParser

__version__ = '1.0'


class GlmParser():
    def __init__(self,
                 weightVectorLoadPath = None,
                 maxIteration         = 1,
                 learner              = None,
                 fgen                 = None,
                 parser               = None,
                 parallelFlag         = False):

        print ("PARSER [DEBUG]: Initialising Parser")
        if fgen is None:
            raise ValueError("PARSER [ERROR]: Feature Generator not specified")
        if learner is None:
            raise ValueError("PARSER [ERROR]: Learner not specified")

        self.maxIteration = maxIteration
        self.w_vector     = WeightVector(weightVectorLoadPath)
        self.evaluator    = Evaluator()

        if parallelFlag:
            self.learner = importlib.import_module('learn.' + learner).Learner()
        else:
            self.learner = importlib.import_module('learn.' + learner).Learner(self.w_vector)
        print("PARSER [INFO]: Using learner: %s " % (self.learner.learner_name))

        self.fgen = importlib.import_module('feature.' + fgen).FeatureGenerator
        print("PARSER [INFO]: Using feature generator: %s " % (fgen))

        self.parser = importlib.import_module('parse.' + parser).EisnerParser()
        print("PARSER [INFO]: Using parser: %s" % (parser))

        print ("PARSER [DEBUG]: Initialisation Complete")
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

        print ("PARSER [DEBUG]: Starting Training Process")

        if dataPool is None:
            raise ValueError("PARSER [ERROR]: DataPool for training not specified")
        if maxIteration is None:
            # We shall encourage the users to specify the number of iterations by themselves
            print ("PARSER [WARN]: Number of Iterations not specified, using 1")
            maxIteration = 1

        if not parallel:
            # It means we will be using sequential training
            print ("PARSER [DEBUG]: Using Sequential Training")
            self.learner.sequential_learn(f_argmax   = self.f_argmax,
                                          data_pool  = dataPool,
                                          max_iter   = maxIteration,
                                          d_filename = weightVectorDumpPath,
                                          dump_freq  = dumpFrequency)
        else:
            print ("PARSER [DEBUG]: Using Parallel Training")
            if shardNum is None:
                # We shall encourage the users to specify the number of shards by themselves
                print ("PARSER [WARN]: Number of shards not specified, using 1")
                shardNum = 1
            if sc is None:
                raise RuntimeError('PARSER [ERROR]: SparkContext not specified')

            parallelLearnClass = importlib.import_module('learn.spark_train').ParallelPerceptronLearner
            learner = parallelLearnClass(self.w_vector, maxIteration)
            learner.parallel_learn(max_iter     = maxIteration,
                                   dataPool     = dataPool,
                                   shards       = shardNum,
                                   fgen         = self.fgen,
                                   parser       = self.parser,
                                   learner      = self.learner,
                                   sc           = sc,
                                   d_filename   = weightVectorDumpPath,
                                   hadoop       = hadoop)
        return

    def evaluate(self, dataPool = None):
        if dataPool is None:
            raise ValueError("PARSER [ERROR]: DataPool for evaluation not specified")
        self.evaluator.evaluate(dataPool, self.parser, self.w_vector)

    def f_argmax(self, sentence):
        current_edge_set = self.parser.parse(sentence, self.w_vector.get_vector_score)
        current_global_vector = sentence.set_current_global_vector(current_edge_set)
        return current_global_vector

if __name__ == "__main__":
    # Default values
    config = {
        'train': None,
        'test': None,
        'iterations': 1,
        'data_path': None,
        'load_weight_from': None,
        'dump_weight_to': None,
        'dump_frequency': 1,
        'spark_shards': 1,
        'prep_path': 'data/prep',
        'learner': 'average_perceptron',
        'parser': 'ceisner',
        'feature_generator': 'english_1st_fgen',
        'format': 'format/penn2malt.format',
    }

    glm_parser = GlmParser

    # Dealing with arguments here
    if True: # Adding arguments
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
            help="""log each feature request based on feature type. This is helpful for
            analysing feature usage and building feature caching utility.
            Upon exiting the main program will dump feature request information
            into a file named "feature_request.log"
            """)
        arg_parser.add_argument('--spark-shards', '-s', metavar='SHARDS_NUM', type=int,
            help='train using parallelisation with spark')
        arg_parser.add_argument('--prep-path',
            help="""specify the directory in which you would like to store prepared data files after partitioning
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
            help="""Path for dumping weight vector. Please also specify a prefix
            of file names, which will be added with iteration count and
            ".db" suffix when dumping the file

            example: "./weight_dump", and the resulting files could be:
            "./weight_dump_Iter_1.db",
            "./weight_dump_Iter_2.db"...
            """)
        arg_parser.add_argument('--dump-frequency', '-f', type=int,
            help="""Frequency of dumping weight vector. The weight vector of last
            iteration will always be dumped
            example: "-i 6 -f 2"
            weight vector will be dumped at iteration 0, 2, 4, 5.
            """)
        arg_parser.add_argument('--iterations', '-i', metavar='ITERATIONS', type=int,
            help="""Number of iterations
            default 1
            """)
        arg_parser.add_argument('--timing', '-a', action='store_true',
            help="""turn on the timer (output time usage for each sentence)
            If combined with --debug-run-number then before termination it also
            prints out average time usage
            """)
        arg_parser.add_argument('--hadoop', '-c', action='store_true',
           help="""Using Glm Parser in Spark Yarn Mode""")

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
            raise ValueError("Illegal integer: %d" % (debug.debug.run_first_num, ))
        else:
            print("Debug run number = %d" % (debug.debug.run_first_num, ))
    if args.log_feature_request:
        debug.debug.log_feature_request_flag = True
        print("Enable feature request log")
    if args.timing:
        debug.debug.time_accounting_flag = True

    # Process config
    if args.config:
        # Check local config path
        if (not os.path.isfile(args.config)) and (not yarn_mode):
            raise ValueError("The config file doesn't exist: " + args.config)

        # Initialise the config parser
        print("Reading configurations from file: %s" % (args.config))
        config_parser = SafeConfigParser(os.environ)

        # Read contents of config file
        if yarn_mode:
            listContent = fileRead(args.config, sparkContext)
        else:
            listContent = fileRead("file://" + args.config, sparkContext)
        tmpStr = ''.join(str(e)+"\n" for e in listContent)
        stringIOContent = StringIO.StringIO(tmpStr)
        config_parser.readfp(stringIOContent)

        # Process the contents of config file
        for option in ['train', 'test', 'data_path', 'prep_path', 'format']:
            if config_parser.get('data', option) != '':
                config[option] = config_parser.get('data', option)

        for option in ['load_weight_from', 'dump_weight_to']:
            if config_parser.get('option', option) != '':
                config[option] = config_parser.get('option', option)

        for int_option in ['iterations', 'dump_frequency', 'spark_shards']:
            if config_parser.get('option', int_option) != '':
                config[int_option] = config_parser.getint('option', int_option)

        for option in ['learner', 'feature_generator', 'parser']:
            if config_parser.get('option', int_option) != '':
                config[option] = config_parser.get('core', option)

        try:
            config['data_path'] = cf.get('data', 'data_path')
        except:
            print "WARNING: Unable to read data_path from config file. ",
            print "It could be caused by the environment variable settings, ",
            print "which is not supported when running in yarn mode"

    # we do this here because we want the defaults to include our config file
    arg_parser.set_defaults(**config)
    args = arg_parser.parse_args()

    # we want to the CLI parameters to override the config file
    config.update(vars(args))

    # Check values of config[]
    if config['data_path'] is None:
        raise ValueError("data_path not specified.")
    if (not os.path.isdir(config['data_path'])) and (not yarn_mode):
        raise ValueError("The data_path directory doesn't exist: " + config['data_path'])
    if (not os.path.isfile(config['format'])) and (not yarn_mode):
        raise ValueError("The format file doesn't exist: " + config['format'])

    # Initialise Parser
    gp = glm_parser(weightVectorLoadPath = config['load_weight_from'],
                    learner              = config['learner'],
                    fgen                 = config['feature_generator'],
                    parser               = config['parser'],
                    parallelFlag         = spark_mode)

    # Run training
    if config['train'] is not None:
        trainDataPool = DataPool(section_regex = config['train'],
                                 data_path     = config['data_path'],
                                 fgen          = config['feature_generator'],
                                 format_path   = config['format'],
                                 shardNum      = config['spark_shards'],
                                 sc            = sparkContext,
                                 hadoop        = yarn_mode)

        start_time = time.time()
        gp.train(dataPool             = trainDataPool,
                 maxIteration         = config['iterations'],
                 weightVectorDumpPath = config['dump_weight_to'],
                 dumpFrequency        = config['dump_frequency'],
                 shardNum             = config['spark_shards'],
                 parallel             = spark_mode,
                 sc                   = sparkContext,
                 hadoop               = yarn_mode)
        end_time = time.time()

        training_time = end_time - start_time
        print "Total Training Time: ", training_time
        logging.info("Training time usage(seconds): %f" % (training_time,))

    # Run evaluation
    if config['train'] is not None:
        testDataPool = DataPool(section_regex = config['test'],
                                data_path     = config['data_path'],
                                fgen          = config['feature_generator'],
                                format_path   = config['format'],
								sc            = sparkContext,
								hadoop        = yarn_mode)
        print "Evaluating..."
        gp.evaluate(dataPool=testDataPool)

    # Finalising, shutting down spark
    if spark_mode:
        sparkContext.stop()
