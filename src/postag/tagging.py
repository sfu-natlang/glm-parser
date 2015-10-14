
from __future__ import division
import perc
import time
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from collections import defaultdict
from feature import english_1st_fgen, pos_fgen
from data.data_pool import *


def get_feats_for_word(index,fv):
    feats = [fv[index]]
    for i in range(index+1, len(fv)):
        feat = fv[i]
        if feat[0] == 0:
            index = i
            break
        feats.append(feat)
    return (index, feats)

def avg_perc_train(train_data, tagset, n):
    if len(tagset) <= 0:
        raise valueError("Empty tagset")
    default_tag = tagset[0]

    weight_vec = defaultdict(int)
    avg_vec = defaultdict(int)
    last_iter = {}

    epochs = n
    num_updates = 0
    for round in range(0,epochs):
        num_mistakes = 0
        print len(train_data)
        for (word_list, pos_list) in train_data:
            fv = []
            pos_feat = pos_fgen.Pos_feat_gen(word_list,pos_list)
            pos_feat.get_pos_feature(fv)
            if len(fv) == 0:
                raise ValueError("features do not align with input sentence")
            #TO DO: modify perc!!!!!
            output = perc.perc_test(weight_vec,word_list,fv,tagset, default_tag)
            num_updates += 1
            if output != pos_list:
                num_mistakes += 1
                feat_index = 0
                for i in range(0,len(output)):
                    (feat_index,feats) = get_feats_for_word(feat_index,fv)
                    feat_vec_update = defaultdict(int)
                    for feat in feats:
                        output_feat = true_feat = feat
                        feat_vec_update[output_feat,output[i]] += -1
                        feat_vec_update[true_feat,pos_list[i]] += 1
                    for (upd_feat, upd_tag) in feat_vec_update:
                        if feat_vec_update[upd_feat, upd_tag] != 0:
                            weight_vec[upd_feat, upd_tag] += feat_vec_update[upd_feat,upd_tag]
                            if (upd_feat, upd_tag) in last_iter:
                                avg_vec[upd_feat, upd_tag] += (num_updates - last_iter[upd_feat, upd_tag]) * weight_vec[upd_feat, upd_tag]
                            else:
                                avg_vec[upd_feat, upd_tag] = weight_vec[upd_feat, upd_tag]
                            last_iter[upd_feat, upd_tag] = num_updates
        print >>sys.stderr, "number of mistakes:", num_mistakes
    for (feat, tag) in weight_vec:
        if (feat, tag) in last_iter:
            avg_vec[feat, tag] += (num_updates - last_iter[feat, tag]) * weight_vec[feat, tag]
        else:
            avg_vec[feat, tag] = weight_vec[feat, tag]
        weight_vec[feat, tag] = avg_vec[feat, tag] / num_updates
    return weight_vec

def sent_evaluate(result_list, gold_list):
    if isinstance(result_list, list):
        result_set = set(result_list)
    if isinstance(gold_list, list):
        gold_set = set(gold_list)
    intersect_set = result_set.intersection(gold_set)
    correct_num = len(intersect_set)
    gold_set_size = len(gold_set)   
    return correct_num, gold_set_size

def result_evaluate(unlabeled_correct_num,unlabeled_gold_set_size,correct_num, gold_set_size):
    unlabeled_correct_num += correct_num
    unlabeled_gold_set_size += gold_set_size
    return unlabeled_correct_num, unlabeled_gold_set_size

if __name__ == '__main__':
    unlabeled_correct_num = 0
    unlabeled_gold_set_size = 0
    # each element in the feat_vec dictionary is:
    # key=feature_id value=weight
    feat_vec = {}
    tagset = ['ROOT','CC','CD','DT','EX','FW','IN','JJ','JJR','JJS','LS','MD','NN','NNS','NNP','NNPS','PDT','POS',
    'PRP','PRP$','RB','RBR','RBS','RP','SYM','TO','UH','VB','VBD','VBG','VBN','VBP','VBZ','WDT','WP','WP$','WRB','.',',',':','(',')']
    train_data = []
    #data_path = "/Users/vivian/data/penn-wsj-deps/"
    data_path = sys.argv[1]
    numepochs = sys.argv[2]
    fgen = english_1st_fgen.FirstOrderFeatureGenerator
    data_pool = DataPool([(2,21)], data_path,fgen)
    sentence_count = 1
    print "loading data..."
    while data_pool.has_next_data():
        print("Sentence %d" % sentence_count)
        sentence_count+=1
        data = data_pool.get_next_data()
        train_data.append((data.word_list,data.pos_list))
    print "perceptron training..."
    start = time.time()
    feat_vec = avg_perc_train(train_data, tagset, numepochs)
    print time.time()-start
    test_data = []
    data_pool = DataPool([0,1,22,24], data_path,fgen)
    while data_pool.has_next_data():
        data = data_pool.get_next_data()
        test_data.append((data.word_list,data.pos_list))
    print "testing"
    for (word_list, pos_list) in test_data:
    #generate features for thee word list...      
        fv = []
        pos_feat = pos_fgen.Pos_feat_gen(word_list,pos_list)
        pos_feat.get_pos_feature(fv)
        output = perc.perc_test(feat_vec,word_list,fv,tagset,tagset[0])
        #print word_list, " ", len(word_list)
        #print output, " ", len(output)
        #print pos_list, " ", len(pos_list)
        cnum, gnum = sent_evaluate(output,pos_list)
        unlabeled_correct_num, unlabeled_gold_set_size=result_evaluate(unlabeled_correct_num,unlabeled_gold_set_size,cnum,gnum)
        #print "accuraccy:%d, %d" %(unlabeled_correct_num,unlabeled_gold_set_size)
    acc = unlabeled_correct_num /unlabeled_gold_set_size
    print "whole accraccy: ", acc

        




