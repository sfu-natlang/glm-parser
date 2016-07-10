from __future__ import division
import os
import sys
import inspect
import copy
import operator
import optparse
import pos_features
from collections import defaultdict

gottenFile = inspect.getfile(inspect.currentframe())
currentdir = os.path.dirname(os.path.abspath(gottenFile))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


class Viterbi():
    def __init__(self, w_vector=None):
        self.w_vector = w_vector

    def get_maxvalue(self, viterbi_dict):
        maxvalue = (None, None)  # maxvalue has tuple (tag, value)
        for tag in viterbi_dict.keys():
            value = viterbi_dict[tag]  # value is (score, backpointer)
            if maxvalue[1] is None:
                maxvalue = (tag, value[0])
            elif maxvalue[1] < value[0]:
                maxvalue = (tag, value[0])
            else:
                pass  # no change to maxvalue
        if maxvalue[1] is None:
            raise ValueError("max value tag for this word is None")
        return maxvalue

    def perc_test(self, feat_vec, labeled_list, tagset, default_tag):
        output = []

        # size of the viterbi data structure
        N = len(labeled_list)

        # Set up the data structure for viterbi search
        viterbi = {}
        for i in range(0, N):
            viterbi[i] = {}
            # each column contains for each tag: a (value, backpointer) tuple

        # We do not tag the first two and last two words
        # since we added B_-2, B_-1, B_+1 and B_+2 as buffer words
        viterbi[0]['B_-2'] = (0.0, '')
        viterbi[1]['B_-1'] = (0.0, 'B_-2')
        # find the value of best_tag for each word i in the input
        # feat_index = 0
        pos_feat = pos_features.Pos_feat_gen(labeled_list)
        for i in range(2, N-2):
            word = labeled_list[i]
            found_tag = False
            for tag in tagset:
                prev_list = []
                for prev_tag in viterbi[i-1]:
                    feats = []
                    (prev_value, prev_backpointer) = viterbi[i-1][prev_tag]
                    pos_feat.get_pos_feature(feats,
                                             i,
                                             prev_tag,
                                             prev_backpointer)
                    weight = 0.0
                    # sum up the weights for all features except the bigram
                    # features
                    for feat in feats:
                        if (feat, tag) in feat_vec:
                            weight += feat_vec[feat, tag]
                    prev_tag_weight = weight
                    prev_list.append((prev_tag_weight + prev_value, prev_tag))
                (best_weight, backpointer) = sorted(prev_list,
                                                    key=operator.itemgetter(0),
                                                    reverse=True)[0]
                if best_weight != 0.0:
                    viterbi[i][tag] = (best_weight, backpointer)
                    found_tag = True
            if found_tag is False:
                viterbi[i][default_tag] = (0.0, default_tag)

        # recover the best sequence using backpointers
        maxvalue = self.get_maxvalue(viterbi[N-3])
        best_tag = maxvalue[0]
        for i in range(N-3, 1, -1):
            output.insert(0, best_tag)
            (value, backpointer) = viterbi[i][best_tag]
            best_tag = backpointer

        output.insert(0, 'B_-1')
        output.insert(0, 'B_-2')
        return output
