# -*- coding: utf-8 -*-
from __future__ import print_function

#
# Global Linear Model Parser
# Simon Fraser University
# NLP Lab
#
# Author: Yulan Huang, Ziqi Wang, Anoop Sarkar
# (Please add on your name if you have authored this file)
#
from data.data_pool import DataPool

from evaluate.evaluator import Evaluator

from weight.weight_vector import WeightVector

from learn.partition import partition_data

import time
import importlib
import os
import sys
import argparse
import ConfigParser

__version__ = '1.0'

class GlmParser():
    def __init__(self, train="",
                 test="",
                 iterations=1,
                 data_path="penn-wsj-deps/",
                 load_weight_from=None,
                 dump_weight_to=None,
                 learner=None,
                 feature_generator=None,
                 parser=None,
                 data_format="format/penn2malt.format",
                 prep_path="data/prep",
                 parallel=False,
                 dump_freq=1,
                 shards=1,
                 **kwargs):

        self.train = train
        self.test = test
        self.iterations = iterations
        self.data_path = data_path
        self.w_vector = WeightVector(load_weight_from)
        self.prep_path = prep_path
        self.dump_freq = dump_freq
        self.load_weight_from = load_weight_from
        self.dump_weight_to = dump_weight_to
        self.data_format = data_format
        self.shards = shards
        self.parser = parser()
        self.evaluator = Evaluator()

        if feature_generator:
            # Do not instantiate this here; it's used elsewhere
            self.feature_generator = feature_generator
        else:
            raise ValueError("You need to specify a feature generator")

        # XXX Why is the data being loaded here?
        if not parallel:
            self.train_data_pool = DataPool(train, data_path,
                                            fgen=self.feature_generator,
                                            format_path=self.data_format)

        if test:
            self.test_data_pool = DataPool(test, data_path,
                                           fgen=self.feature_generator,
                                           format_path=self.data_format)

        if learner:
            if parallel:
                self.learner = learner()
            else:
                self.learner = learner(self.w_vector, self.iterations)
        else:
            raise ValueError("You need to specify a learner")

    def sequential_train(self):

        if self.train:
            train_data_pool = DataPool(self.train,
                                       self.data_path,
                                       fgen=self.feature_generator,
                                       format_path=self.data_format)
        else:
            train_data_pool = self.train_data_pool

        self.learner.sequential_learn(self.compute_argmax,
                                      train_data_pool,
                                      self.iterations,
                                      self.dump_weight_to,
                                      self.dump_freq)

    def parallel_train(self, shards=1, parallel_learner=None,
                       spark_context=None, hadoop=False):

        output_path = partition_data(self.data_path, self.train, self.shards,
                                     self.prep_path)

        parallel_learner = parallel_learner(self.w_vector, self.iterations)

        parallel_learner.parallel_learn(self.iterations,
                                        output_path,
                                        self.shards,
                                        fgen=self.feature_generator,
                                        parser=self.parser,
                                        format_path=self.data_format,
                                        learner=self.learner,
                                        sc=spark_context,
                                        d_filename=self.dump_weight_to)

    def evaluate(self, training_time,  test_regex=''):
        if not test_regex == '':
            test_data_pool = DataPool(self.test,
                                      self.data_path,
                                      fgen=self.feature_generator,
                                      format_path=self.data_format)

        else:
            test_data_pool = self.test_data_pool

        self.evaluator.evaluate(test_data_pool, self.parser, self.w_vector,
                                training_time)


    def compute_argmax(self, sentence):
        current_edge_set = self.parser.parse(sentence, self.w_vector.get_vector_score)
        #sentence.set_current_global_vector(current_edge_set)
        #current_global_vector = sentence.current_global_vector
        current_global_vector = sentence.set_current_global_vector(current_edge_set)
        return current_global_vector


if __name__ == "__main__":

    # XXX: Make sure all the config options have _ instead of - so they work as
    # argparse defaults without messing with 'dest'
    config = {
        'train': None,
        'test': None,
        'iterations': 1,
        'data_path': None,
        'load_weight_from': None,
        'dump_weight_to': './weight_dump',
        'dump_freq': 1,
        'parallel': False,
        'shards': 1,
        'use_hadoop': False,
        'prep_path': 'data/prep',
        'learner': 'average_perceptron',
        'parser': 'ceisner',
        'feature_generator': 'english_1st_fgen',
        'format': 'format/penn2malt.format',
        'max_sentences': None,
        'timing': False,
    }

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

        default "english_1st_fgen"; alternative "english_2nd_fgen"
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
    arg_parser.add_argument('--shards', '-s', metavar='SHARDS_NUM', type=int,
        help='train using parallelisation')
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
    arg_parser.add_argument('--dump-freq', '-f', type=int,
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
    arg_parser.add_argument('--use-hadoop', '-c', action='store_true',
        help="""Use Hadoop.""")

    # Note, we're not setting defaults here yet; we'll do that below!
    args = arg_parser.parse_args()

    if args.config:
        if not os.path.isfile(args.config):
            print("The config file doesn't exist:", args.config,
                  file=sys.stderr)
            sys.exit(1)

        config_parser = ConfigParser.RawConfigParser(config)
        config_parser.read(args.config)

        for option in ['train', 'test', 'data_path', 'prep_path', 'format']:
            config[option] = config_parser.get('data', option)

        for boolean in ['use_hadoop', 'timing', 'parallel']:
            config[boolean] = config_parser.getboolean('option', boolean)

        for int_option in ['iterations', 'dump_freq', 'shards']:
            config[int_option] = config_parser.getint('option', int_option)

        for option in ['load_weight_from', 'dump_weight_to', 'learner',
                       'feature_generator', 'parser']:
            config[option] = config_parser.get('option', option)

    # we do this here because we want the defaults to include our config file
    arg_parser.set_defaults(**config)
    args = arg_parser.parse_args()

    # we want to the CLI parameters to override the config file
    config.update(vars(args))

    learner = importlib.import_module('learn.' +
                                      config['learner']).Learner
    feature_generator = importlib.import_module('feature.' +
                                config['feature_generator']).FeatureGenerator
    parser = importlib.import_module('parse.' + config['parser']).Parser

    gp = GlmParser(config['train'],
                   config['test'],
                   data_path=config['data_path'],
                   load_weight_from=config['load_weight_from'],
                   dump_weight_to=config['dump_weight_to'],
                   learner=learner,
                   feature_generator=feature_generator,
                   parser=parser,
                   spark=config['parallel'],
                   data_format=config['format'],
                   part_data=config['prep_path'])

    training_time = None

    if config['train']:
        start_time = time.time()

        if config['parallel']:
            from pyspark import SparkContext, SparkConf
            conf = SparkConf()
            spark_context = SparkContext(conf=conf)
            parallel_learn = importlib.import_module('learn.spark_train').Learner
            gp.parallel_train(shards=config['shards'],
                              parallel_learner=parallel_learn,
                              spark_context=spark_context,
                              hadoop=config['use_hadoop'])
        else:
            gp.sequential_train()

        end_time = time.time()
        training_time = end_time - start_time
        print("Total Training Time: ", training_time)

    if config['test']:
        print("Evaluating...")
        gp.evaluate(training_time)

    if config['parallel']:
        # TODO put this in a better place...
        spark_context.stop()
