# -*- coding: utf-8 -*-

#
# Part of Speech Tagger
# Simon Fraser University
# NLP Lab
#
# Author: Yulan Huang, Ziqi Wang, Anoop Sarkar, Jetic Gu
# (Please add on your name if you have authored this file)
#
# This is the main programme of the Part of Speech Tagger.
# Individual modules of the tagger are located in src/pos/

from data import data_pool
from pos import pos_decode, pos_perctrain, pos_features
from weight import weight_vector
import debug.debug
import debug.interact
import os,sys
import timeit
import time
import ConfigParser

import argparse
from ConfigParser import SafeConfigParser
from collections import defaultdict

class PosTagger():
    def __init__(self, train_regex="", test_regex="", data_path="../../penn-wsj-deps/", tag_file="tagset.txt",
                 max_iter=1,data_format="format/penn2malt.format"):
        print "TAGGER [INFO]: Loading Training Data"
        self.train_data = self.load_data(train_regex, data_path, data_format)
        print "TAGGER [INFO]: Loading Testing Data"
        self.test_data = self.load_data(test_regex, data_path, data_format)
        print "TAGGER [INFO]: Total Iteration: %d" % max_iter
        self.max_iter = max_iter
        self.default_tag = "NN"

    def load_data(self, regex, data_path, data_format):
        dp = data_pool.DataPool(regex, data_path, format_path=data_format)
        data_list =[]
        sentence_count = 0
        while dp.has_next_data():
            sentence_count+=1
            data = dp.get_next_data()
            word_list = data.column_list["FORM"]
            pos_list = data.column_list["POSTAG"]

            del word_list[0]
            del pos_list[0] # delet Root

            word_list.insert(0, '_B_-1')
            word_list.insert(0, '_B_-2') # first two 'words' are B_-2 B_-1
            word_list.append('_B_+1')
            word_list.append('_B_+2') # last two 'words' are B_+1 B_+2
            pos_list.insert(0,'B_-1')
            pos_list.insert(0,'B_-2')

            pos_feat = pos_features.Pos_feat_gen(word_list)

            gold_out_fv = defaultdict(int)
            pos_feat.get_sent_feature(gold_out_fv,pos_list)

            data_list.append((word_list,pos_list,gold_out_fv))

        print "TAGGER [INFO]: Sentence Number: %d" % sentence_count
        return data_list

    def perc_train(self, dump_data=True):
        perc = pos_perctrain.PosPerceptron(max_iter=max_iter, default_tag="NN", tag_file="tagset.txt")
        self.w_vector = perc.avg_perc_train(self.train_data)
        if dump_data:
            perc.dump_vector("fv",max_iter,self.w_vector)

    def evaluate(self, fv_path=None):
        tester = pos_decode.Decoder(self.test_data)
        if fv_path is not None:
            feat_vec = weight_vector.WeightVector()
            feat_vec.load(fv_path)
            self.w_vector = feat_vec

        acc = tester.get_accuracy(self.w_vector)

MAJOR_VERSION = 0
MINOR_VERSION = 1

if __name__ == '__main__':

    import getopt, sys

    train_regex = ''
    test_regex = ''
    max_iter = 1
    test_data_path = ''  #"./penn-wsj-deps/"
    tag_file = 'tagset.txt'
    data_format = 'format/penn2malt.format'

    arg_parser = argparse.ArgumentParser(description="""Part Of Speech (POS) Tagger
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
    arg_parser.add_argument('--path', '-p', metavar='DATA_PATH',
        help="""Path to data files (to the parent directory for all sections)
        default "./penn-wsj-deps/"
        """)
    arg_parser.add_argument('--format', metavar='DATA_FORMAT',
        help="""specify the format file for the training and testing files.
        Officially supported format files are located in src/format/
        """)
    arg_parser.add_argument('--tagset', metavar='TAG_TARGET',
        help="""specify the file containing the tags we want to use.
        Officially provided TAG_TARGET file is src/tagset.txt
        """)
    arg_parser.add_argument('--iteration', '-i', metavar='ITERATIONS', type=int,
        help="""Number of iterations
        default 1
        """)
    args=arg_parser.parse_args()
    # load configuration from file
    #   configuration files are stored under src/format/
    #   configuration files: *.format
    if args.config:
        print("TAGGER [INFO]: Reading configurations from file: %s" % (args.config))
        cf = SafeConfigParser(os.environ)
        cf.read(args.config)

        train_regex    = cf.get("data", "train")
        test_regex     = cf.get("data", "test")
        test_data_path = cf.get("data", "data_path")
        data_format    = cf.get("data", "format")
        tag_file       = cf.get("data", "tag_file")

        max_iter                             = cf.getint(    "option", "iteration")

    # load configuration from command line
    if args.path:
        test_data_path = args.path
    if args.iteration:
        max_iter = int(args.iteration)
    if args.train:
        train_regex = args.train
    if args.test:
        test_regex = args.test
    if args.format:
        data_format = args.format
    if args.tagset:
        tag_file = args.tagset

    print "TAGGER [INFO]: Training Starts, Timer is on"
    start_time = time.time()
    tagger = PosTagger(train_regex, test_regex, test_data_path, tag_file, max_iter, data_format)
    tagger.perc_train()
    end_time = time.time()
    training_time = end_time - start_time
    print "TAGGER [INFO]: Total Training Time: ", training_time

    tagger.evaluate()
