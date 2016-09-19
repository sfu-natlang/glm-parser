# The test file is for pyspark shell debug

from pos_tagger import PosTagger
from data.file_io import fileRead, fileWrite
from data.data_pool import DataPool
from weight.weight_vector import WeightVector
from logger.loggers import logging, init_logger

from pos import pos_decode, pos_viterbi
from pos.pos_common import read_tagset

import time
import os
import sys
import importlib
import functools
import argparse
import StringIO
from ConfigParser import SafeConfigParser

init_logger('pos_tagger.log')
logger = logging.getLogger('TAGGER')
sparkContext = sc
spark_mode = True
yarn_mode = False

config = {
    'train':             "wsj_000[0-9].mrg.3.pa.gs.tab",
    'test':              "wsj_000[0-9].mrg.3.pa.gs.tab",
    'iterations':        1,
    'data_path':         "file:///Users/jetic/Daten/glm-parser-data/penn-wsj-deps/",
    'load_weight_from':  None,
    'dump_weight_to':    None,
    'dump_frequency':    1,
    'spark_shards':      4,
    'prep_path':         'file://data/prep',
    'learner':           'perceptron',
    'feature_generator': 'pos_fgen',
    'format':            'file://format/penn2malt.format',
    'tag_file':          'file://tagset.txt'
}

trainDataPool = DataPool(section_regex = config['train'],
                         data_path     = config['data_path'],
                         fgen          = config['feature_generator'],
                         format_path   = config['format'],
                         shardNum      = config['spark_shards'],
                         sc            = sparkContext,
                         hadoop        = yarn_mode)

testDataPool = DataPool(section_regex = config['test'],
                        data_path     = config['data_path'],
                        fgen          = config['feature_generator'],
                        format_path   = config['format'],
                        sc            = sparkContext,
                        hadoop        = yarn_mode)

pt = PosTagger(weightVectorLoadPath = config['load_weight_from'],
               tagFile              = config['tag_file'],
               sparkContext         = sparkContext)

pt.train(dataPool             = trainDataPool,
         maxIteration         = config['iterations'],
         learner              = config['learner'],
         weightVectorDumpPath = config['dump_weight_to'],
         dumpFrequency        = config['dump_frequency'],
         shardNum             = config['spark_shards'],
         parallel             = spark_mode,
         sparkContext         = sparkContext,
         hadoop               = yarn_mode)

pt.evaluate(dataPool      = testDataPool,
            sparkContext  = sparkContext,
            hadoop        = yarn_mode)
