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

from data.data_prep import *

import debug.debug
import debug.interact

import timeit
import time
import sys,os
import logging

import argparse
import ConfigParser
from ConfigParser import SafeConfigParser

class GlmParser():
    def __init__(self,
                 weightVectorLoadPath = None,
                 maxIteration         = 1,
                 learner              = None,
                 fgen                 = None,
                 parser               = None,
                 dataFormat           = None,
                 parallelFlag         = False):

        print ("PARSER [DEBUG]: Initialising Parser")
        if fgen == None:
            raise ValueError("PARSER [ERROR]: Feature Generator not specified")
        if learner == None:
            raise ValueError("PARSER [ERROR]: Learner not specified")
        if dataFormat == None and parallelFlag == True:
            raise ValueError("PARSER [ERROR]: DataFormat not specified")

        self.maxIteration = maxIteration
        self.w_vector     = WeightVector(weightVectorLoadPath)
        self.dataFormat   = dataFormat
        self.evaluator    = Evaluator()

        if parallelFlag:
            self.learner = getClassFromModule('parallel_learn', 'learn', learner)
            self.learner = self.learner()
        else:
            self.learner = getClassFromModule('sequential_learn', 'learn', learner)
            self.learner = self.learner(self.w_vector, maxIteration)
        print("PARSER [INFO]: Using learner: %s " % (learner))

        self.fgen = getClassFromModule('get_local_vector', 'feature', fgen)
        print("PARSER [INFO]: Using feature generator: %s " % (fgen))

        self.parser = getClassFromModule('parse', 'parse', parser)
        self.parser = self.parser()
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

        if dataPool == None:
            raise ValueError("PARSER [ERROR]: DataPool for training not specified")
        if maxIteration == None:
            # We shall encourage the users to specify the number of iterations by themselves
            print ("PARSER [WARN]: Number of Iterations not specified, using 1")
            maxIteration = 1

        if parallel == False:
            # It means we will be using sequential training
            print ("PARSER [DEBUG]: Using Sequential Training")
            self.learner.sequential_learn(f_argmax   = self.f_argmax,
                                          data_pool  = dataPool,
                                          max_iter   = maxIteration,
                                          d_filename = weightVectorDumpPath,
                                          dump_freq  = dumpFrequency)
        else:
            print ("PARSER [DEBUG]: Using Parallel Training")
            if shardNum == None:
                # We shall encourage the users to specify the number of shards by themselves
                print ("PARSER [WARN]: Number of shards not specified, using 1")
                shardNum = 1
            if sc == None:
                print ("PARSER [INFO]: SparkContext not specified, will try to specify now")
                try:
                    from pyspark import SparkContext,SparkConf
                    conf = SparkConf()
                    sc = SparkContext(conf=conf)
                except:
                    raise RuntimeError('DATAPREP [ERROR]: SparkContext entity conflict, entity already exists')
                externalSparkContext = False
            else:
                externalSparkContext = True

            parallelLearnClass = getClassFromModule('parallel_learn', 'learn', 'spark_train')
            learner = parallelLearnClass(self.w_vector,maxIteration)
            learner.parallel_learn(max_iter     = maxIteration,
                                   dataPool     = dataPool,
                                   shards       = shardNum,
                                   fgen         = self.fgen,
                                   parser       = self.parser,
                                   format_path  = self.dataFormat,
                                   learner      = self.learner,
                                   sc           = sc,
                                   d_filename   = weightVectorDumpPath,
                                   hadoop       = hadoop)
            if externalSparkContext == False:
                sc.stop()
                sc = None
        return

    def evaluate(self, dataPool = None):

        if dataPool == None:
            raise ValueError("PARSER [ERROR]: DataPool for evaluation not specified")

        self.evaluator.evaluate(dataPool, self.parser, self.w_vector)

    def f_argmax(self, sentence):
        current_edge_set = self.parser.parse(sentence, self.w_vector.get_vector_score)
        current_global_vector = sentence.set_current_global_vector(current_edge_set)
        return current_global_vector

MAJOR_VERSION = 1
MINOR_VERSION = 0

