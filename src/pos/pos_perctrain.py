# This is the machine learning algorithm of the Part of Speech Tagger.
# As of right now, we are using the average perceptron to do the training.

from __future__ import division
import time
import copy
import os
import sys
import inspect
import logging
from collections import defaultdict

import pos_features
import pos_viterbi
import pos_common

from feature import english_1st_fgen
from data import data_pool
from weight import weight_vector

gottenFile = inspect.getfile(inspect.currentframe())
currentdir = os.path.dirname(os.path.abspath(gottenFile))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

logger = logging.getLogger('LEARNER')


class PosPerceptron():

    def __init__(self,
                 w_vector=None,
                 max_iter=1,
                 default_tag="NN",
                 tag_file="tagset.txt",
                 sparkContext=None):

        self.w_vector = w_vector
        self.max_iter = max_iter
        self.default_tag = default_tag
        self.sparkContext = sparkContext
        self.tagset = pos_common.read_tagset(tag_file, self.sparkContext)
        logger.debug("Trainer Loaded")

    def avg_perc_train(self, train_data):
        logger.info("Using Average Perceptron Trainer")
        if len(self.tagset) <= 0:
            raise valueError("LEARNER [ERRO]: Empty tagset")
        argmax = pos_viterbi.Viterbi()
        w_vec = defaultdict(float)
        u_vec = defaultdict(float)
        data_size = len(train_data)
        last_iter = {}
        c = 0

        for iteration in range(self.max_iter):
            logger.info("Starting Iteration %d" % iteration)
            log_miss = 0

            for (word_list, pos_list, gold_out_fv) in train_data:
                logger.info("Iteration %d, Sentence %d of %d, Length %d" % (
                    iteration,
                    c,
                    data_size,
                    len(word_list) - 1))
                c += 1

                output = argmax.perc_test(w_vec,
                                          word_list,
                                          self.tagset,
                                          self.default_tag)

                if output != pos_list:
                    log_miss += 1

                    # Initialise
                    a = defaultdict(int)
                    w_delta = defaultdict(int)

                    # Get a
                    pos_feat = pos_features.Pos_feat_gen(word_list)
                    pos_feat.get_sent_feature(a, output)

                    # Get Delta
                    for i in gold_out_fv:
                        w_delta[i] += gold_out_fv[i]
                    for i in a:
                        w_delta[i] -= a[i]

                    # Process Delta
                    for i in w_delta:
                        if w_delta[i] != 0:

                            w_vec[i] += w_delta[i]

                            if (i) in last_iter:
                                u_vec[i] += (c - last_iter[i]) * w_vec[i]
                            else:
                                u_vec[i] = w_vec[i]

                            last_iter[i] = c

            logger.info("Iteration completed, number of mistakes: %d"
                        % log_miss)
        logger.debug("Finalising")
        for i in w_vec:
            if i in last_iter:
                u_vec[i] += (c - last_iter[i]) * w_vec[i]
            else:
                u_vec[i] = w_vec[i]

            w_vec[i] = u_vec[i] / c
        logger.debug("Training Completed")
        return w_vec

    def dump_vector(self, filename, iteration, fv):
        logger.info("Dumping weight_vec to %s_Iter_%d.db"
                    % (filename, iteration))
        w_vector = weight_vector.WeightVector()
        w_vector.iadd(fv)
        w_vector.dump("file://" + filename + "_Iter_%d.db" % iteration)

    def dump_vector_per_iter(self,
                             filename,
                             iteration,
                             weight_vec,
                             last_iter,
                             avg_vec,
                             num_updates):

        logger.info("Dumping weight_vec to ", filename,
                    "_Iter_%d.db" % iteration)
        fv = copy.deepcopy(weight_vec)
        av = copy.deepcopy(avg_vec)
        for feat in fv:
            if feat in last_iter:
                av[feat] += (num_updates - last_iter[feat]) * fv[feat]
            else:
                av[feat] = fv[feat]
            fv[feat] = av[feat] / num_updates

        w_vector = weight_vector.WeightVector()
        w_vector.iadd(fv)
        i = i + 1
        w_vector.dump("file://" + filename + "_Iter_%d.db" % iteration)
