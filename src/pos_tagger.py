# -*- coding: utf-8 -*-
#
# Part of Speech Tagger
# Simon Fraser University
# NLP Lab
#
# Author: Yulan Huang, Ziqi Wang, Anoop Sarkar, Jetic Gu, Kingston Chen,
# (Please add on your name if you have authored this file)
#
# This is the main programme of the Part of Speech Tagger.
# Individual modules of the tagger are located in src/pos/

from data.data_pool import DataPool
from pos import pos_decode, pos_perctrain, pos_features, pos_viterbi
from weight.weight_vector import WeightVector
from pos.pos_common import read_tagset
from logger.loggers import logging, init_logger

import debug.debug
import os
import sys
import timeit
import time
import argparse
from ConfigParser import SafeConfigParser
from collections import defaultdict

__version__ = '1.0'
if __name__ == '__main__':
    init_logger('pos_tagger.log')
logger = logging.getLogger('TAGGER')


class PosTagger():
    def __init__(self,
                 weightVectorLoadPath = None,
                 tag_file             = "file://tagset.txt",
                 sparkContext         = None):

        logger.info("Tag File selected: %s" % tag_file)
        self.tagset = read_tagset(tag_file, sparkContext)
        self.default_tag = "NN"
        self.sparkContext = sparkContext
        if weightVectorLoadPath is not None:
            self.w_vector = WeightVector()
            self.w_vector.load(weightVectorLoadPath, self.sparkContext)

    def load_data(self, dataPool):
        data_list = []
        sentence_count = 0
        while dataPool.has_next_data():
            sentence_count += 1
            data = dataPool.get_next_data()
            word_list = data.column_list["FORM"]
            pos_list = data.column_list["POSTAG"]

            del word_list[0]
            del pos_list[0]  # delet Root

            word_list.insert(0, '_B_-1')
            word_list.insert(0, '_B_-2')  # first two 'words' are B_-2 B_-1
            word_list.append('_B_+1')
            word_list.append('_B_+2')     # last two 'words' are B_+1 B_+2
            pos_list.insert(0, 'B_-1')
            pos_list.insert(0, 'B_-2')

            pos_feat = pos_features.Pos_feat_gen(word_list)

            gold_out_fv = defaultdict(int)
            pos_feat.get_sent_feature(gold_out_fv, pos_list)

            data_list.append((word_list, pos_list, gold_out_fv))

        logger.info("Sentence Number: %d" % sentence_count)
        return data_list

    def perc_train(self,
                   dataPool=None,
                   max_iter=1,
                   dump_data=True):

        logger.info("Loading Training Data")
        if dataPool is None:
            logger.error('Training DataPool not specified\n')
            sys.exit(1)
        train_data = self.load_data(dataPool)

        logger.info("Training with Iterations: %d" % max_iter)
        perc = pos_perctrain.PosPerceptron(max_iter=max_iter,
                                           default_tag="NN",
                                           tag_file="file://tagset.txt",
                                           sparkContext=self.sparkContext)

        self.w_vector = perc.avg_perc_train(train_data)
        if dump_data:
            logger.info("Dumping trained weight vector")
            perc.dump_vector("fv", max_iter, self.w_vector)
        return self.w_vector

    def evaluate(self, dataPool=None):
        if dataPool is None:
            logger.error('Training DataPool not specified\n')
            sys.exit(1)

        logger.info("Loading Testing Data")
        test_data = self.load_data(dataPool)
        tester = pos_decode.Decoder(test_data)
        acc = tester.get_accuracy(self.w_vector)

    def getTags(self, word_list):
        argmax = pos_viterbi.Viterbi()
        pos_list = argmax.perc_test(self.w_vector, word_list, self.tagset, "NN")
        return pos_list[2:]

