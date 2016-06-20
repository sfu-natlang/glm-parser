# This is the machine learning algorithm of the Part of Speech Tagger.
# As of right now, we are using the average perceptron to do the training.

from __future__ import division
import time,copy,logging
import os,sys,inspect
from collections import defaultdict
import pos_features, pos_viterbi, pos_common

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from feature import english_1st_fgen
from data import data_pool
from weight import weight_vector

class PosPerceptron():

    def __init__(self, w_vector=None, max_iter=1, default_tag="NN", tag_file="tagset.txt"):
        self.w_vector = w_vector
        self.max_iter = max_iter
        self.default_tag = default_tag
        self.tagset = pos_common.read_tagset(tag_file)
        print "TAGGER [DEBUG]: Trainer Loaded"

    def avg_perc_train(self, train_data):
        print "TAGGER [INFO]: Using Average Perceptron Trainer"
        if len(self.tagset) <= 0:
            raise valueError("Empty tagset")
        argmax = pos_viterbi.Viterbi()
        w_vec = defaultdict(float)
        u_vec = defaultdict(float)
        last_iter = {}
        c = 0

        for iteration in range(self.max_iter):
            print "TAGGER [INFO]: Starting Iteration %d"%iteration
            log_miss = 0

            for (word_list, pos_list, gold_out_fv) in train_data:
                print "\rTAGGER [INFO]: %d sentences trained"%c,
                output = argmax.perc_test(w_vec,word_list,self.tagset,self.default_tag)
                c += 1

                if output != pos_list:
                    log_miss += 1

                    # Initialise
                    a = defaultdict(int)
                    w_delta = defaultdict(int)

                    # Get a
                    pos_feat = pos_features.Pos_feat_gen(word_list)
                    pos_feat.get_sent_feature(a,output)

                    # Get Delta
                    for item in gold_out_fv:
                        w_delta[item] += gold_out_fv[item]
                    for item in a:
                        w_delta[item] -= a[item]

                    # Process Delta
                    for item in w_delta:
                        if w_delta[item] != 0:

                            w_vec[item] += w_delta[item]

                            if (item) in last_iter:
                                u_vec[item] += (c - last_iter[item]) * w_vec[item]
                            else:
                                u_vec[item] = w_vec[item]

                            last_iter[item] = c

            print "\rTAGGER [INFO]: Iteration completed, number of mistakes:", log_miss
        print "TAGGER [DEBUG]: Finalising"
        for item in w_vec:
            if item in last_iter:
                u_vec[item] += (c - last_iter[item]) * w_vec[item]
            else:
                u_vec[item] = w_vec[item]

            w_vec[item] = u_vec[item] / c
        print "TAGGER [DEBUG]: Training Completed"
        return w_vec

    def dump_vector(self, filename, iteration, fv):
        print "TAGGER [INFO]: Dumping weight_vec to " + filename + "_Iter_%d.db"%iteration
        w_vector = weight_vector.WeightVector()
        w_vector.iadd(fv)
        w_vector.dump(filename + "_Iter_%d.db"%iteration)

    def dump_vector_per_iter(self, filename, iteration, weight_vec, last_iter, avg_vec, num_updates):
        print "TAGGER [INFO]: Dumping weight_vec to " + filename + "_Iter_%d.db"%iteration
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
        i=i+1
        w_vector.dump(filename + "_Iter_%d.db"%iteration)
