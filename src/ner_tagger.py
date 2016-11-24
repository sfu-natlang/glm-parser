# -*- coding: utf-8 -*-

#
# Named Entity Recogniser
# Simon Fraser University
# NLP Lab
#
# This is the main programme of the Named Entity Recogniser
#
import debug.debug
from data.file_io import fileRead, fileWrite
from data.data_pool import DataPool
from weight.weight_vector import WeightVector
from logger.loggers import logging, init_logger
from feature.feature_vector import FeatureVector

from evaluate.tagger_evaluator import Evaluator
from data.pos_tagset_reader import read_tagset

import time
import os
import sys
import importlib
import functools
import argparse
import StringIO
from ConfigParser import SafeConfigParser

from ner import ner_decode, ner_perctrain, ner_features
from collections import defaultdict

__version__ = '1.0'
if __name__ == '__main__':
    init_logger('ner_tagger.log')
logger = logging.getLogger('NER')


class NerTagger():

    # def __init__(self,
    #              tagFile        = "file://ner_tagset.txt",
    #              sparkContext   = None):
    def __init__(self,
                 weightVectorLoadPath = None,
                 tagger               = "ner_viterbi",
                 tagFile              = "file://ner_tagset.txt",
                 sparkContext         = None):

        logger.info("Initialising NER Tagger")
        # - self.tagFile = tagFile
        self.w_vector = WeightVector(weightVectorLoadPath, sparkContext)
        self.evaluator = Evaluator

        self.tagger = importlib.import_module('ner.' + tagger).Tagger()
        logger.info("Using tagger: %s" % (tagger))

        self.tagFile = read_tagset(tagFile, sparkContext)
        logger.info("Tag File selected: %s" % tagFile)
        self.default_tag = "O"
        logger.info("Initialisation Complete")
        return

    def loading_data(self, data_file):
    # def loading_data(self,
    #                  dataPool,
    #                  maxIteration           = 1,
    #                  learner                = 'average_perceptron',
    #                  weightVectorDumpPath   = None,
    #                  dumpFrequency          = 1,
    #                  parallel               = False,
    #                  sparkContext           = None,
    #                  hadoop                 = False):
        # function to load the training and testing data
        f = fileRead(data_file)
        sentence = []
        sentence_count = 0
        tags = []
        pos_tag = []
        chunking_tag = []
        data_list = []
        for line in f:
            line = line.strip()
            if line:
                # Non-empty line
                token = line.split()
                word = token[0]
                tag  = token[3]
                p_tag = token[1]
                # holds the pos tag
                ch_tag = token[2]
                # holds the chunking tag
                # appends the word at the end of the list
                sentence.append(word)
                # appends the tag at the end of the list
                tags.append(tag)
                pos_tag.append(p_tag)
                chunking_tag.append(ch_tag)
            else:
                # End of sentence reached
                # converts the sentence list to a tuple and then appends that tuple to the end of the self.x list
                sentence.insert(0, '_B_-1')
                sentence.insert(0, '_B_-2')
                sentence.append('_B_+1')
                sentence.append('_B_+2')  # last two 'words' are B_+1 B_+2
                tags.insert(0, 'B_-1')
                tags.insert(0, 'B_-2')
                tags.append('B_+1')
                tags.append('B_+2')
                pos_tag.insert(0, 'B_-1')
                pos_tag.insert(0, 'B_-2')
                pos_tag.append('B_+1')
                pos_tag.append('B_+2')
                chunking_tag.insert(0, 'B_-1')
                chunking_tag.insert(0, 'B_-2')
                chunking_tag.append('B_+1')
                chunking_tag.append('B_+2')

                ner_feat = ner_features.Ner_feat_gen(sentence)
                gold_out_fv = defaultdict(int)
                # getiing the gold features for the sentence
                ner_feat.get_sent_feature(gold_out_fv, tags, pos_tag, chunking_tag)

                data_list.append((sentence, pos_tag, chunking_tag, tags, gold_out_fv))
                sentence = []
                tags = []
                pos_tag = []
                chunking_tag = []
                sentence_count += 1

        logger.info("Total sentence Number: %d" % sentence_count)
        return data_list

    def load_data(self, brown_file):
        # function to load the brown clusters
        f = fileRead(brown_file)
        data_list = []
        for line in f:
            line = line.strip()
            if line:
                # Non-empty line
                data_list.append(line)
        return data_list

    # def train(self,
    #           train_data   = "/cs/natlang-data/CoNLL/CoNLL-2003/eng.train",
    #           maxIteration = 10,
    #           learner      = 'average_perceptron',
    #           dump_data    = True):
    def train(self,
                     dataPool,
                     maxIteration           = 1,
                     learner                = 'average_perceptron',
                     weightVectorDumpPath   = None,
                     dumpFrequency          = 1,
                     parallel               = False,
                     sparkContext           = None,
                     hadoop                 = False):

        # logger.info("Loading training data")
        # self.train_data_file = train_data
        # self.train_data = self.loading_data(self.train_data_file)
        # logger.info("Training data loaded")
        if not isinstance(dataPool, DataPool):
            raise ValueError("NER_TAGGER [ERROR]: dataPool for training is not an DataPool object")
        if maxIteration is None:
            logger.warn("Number of Iterations not specified, using 1")
            maxIteration = 1
        if learner is None:
            raise ValueError("NER_TAGGER [ERROR]: Learner not specified")

        # Load Learner
        learner = importlib.import_module('learner.' + learner).Learner(self.w_vector)

        # Prepare suitable argmax as PosTagger 80-90
        def tagger_f_argmax(w_vector, sentence, tagger, tagset, default_tag):
            output = tagger.tag(sentence    = sentence,
                                w_vector    = w_vector,
                                tagset      = tagset,
                                default_tag = default_tag)
            current_global_vector = FeatureVector(sentence.get_local_vector(poslist=output))
            return current_global_vector
        f_argmax = functools.partial(tagger_f_max,
                                     tagger      = self.tagger,
                                     tagset      = self.tagset,
                                     default_tag = self.default_tag)

        # function to call the average perceptron algorithm implemented in another file
        # perc = ner_perctrain.NerPerceptron(max_iter    = maxIteration,
        #                                    default_tag = "O",
        #                                    tag_file    = self.tagFile)
        # Start Training Process
        logger.info("Starting Training Process")
        start_time = time.time()
        # if learner == 'average_perceptron':
        #     self.w_vector = perc.avg_perc_train(self.train_data)
        # else:
        #     self.w_vector = perc.perc_train(self.train_data)
        if not parallel:
            # Sequential Training
            self.w_vector = learner.sequential_learn(
                f_argmax    = f_argmax,
                data_pool   = dataPool,
                iterations  = maxIteration,
                d_filename  = weightVectorDumpPath,
                dump_freq   = dumpFrequency
            )
        else:
            # parallel
            self.w_vector = learner.parallel_learn(
                f_argmax     = f_argmax,
                data_pool    = dataPool,
                iterations   = maxIteration,
                d_filename   = weightVectorDumpPath,
                dump_freq    = dumpFrequency,
                sparkContext = sparkContext,
                hadoop       = hadoop
            )

        end_time = time.time()
        logger.info("Total Training Time(seconds): %f" % (end_time - start_time,))

        # if dump_data:
        #     perc.dump_vector("file://NER", maxIteration, self.w_vector)
        return

    # def evaluate(self,
    #              test_data="/cs/natlang-data/CoNLL/CoNLL-2003/eng.testa",
    #              fv_path=None):
    def evaluate(self,
                 dataPool,
                 parallel       = False,
                 sparkContext   = None,
                 hadoop         = None):

        logger.info("Starting evaluation process")
        # logger.info("Loading evaluation data")
        # self.test_data_file = test_data
        # self.test_data = self.loading_data(self.test_data_file)
        # logger.info("Evaluation data loaded")
        if not isinstance(dataPool, DataPool):
            raise ValueError("NER_TAGGER [ERROR]: dataPool for evaluation is not an DataPool object")

        start_time = time.time()
        # function to calulate the accuracy
        # tester = ner_decode.Decoder(self.test_data)
        evaluator = self.evaluator(self.tagger, self.tagset)
        # if fv_path is not None:
        #     feat_vec = weight_vector.WeightVector()
        #     feat_vec.load(fv_path)
        #     self.w_vector = feat_vec
        #
        # acc = tester.get_accuracy(self.w_vector)

        if not parallel:
            evaluator.sequentialEvaluate(
                data_pool       = dataPool,
                w_vector        = self.w_vector,
                sparkContext    = sparkContext,
                hadoop          = hadoop)
        else:
            evaluator.parallelEvaluate(
                data_pool       = dataPool,
                w_vector        = self.w_vector,
                sparkContext    = sparkContext,
                hadoop          = hadoop)

        end_time = time.time()
        logger.info("Total evaluation Time(seconds): %f" % (end_time - start_time,))

