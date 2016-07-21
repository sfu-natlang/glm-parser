# This is the machine learning algorithm of the Part of Speech Tagger.
# As of right now, we are using the average perceptron to do the training.

from __future__ import division
import time
import copy
import os
import sys
import inspect
import logging

import pos_viterbi
import pos_common

from data import data_pool
from weight.weight_vector import WeightVector

gottenFile = inspect.getfile(inspect.currentframe())
currentdir = os.path.dirname(os.path.abspath(gottenFile))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

logger = logging.getLogger('LEARNER')


def tagger_f_argmax(w_vector, sentence, tagset, default_tag):
    tagger = pos_viterbi.Viterbi()
    output = tagger.tag(sentence    = sentence,
                        w_vector    = w_vector,
                        tagset      = tagset,
                        default_tag = default_tag)
    print output
    print sentence.get_pos_list()
    current_global_vector = sentence.get_local_vector(poslist=output)
    return current_global_vector


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

    def sequential_learn(self, data_pool):
        import functools
        f_argmax = functools.partial(tagger_f_argmax,
                                     tagset=self.tagset,
                                     default_tag=self.default_tag)

        logger.info("Using Average Perceptron Trainer")
        if len(self.tagset) <= 0:
            raise valueError("LEARNER [ERRO]: Empty tagset")
        argmax = pos_viterbi.Viterbi()
        w_vec = WeightVector()
        u_vec = WeightVector()
        data_size = len(data_pool.data_list)
        last_iter = {}
        c = 0

        for iteration in range(self.max_iter):
            logger.debug("Iteration %d" % iteration)
            sentence_count = 1
            log_miss = 0

            while data_pool.has_next_data():
                sentence = data_pool.get_next_data()

                gold_vector = sentence.gold_global_vector

                logger.info("Iteration %d, Sentence %d of %d, Length %d" % (
                    iteration,
                    c,
                    data_size,
                    len(sentence.get_word_list()) - 1))
                sentence_count += 1

                c += 1

                current_vector = f_argmax(w_vec, sentence)

                if current_vector != gold_vector:
                    log_miss += 1

                    # Get Delta
                    delta_vector = gold_vector - current_vector

                    # Process Delta
                    for i in delta_vector.keys():
                        if delta_vector[i] != 0:

                            w_vec[i] += delta_vector[i]

                            if (i) in last_iter:
                                u_vec[i] += (c - last_iter[i]) * w_vec[i]
                            else:
                                u_vec[i] = w_vec[i]

                            last_iter[i] = c

            logger.info("Iteration completed, number of mistakes: " + str(log_miss))
            data_pool.reset_index()

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
        logger.info("Dumping weight_vec to ", filename,
                    "_Iter_%d.db" % iteration)
        w_vector = WeightVector()
        w_vector.iadd(fv)
        w_vector.dump("file://" + filename + "_Iter_%d.db" % (iteration))

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

        w_vector = WeightVector()
        w_vector.iadd(fv)
        i = i + 1
        w_vector.dump("file://" + filename + "_Iter_%d.db" % iteration)
