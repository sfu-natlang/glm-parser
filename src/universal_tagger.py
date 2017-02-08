# -*- coding: utf-8 -*-

#
# Part of Speech Tagger
# Simon Fraser University
# NLP Lab
#
# Author: Yulan Huang, Ziqi Wang, Anoop Sarkar, Jetic Gu, Kingston Chen, Jerry Li
#
# (Please add on your name if you have authored this file)
#
import debug.debug
from data.file_io import fileRead, fileWrite
from data.data_pool import DataPool
from weight.weight_vector import WeightVector
from logger.loggers import logging, init_logger
from feature.feature_vector import FeatureVector

from evaluate.tagger_evaluator import Evaluator
from data.tagset_reader import read_tagset

import time
import os
import sys
import importlib
import functools
import argparse
import StringIO
from ConfigParser import SafeConfigParser

__version__ = '1.2'
if __name__ == '__main__':
    init_logger('universal_tagger.log')
logger = logging.getLogger('TAGGER')


class Tagger():
    def __init__(self,
                 weightVectorLoadPath = None,
                 tagger               = "viterbi",
                 tagFile              = "file://tagset.txt",
                 sparkContext         = None):

        logger.info("Initialising Tagger")
        self.w_vector = WeightVector(weightVectorLoadPath, sparkContext)
        self.evaluator = Evaluator

        self.tagger = importlib.import_module('tagger.' + tagger).Tagger()
        logger.info("Using tagger: %s" % (tagger))

        self.tagset = read_tagset(tagFile, sparkContext)
        logger.info("Tag File selected: %s" % tagFile)
        self.default_tag = self.tagset[0]
        logger.info("Initialisation Complete")
        return

    def train(self,
              dataPool,
              maxIteration         = 1,
              learner              = 'average_perceptron',
              weightVectorDumpPath = None,
              dumpFrequency        = 1,
              parallel             = False,
              sparkContext         = None,
              hadoop               = False):

        # Check values
        if not isinstance(dataPool, DataPool):
            raise ValueError("TAGGER [ERROR]: dataPool for training is not an DataPool object")
        if maxIteration is None:
            logger.warn("Number of Iterations not specified, using 1")
            maxIteration = 1
        if learner is None:
            raise ValueError("TAGGER [ERROR]: Learner not specified")

        # Load Learner
        learner = importlib.import_module('learner.' + learner).Learner(self.w_vector)

        # Prepare the suitable argmax
        def tagger_f_argmax(w_vector, sentence, tagger, tagset, default_tag):
            output = tagger.tag(sentence    = sentence,
                                w_vector    = w_vector,
                                tagset      = tagset,
                                default_tag = default_tag)
            current_global_vector = FeatureVector(sentence.get_local_vector(output=output))
            return current_global_vector
        f_argmax = functools.partial(tagger_f_argmax,
                                     tagger=self.tagger,
                                     tagset=self.tagset,
                                     default_tag=self.default_tag)

        # Start Training Process
        logger.info("Starting Training Process")
        start_time = time.time()
        if not parallel:  # using sequential training
            self.w_vector = learner.sequential_learn(
                f_argmax   = f_argmax,
                data_pool  = dataPool,
                iterations = maxIteration,
                d_filename = weightVectorDumpPath,
                dump_freq  = dumpFrequency)
        else:  # using parallel training
            self.w_vector = learner.parallel_learn(
                f_argmax     = f_argmax,
                data_pool    = dataPool,
                iterations   = maxIteration,
                d_filename   = weightVectorDumpPath,
                dump_freq    = dumpFrequency,
                sparkContext = sparkContext,
                hadoop       = hadoop)

        end_time = time.time()
        logger.info("Total Training Time(seconds): %f" % (end_time - start_time,))
        return

    def evaluate(self,
                 dataPool,
                 exportFileURI=None,
                 parallel=False,
                 sparkContext=None,
                 hadoop=None):

        logger.info("Starting evaluation process")
        if not isinstance(dataPool, DataPool):
            raise ValueError("TAGGER [ERROR]: dataPool for evaluation is not an DataPool object")

        start_time = time.time()
        evaluator = self.evaluator(self.tagger, self.tagset)
        if not parallel:
            resultingDataPool = evaluator.sequentialEvaluate(
                data_pool    = dataPool,
                w_vector     = self.w_vector,
                sparkContext = sparkContext,
                hadoop       = hadoop)
            if exportFileURI is not None:
                resultingDataPool.export(exportFileURI, sparkContext)
        else:
            resultingDataPool = evaluator.parallelEvaluate(
                data_pool    = dataPool,
                w_vector     = self.w_vector,
                sparkContext = sparkContext,
                hadoop       = hadoop)
        end_time = time.time()
        logger.info("Total evaluation Time(seconds): %f" % (end_time - start_time,))

    def getTags(self, sentence, fgen="POS"):
        if fgen == "POS":
            from feature.pos_fgen import FeatureGenerator
        elif fgen == "NER":
            from feature.ner_fgen import FeatureGenerator

        inital_fgen = sentence.fgen

        sentence.load_fgen(FeatureGenerator)
        output = self.tagger.tag(sentence, self.w_vector, self.tagset, self.default_tag)
        sentence.load_fgen(inital_fgen)

        return output[2:]