if __name__ == "__main__":
    import getopt, sys

    # Default values
    train_regex   = ''
    test_regex    = ''
    maxIteration  = 1
    data_path     = ''  #"./penn-wsj-deps/"
    l_filename    = None
    d_filename    = None
    dump_freq     = 1
    parallel_flag = False
    shards_number = 1
    h_flag        = False
    prep_path     = 'data/prep/' #to be changed
    interactValue = False
    learnerValue  = 'average_perceptron'
    fgenValue     = 'english_1st_fgen'
    parserValue   = 'ceisner'
    data_format   = 'format/penn2malt.format'

    glm_parser = GlmParser

    # Dealing with arguments here
    if True: # Adding arguments
        arg_parser = argparse.ArgumentParser(description="""Global Linear Model (GLM) Parser
            Version %d.%d""" % (MAJOR_VERSION, MINOR_VERSION))
        arg_parser.add_argument('config', metavar='CONFIG_FILE',
            help="""specify the config file. This will load all the setting from the config file,
            in order to avoid massive command line inputs. Please consider using config files
            instead of manually typing all the options.

            Additional options by command line will override the settings in the config file.

            Officially provided config files are located in src/config/
            """)
        arg_parser.add_argument('--train', metavar='TRAIN_REGEX',
            help="""specify the data for training with regular expression
            """)
        arg_parser.add_argument('--test', metavar='TEST_REGEX',
            help="""specify the data for testing with regular expression
            """)
        arg_parser.add_argument('--fgen',
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
            help="""specify a learner for weight vector training
            default "average_perceptron"; alternative "perceptron"
            """)
        arg_parser.add_argument('--parser',
            help="""specify the parser using parser module name (i.e. .py file name without suffix).
            The recognition rule is the same as --fgen switch. A valid parser object
            must possess "parse" attribute in order to be recognised as a parser
            implementation.

            Some parser might not work correctly with the infrastructure, which keeps
            changing all the time. If this happens please file an issue on github page

            default "ceisner"; alternative "ceisner3"
            """)
        arg_parser.add_argument('--format', metavar='DATA_FORMAT',
            help="""specify the format file for the training and testing files.
            Officially supported format files are located in src/format/
            """)
        arg_parser.add_argument('--debug-run-number', metavar='N', type=int,
            help="""run the first [int] sentences only. Usually combined with option -a to gather
            time usage information
            If combined with -a, then time usage information is available, and it will print
            out average time usage after each iteration
            *** Caution: Overrides -t (no evaluation will be conducted), and partially
            overrides -b -e (Only run specified number of sentences) -i (Run forever)
            """)
        #arg_parser.add_argument('--interactive', action='store_true',
        #    help="""use interactive version of glm-parser, in which you have access to some
        #    critical points ("breakpoints") in the procedure
        #    """)
        arg_parser.add_argument('--log-feature-request', action='store_true',
            help="""log each feature request based on feature type. This is helpful for
            analysing feature usage and building feature caching utility.
            Upon exiting the main program will dump feature request information
            into a file named "feature_request.log"
            """)
        arg_parser.add_argument('--spark', '-s', metavar='SHARDS_NUM', type=int,
            help='train using parallelisation')
        arg_parser.add_argument('--prep-path',
            help="""specify the directory in which you would like to store prepared data files after partitioning
            """)
        arg_parser.add_argument('--path', '-p', metavar='DATA_PATH',
            help="""Path to data files (to the parent directory for all sections)
            default "./penn-wsj-deps/"
            """)
        arg_parser.add_argument('-l', metavar='L_FILENAME',
            help="""Path to an existing weight vector dump file
            example: "./Weight.db"
            """)
        arg_parser.add_argument('-d', metavar='D_FILENAME',
            help="""Path for dumping weight vector. Please also specify a prefix
            of file names, which will be added with iteration count and
            ".db" suffix when dumping the file

            example: "./weight_dump", and the resulting files could be:
            "./weight_dump_Iter_1.db",
            "./weight_dump_Iter_2.db"...
            """)
        arg_parser.add_argument('--frequency', '-f', type=int,
            help="""Frequency of dumping weight vector. The weight vector of last
            iteration will always be dumped
            example: "-i 6 -f 2"
            weight vector will be dumped at iteration 0, 2, 4, 5.
            """)
        arg_parser.add_argument('--iteration', '-i', metavar='ITERATIONS', type=int,
            help="""Number of iterations
            default 1
            """)
        arg_parser.add_argument('--timer', '-a', action='store_true',
            help="""turn on the timer (output time usage for each sentence)
            If combined with --debug-run-number then before termination it also
            prints out average time usage
            """)
        arg_parser.add_argument('--hadoop', '-c', action='store_true')
        args=arg_parser.parse_args()

    if args.config: # Process config
        if not os.path.isfile(args.config):
            raise ValueError('Specified config file does not exist or is not a file: ' + args.config)
        print("Reading configurations from file: %s" % (args.config))
        cf = SafeConfigParser(os.environ)
        cf.read(args.config)

        train_regex    = cf.get("data", "train")
        test_regex     = cf.get("data", "test")
        try:
            data_path      = cf.get("data", "data_path")
        except:
            print ("WARNING: Unable to read data_path from config file. It could be caused by the environment variable settings, which it not supported when running in yarn mode")
        prep_path      = cf.get("data", "prep_path")
        data_format    = cf.get("data", "format")

        h_flag                               = cf.get(       "option", "h_flag")
        parallel_flag                        = cf.getboolean("option", "parallel_train")
        shards_number                        = cf.getint(    "option", "shards")
        maxIteration                         = cf.getint(    "option", "iteration")
        l_filename                           = cf.get(       "option", "l_filename") if cf.get(       "option", "l_filename") != '' else None
        d_filename                           = cf.get(       "option", "d_filename") if cf.get(       "option", "l_filename") != '' else None
        debug.debug.time_accounting_flag     = cf.getboolean("option", "timer")
        dump_freq                            = cf.getint(    "option", "dump_frequency")
        debug.debug.log_feature_request_flag = cf.getboolean("option", "log-feature-request")
        interactValue                        = cf.getboolean("option", "interactive")

        learnerValue   = cf.get(       "core", "learner")
        fgenValue      = cf.get(       "core", "feature_generator")
        parserValue    = cf.get(       "core", "parser")

    if True: # Process other arguments
        if args.hadoop:
            h_flag = True
        if args.spark:
            shards_number = int(args.spark)
            parallel_flag = True
        if args.path:
            data_path = args.path
        if args.iteration:
            maxIteration = int(args.iteration)
        if args.l:
            l_filename = args.l
        if args.d:
            d_filename = args.d
        if args.timer:
            debug.debug.time_accounting_flag = True
        if args.frequency:
            dump_freq = int(args.frequency)
        if args.train:
            train_regex = args.train
        if args.test:
            test_regex = args.test
        if args.debug_run_number:
            debug.debug.run_first_num = int(args.debug-run-number)
            if debug.debug.run_first_num <= 0:
                raise ValueError("Illegal integer: %d" % (debug.debug.run_first_num, ))
            else:
                print("Debug run number = %d" % (debug.debug.run_first_num, ))
        if args.prep_path:
            prep_path = args.prep_path
        if args.learner:
            learnerValue = args.learner
        if args.fgen:
            fgenValue = args.fgen
        if args.parser:
            parserValue = args.parser
        #if args.interactive:
        #    interactValue = True
        if args.log_feature_request:
            debug.debug.log_feature_request_flag = True
        if args.format:
            data_format = args.format;

    # process options

    if debug.debug.time_accounting_flag == True:
        print("Time accounting is ON")

    #if interactValue == True:
    #    glm_parser.sequential_train = debug.interact.glm_parser_sequential_train_wrapper
    #    glm_parser.evaluate = debug.interact.glm_parser_evaluate_wrapper
    #    glm_parser.f_argmax = debug.interact.glm_parser_compute_argmax_wrapper
    #    DataPool.get_data_list = debug.interact.data_pool_get_data_list_wrapper
    #    learner.sequential_learn = debug.interact.average_perceptron_learner_sequential_learn_wrapper
    #    print("Enable interactive mode")

    if debug.debug.log_feature_request_flag == True:
        print("Enable feature request log")

    # Initialisation:
    #     Initialise Parser
    gp = glm_parser(weightVectorLoadPath = l_filename,
                    learner              = learnerValue,
                    fgen                 = fgenValue,
                    parser               = parserValue,
                    parallelFlag         = parallel_flag,
                    dataFormat           = data_format)

    #     Initialise sparkcontext
    sc = None
    if parallel_flag == True:
        from pyspark import SparkContext,SparkConf
        conf = SparkConf()
        sc = SparkContext(conf=conf)

    #     Initialise Timer
    training_time = None

    # Run training
    if train_regex is not '':
        trainDataPool = DataPool(section_regex = train_regex,
                                 data_path     = data_path,
                                 fgen          = fgenValue,
                                 format_path   = data_format,
                                 shardNum      = shards_number,
                                 sc            = sc,
                                 hadoop        = h_flag)

        start_time = time.time()
        gp.train(dataPool             = trainDataPool,
                 maxIteration         = maxIteration,
                 weightVectorDumpPath = d_filename,
                 dumpFrequency        = 1,
                 parallel             = parallel_flag,
                 shardNum             = shards_number,
                 sc                   = sc,
                 hadoop               = h_flag)
        end_time = time.time()

        training_time = end_time - start_time
        print "Total Training Time: ", training_time
        logging.info("Training time usage(seconds): %f" % (training_time,))

    # Run evaluation
    if test_regex is not '':
        testDataPool = DataPool(section_regex = test_regex,
                                data_path     = data_path,
                                fgen          = fgenValue,
                                format_path   = data_format)
        print "Evaluating..."
        gp.evaluate(dataPool = testDataPool)

    # Finalising
    if parallel_flag:
        sc.stop()