# Is it necessary to add getTags function given Pos_Tagger used it?

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
        'format':            'format/penn2malt.format',
        'tag_file':          None
    }

    # Dealing with arguments here
    if True:  # Adding arguments
        arg_parser = argparse.ArgumentParser(
            description="""Name Entity Recognition (NER) Tagger
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
        arg_parser.add_argument('--spark-shards', '-s', metavar='SHARDS_NUM',
            type=int, help='train using parallelisation with spark')
        arg_parser.add_argument('--data-path', '-p', metavar='DATA_PATH',
            help="""Path to data files (to the parent directory for all sections)
            """)
        arg_parser.add_argument('--iterations', '-i', metavar='ITERATIONS',
            type=int, help="""Number of iterations, default is 1""")
        arg_parser.add_argument('--hadoop', '-c', action='store_true',
            help="""Using POS Tagger in Spark Yarn Mode""")
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
        for option in ['train', 'test', 'tag_file']:
            if config_parser.get('data', option) != '':
                config[option] = config_parser.get('data', option)

        for int_option in ['iterations', 'spark_shards']:
            if config_parser.get('option', int_option) != '':
                config[int_option] = config_parser.getint('option', int_option)

        for option in ['learner']:
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
                'tag_file']:
            if config[option] is not None:
                if (not config[option].startswith("file://")) and \
                        (not config[option].startswith("hdfs://")):
                    config[option] = 'file://' + config[option]

    # Initialise Tagger
    nt = NerTagger(tagFile=config['tag_file'])

    # Run training
    if config['train']:
        nt.train(train_data   = config['data_path'] + config['train'],
                 maxIteration = config['iterations'],
                 learner      = config['learner'])

    # Run evaluation
    if config['test']:
        nt.evaluate(test_data=config['data_path'] + config['test'])

    # Finalising, shutting down spark
    if spark_mode:
        sparkContext.stop()
