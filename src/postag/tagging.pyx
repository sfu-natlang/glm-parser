from __future__ import division
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import gzip # use compressed data files
import copy, operator, optparse
from feature import pos_fgen

def get_maxvalue(viterbi_dict):
    maxvalue = (None, None) # maxvalue has tuple (tag, value)
    for tag in viterbi_dict.keys():
        value = viterbi_dict[tag] # value is (score, backpointer)
        if maxvalue[1] is None:
            maxvalue = (tag, value[0])
        elif maxvalue[1] < value[0]:
            maxvalue = (tag, value[0])
        else:
            pass # no change to maxvalue
    if maxvalue[1] is None:
        raise ValueError("max value tag for this word is None")
    return maxvalue

def get_weight(t,u,s,pos_feat,k,feat_vec):
    weight = 0.0
    feats = []
    pos_feat.get_pos_feature(feats,k+1,t,u)
    for feat in feats:
        if (feat, s) in feat_vec:
            weight += feat_vec[feat, s]
    return weight

def perc_test(feat_vec, labeled_list, tagset, default_tag):
    output = []
    labels = copy.deepcopy(labeled_list)
    # add in the start and end buffers for the context
    labels.insert(0, '_B_-1')
    labels.insert(0, '_B_-2') # first two 'words' are B_-2 B_-1
    labels.append('_B_+1')
    labels.append('_B_+2') # last two 'words' are B_+1 B_+2
    pos_feat = pos_fgen.Pos_feat_gen(labels)
    n = len(labeled_list)
    pi = {} #stores the prob
    bp = {} #backpointer
    pi[(0,'B_-2','B_-1')] = 0;
    for k in range(1,n+1):
        if k == 1:
            # T is possible tags of second previous word in position k-2
            T = {'B_-2'}
            # U is possible tags of first previous word in position k-1
            U = {'B_-1'}
            # S is possible tags of the current word in position k
            S = tagset
        elif k == 2:
            T = {'B_-1'}
            U = tagset
            S = tagset
        else:
            T = tagset
            U = tagset
            S = tagset

        for u in U:
            for s in S:
                pi[(k, u, s)], bp[(k, u, s)] = max(((pi[(k-1, t, u)] + get_weight(t,u,s,pos_feat,k,feat_vec), t) for t in T))

# Store the tag sequence as an array
    tag = ['']*(n+1)

        # Calculate the tag sequence by following the back pointers
    prob, tag[n-1], tag[n] = max((max(((pi[(n, u, s)], u, s) for s in S)) for u in U))
    #max((max(((pi[(n, u, s)] + get_weight(u,s,'STOP',pos_feat,n+1,feat_vec), u, s) for s in S)) for u in U))
    for k in range(n-2, 0, -1):
        tag[k] = bp[(k+2, tag[k+1], tag[k+2])]
    tag = tag[1:]

        # Return the probability and tag sequence
    return tag