if __name__ == '__main__':
    __logger = logging.getLogger('MAIN')
    # Process Defaults
    config = {
        'train':           None,
        'test':            None,
        'iterations':      1,
        'data_path':       None,
        'tag_file':        None,
        'format':          'format/penn2malt.format',
        'tagger_w_vector': None
    }

    arg_parser = argparse.ArgumentParser(description="""Part Of Speech (POS) Tagger
        Version %s""" % __version__)
    arg_parser.add_argument('config', metavar='CONFIG_FILE', nargs='?', help="""
        specify the config file. This will load all the setting from the config
        file, in order to avoid massive command line inputs. Please consider
        using config files instead of manually typing all the options.

        Additional options by command line will override the settings in the
        config file.

        Officially provided config files are located in src/config/
        """)
    arg_parser.add_argument('--train', metavar='TRAIN_REGEX', help="""
        specify the data for training with regular expression
        """)
    arg_parser.add_argument('--test', metavar='TEST_REGEX', help="""
        specify the data for testing with regular expression
        """)
    arg_parser.add_argument('--path', '-p', metavar='DATA_PATH', help="""
        Path to data files (to the parent directory for all sections)
        default "./penn-wsj-deps/"
        """)
    arg_parser.add_argument('--format', metavar='DATA_FORMAT', help="""
        specify the format file for the training and testing files.
        Officially supported format files are located in src/format/
        """)
    arg_parser.add_argument('--tag-file', metavar='TAG_TARGET', help="""
        specify the file containing the tags we want to use.
        Officially provided TAG_TARGET file is src/tagset.txt
        """)
    arg_parser.add_argument(
        '--iterations', '-i',
        metavar='ITERATIONS', type=int, help="""
        Number of iterations
        default 1
        """)
    arg_parser.add_argument('--tagger-w-vector', metavar='FILENAME',
        help="""Path to an existing w-vector for tagger. Use this option if
        you need to evaluate the glm_parser with a trained tagger.
        """)

    args = arg_parser.parse_args()
    # load configuration from file
    #   configuration files are stored under src/format/
    #   configuration files: *.format
    if args.config:
        __logger.info("Reading configurations from file: " + args.config)
        cf = SafeConfigParser(os.environ)
        cf.read(args.config)

        for option in ['train', 'test', 'data_path', 'tag_file', 'format']:
            if cf.get('data', option) != '':
                config[option] = cf.get('data', option)

        if cf.get('option', 'iterations') != '':
            config['iterations'] = cf.getint("option", "iterations")

        if cf.get('option', 'tagger_w_vector') != '':
            config['tagger_w_vector'] = cf.get('option', 'tagger_w_vector')

    # we do this here because we want the defaults to include our config file
    arg_parser.set_defaults(**config)
    args = arg_parser.parse_args()

    # we want to the CLI parameters to override the config file
    config.update(vars(args))

    yarn_mode = False

    # Check values of config[]
    if config['data_path'] is None:
        __logger.error('data_path not specified\n')
        sys.exit(1)
    if (not os.path.isdir(config['data_path'])) and (not yarn_mode):
        __logger.error("The data_path directory doesn't exist: %s\n" % config['data_path'])
        sys.exit(1)
    if (not os.path.isfile(config['format'])) and (not yarn_mode):
        __logger.error("The format file doesn't exist: %s\n" % config['format'])
        sys.exit(1)

    if not yarn_mode:
        for option in [
                'data_path',
                'format',
                'tagger_w_vector',
                'tag_file']:
            if config[option] is not None:
                if (not config[option].startswith("file://")) and \
                        (not config[option].startswith("hdfs://")):
                    config[option] = 'file://' + config[option]

    tagger = PosTagger(weightVectorLoadPath=config['tagger_w_vector'], tag_file=config['tag_file'])

    if config['train']:
        trainDataPool = DataPool(section_regex = config['train'],
                                 data_path     = config['data_path'],
                                 format_path   = config['format'])

        __logger.info("Training Starts, Timer is on")
        start_time = time.time()
        tagger.perc_train(dataPool = trainDataPool,
                          max_iter = config['iterations'])
        end_time = time.time()
        training_time = end_time - start_time
        __logger.info("Total Training Time: %f" % training_time)

    if config['test']:
        testDataPool = DataPool(section_regex = config['test'],
                                data_path     = config['data_path'],
                                format_path   = config['format'])
        tagger.evaluate(dataPool=testDataPool)
