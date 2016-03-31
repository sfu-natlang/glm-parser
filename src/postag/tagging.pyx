from __future__ import division
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import gzip # use compressed data files
import copy, operator, optparse
from feature import pos_fgen
from collections import defaultdict

def get_maxvalue(viterbi_dict):
    maxvalue = ((None,None), None) # maxvalue has tuple (tag, pre_tag, value)
    for tag in viterbi_dict.keys():
        for pre_tag in viterbi_dict[tag]:
            value = viterbi_dict[tag][pre_tag] # value is (score, backpointer)
            if maxvalue[1] is None:
                maxvalue = ((tag,pre_tag), value[0])
            elif maxvalue[1] < value[0]:
                maxvalue = ((tag,pre_tag), value[0])
            else:
                pass # no change to maxvalue
    if maxvalue[1] is None:
        raise ValueError("max value tag for this word is None")
    return maxvalue


def perc_test(feat_vec, labeled_list, tagset, default_tag):
    output = []
    labels = copy.deepcopy(labeled_list)
    # add in the start and end buffers for the context
    labels.insert(0,'_B_0')
    labels.insert(0, '_B_-1')
    labels.insert(0, '_B_-2') # first two 'words' are B_-2 B_-1
    labels.append('_B_+1')
    labels.append('_B_+2') # last two 'words' are B_+1 B_+2

    # size of the viterbi data structure
    N = len(labels)

    # Set up the data structure for viterbi search
    viterbi = {}
    for i in range(0, N):
        viterbi[i] = defaultdict(lambda: {}) 

    # We do not tag the first two and last two words
    # since we added B_-2, B_-1, B_+1 and B_+2 as buffer words 
    viterbi[0]['B_-2'][''] = (0.0, '','')
    viterbi[1]['B_-1']['B_-2'] = (0.0, 'B_-2','')
    viterbi[2]['B_0']['B_-1'] = (0.0,'B_-1','B_-2')
    # find the value of best_tag for each word i in the input
    # feat_index = 0
    pos_feat = pos_fgen.Pos_feat_gen(labels)
    for i in range(3, N-2):
        word = labels[i]
        found_tag = False
        for tag in tagset:
            prev_list = []
            for prev_tag_a in viterbi[i-1]:
                for prev_tag_b in viterbi[i-1][prev_tag_a]:
                    feats = []
                    (prev_value, prev_tag_b,prev_tag_c) = viterbi[i-1][prev_tag_a][prev_tag_b]
                    pos_feat.get_pos_feature(feats,i,prev_tag_a,prev_tag_b,prev_tag_c)
                    weight = 0.0
                    # sum up the weights for all features
                    for feat in feats:
                        if (feat, tag) in feat_vec:
                            weight += feat_vec[feat, tag]
                    prev_list.append((weight + prev_value, prev_tag_a, prev_tag_b) )
            (best_weight, backpointer_a, backpointer_b) = sorted(prev_list, key=operator.itemgetter(0), reverse=True)[0]
            #print >>sys.stderr, "best_weight:", best_weight, "backpointer_a:", backpointer_a, " ",backpointer_b
            if best_weight != 0.0:
                viterbi[i][tag][backpointer_a] = (best_weight, backpointer_a, backpointer_b)
                found_tag = True
        if found_tag is False:
            viterbi[i][default_tag][default_tag] = (0.0, default_tag,default_tag)


    # recover the best sequence using backpointers
    maxvalue = get_maxvalue(viterbi[N-3])
    best_tag,prev_tag_a = maxvalue[0]
    for i in range(N-3, 2, -1):
        output.insert(0,best_tag)
        (value, prev_tag_a, prev_tag_b) = viterbi[i][best_tag][prev_tag_a]
        best_tag = prev_tag_a
        prev_tag_a = prev_tag_b

    return output