if __name__ == '__main__':
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
        'tagger':            'viterbi',
        'feature_generator': 'english_1st_fgen',
        'format':            'penn2malt',
        'tag_file':          None,
        'export':            'output.txt'
    }

    # Dealing with arguments here
    if True:  # Adding arguments
        arg_parser = argparse.ArgumentParser(
            description="""Universal Tagger
            Version %s""" % __version__)
        arg_parser.add_argument('config', metavar='CONFIG_FILE', nargs='?',
            help="""specify the config file. This will load all the setting from the config file,
            in order to avoid massive command line inputs. Please consider using config files
            instead of manually typing all the options.

            Additional options by command line will override the settings in the config file.

            Officially provided config files are located in src/config/
            """)
        arg_parser.add_argument('--train', metavar='TRAIN_FILE_PATTERN',
            help="""specify the data for training with regular expression""")
        arg_parser.add_argument('--test', metavar='TEST_FILE_PATTERN',
            help="""specify the data for testing with regular expression""")
        arg_parser.add_argument('--feature-generator',
            choices=['pos_fgen', 'ner_fgen'],
            help="""specify feature generation facility by a python file name.
            The file will be searched under /feature directory.
            """)
        arg_parser.add_argument('--learner',
            choices=['average_perceptron', 'perceptron'],
            help="""specify a learner for weight vector training""")
        arg_parser.add_argument('--tagger',
            choices=['viterbi', 'viterbi_pruning'],
            help="""specify the tagger using tagger module name (i.e. .py file
            name without suffix).

            default "viterbi"; alternative "viterbi_pruning"
            """)
        arg_parser.add_argument('--format', metavar='FORMAT',
            help="""specify the format file for the training and testing files.
            Officially supported format files are located in src/data_format/
            """)
        arg_parser.add_argument('--spark-shards', '-s', metavar='SHARDS_NUM',
            type=int, help='train using parallelisation with spark')
        arg_parser.add_argument('--prep-path',
            help="""specify the directory in which you would like to store the
            prepared data files after partitioning. For yarn mode the directory
            will be on HDFS.
            """)
        arg_parser.add_argument('--data-path', '-p', metavar='DATA_PATH',
            help="""Path to data files (to the parent directory for all sections)
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
            type=int, help="""Number of iterations, default is 1""")
        arg_parser.add_argument('--hadoop', '-c', action='store_true',
            help="""Using the Tagger in Spark Yarn Mode""")
        arg_parser.add_argument('--tagger-w-vector', metavar='FILENAME',
            help="""Path to an existing w-vector for tagger.""")
        arg_parser.add_argument('--tag-file', metavar='TAG_TARGET', help="""
            specify the file containing the tags we want to use.
            This option is only valid while using option tagger-w-vector.
            Officially provided TAG_TARGET file is src/tagset.txt
            """)
        arg_parser.add_argument('--export', '-e', metavar='EXPORTURI', help="""
            Export the result after finished evaluation to designated URI.
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
        for option in ['train', 'test', 'prep_path', 'format', 'tag_file']:
            if config_parser.get('data', option) != '':
                config[option] = config_parser.get('data', option)

        for option in ['load_weight_from', 'dump_weight_to']:
            if config_parser.get('option', option) != '':
                config[option] = config_parser.get('option', option)

        for int_option in ['iterations', 'dump_frequency', 'spark_shards']:
            if config_parser.get('option', int_option) != '':
                config[int_option] = config_parser.getint('option', int_option)

        for option in ['learner', 'feature_generator', 'tagger']:
            if config_parser.get('core', option) != '':
                config[option] = config_parser.get('core', option)

        try:
            config['data_path'] = config_parser.get('data', 'data_path')
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
                'export',
                'tag_file']:
            if config[option] is not None:
                if (not config[option].startswith("file://")) and \
                        (not config[option].startswith("hdfs://")):
                    config[option] = 'file://' + config[option]

    # Initialise Tagger
    tagger = Tagger(weightVectorLoadPath = config['load_weight_from'],
                    tagger               = config['tagger'],
                    tagFile              = config['tag_file'],
                    sparkContext         = sparkContext)

    # Run training
    if config['train']:
        trainDataPool = DataPool(fgen         = config['feature_generator'],
                                 data_format  = config['format'],
                                 data_regex   = config['train'],
                                 data_path    = config['data_path'],
                                 shards       = config['spark_shards'],
                                 sparkContext = sparkContext,
                                 hadoop       = yarn_mode)

        tagger.train(dataPool             = trainDataPool,
                     maxIteration         = config['iterations'],
                     learner              = config['learner'],
                     weightVectorDumpPath = config['dump_weight_to'],
                     dumpFrequency        = config['dump_frequency'],
                     parallel             = spark_mode,
                     sparkContext         = sparkContext,
                     hadoop               = yarn_mode)

    # Run evaluation
    if config['test']:
        testDataPool = DataPool(fgen         = config['feature_generator'],
                                data_format  = config['format'],
                                data_regex   = config['test'],
                                data_path    = config['data_path'],
                                shards       = config['spark_shards'],
                                sparkContext = sparkContext,
                                hadoop       = yarn_mode)

        tagger.evaluate(dataPool      = testDataPool,
                        exportFileURI = config['export'],
                        parallel      = spark_mode,
                        sparkContext  = sparkContext,
                        hadoop        = yarn_mode)

    # Finalising, shutting down spark
    if spark_mode:
        sparkContext.stop()
