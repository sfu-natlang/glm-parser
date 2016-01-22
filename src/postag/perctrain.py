
from __future__ import division
import tagging
import time
import copy
import logging
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from collections import defaultdict
from feature import english_1st_fgen, pos_fgen
from data import data_pool
from hvector._mycollections import mydefaultdict
from hvector.mydouble import mydouble
from weight import weight_vector

logging.basicConfig(filename='glm_tagging.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
# read the valid output tags for the task
def read_tagset(tagsetfile):
    tagset = []
    for line in open(tagsetfile, 'r'):
        line = line.strip()
        tagset.append(line)
    return tagset

def avg_perc_train(train_data, tagset, epochs):
    if len(tagset) <= 0:
        raise valueError("Empty tagset")
    default_tag = tagset[0]
    weight_vec = mydefaultdict(mydouble)
    avg_vec = mydefaultdict(mydouble)
    last_iter = {}
    num_updates = 0
    for round in range(0,epochs):
        num_mistakes = 0
        trian_sent = 0
        for (word_list, pos_list) in train_data:
            output = tagging.perc_test(weight_vec,word_list,tagset,default_tag)
            num_updates += 1
            if output != pos_list:
                
                num_mistakes += 1
                labels = copy.deepcopy(word_list)
                out_cp = copy.deepcopy(output)
                pos_cp = copy.deepcopy(pos_list)
                labels.insert(0,'_B-1')
                labels.insert(0, '_B-2') # first two 'words' are B_-2 B_-1
                labels.append("_B+1")
                labels.append("_B+2")
                out_cp.insert(0,'B_-1')
                out_cp.insert(0,'B_-2')
                pos_cp.insert(0,'B_-1')
                pos_cp.insert(0,'B_-2')
                pos_feat = pos_fgen.Pos_feat_gen(labels)
                gold_out_fv = defaultdict(int)
                pos_feat.get_sent_feature(gold_out_fv,pos_cp)
                cur_out_fv = defaultdict(int)
                pos_feat.get_sent_feature(cur_out_fv,out_cp)
                feat_vec_update = defaultdict(int)
                for feature in gold_out_fv:
                    feat_vec_update[feature]+=gold_out_fv[feature]
                for feature in cur_out_fv:
                    feat_vec_update[feature]-=cur_out_fv[feature]
                for upd_feat in feat_vec_update:
                    if feat_vec_update[upd_feat] != 0:
                        weight_vec[upd_feat] += feat_vec_update[upd_feat]
                        if (upd_feat) in last_iter:
                            avg_vec[upd_feat] += (num_updates - last_iter[upd_feat]) * weight_vec[upd_feat]
                        else:
                            avg_vec[upd_feat] = weight_vec[upd_feat]
                        last_iter[upd_feat] = num_updates
            trian_sent+=1
            #print "training sentence:", trian_sent
        print >>sys.stderr, "number of mistakes:", num_mistakes, " iteration:", round+1
        #dump_vector("fv",round,weight_vec,last_iter,avg_vec, num_updates)
    for feat in weight_vec:
        if feat in last_iter:
            avg_vec[feat] += (num_updates - last_iter[feat]) * weight_vec[feat]
        else:
            avg_vec[feat] = weight_vec[feat]
        weight_vec[feat] = avg_vec[feat] / num_updates
    return weight_vec

def dump_vector(filename, i, fv):
    w_vector = weight_vector.WeightVector()
    w_vector.data_dict.iadd(fv)
    w_vector.dump(filename + "_Iter_%d.db"%i)
'''
def dump_vector(filename, i, weight_vec, last_iter, avg_vec, num_updates):
    fv = copy.deepcopy(weight_vec)
    av = copy.deepcopy(avg_vec)
    for (feat, tag) in fv:
        if (feat, tag) in last_iter:
            av[feat, tag] += (num_updates - last_iter[feat, tag]) * fv[feat, tag]
        else:
            av[feat, tag] = fv[feat, tag]
        fv[feat, tag] = av[feat, tag] / num_updates

    w_vector = weight_vector.WeightVector()
    w_vector.data_dict.iadd(fv)
    i=i+1
    w_vector.dump(filename + "_Iter_%d.db"%i)
'''
if __name__ == '__main__':
    # each element in the feat_vec dictionary is:
    # key=feature_id value=weight
    tagfile = sys.argv[1]
    data_path = sys.argv[2]
    numepochs = int(sys.argv[3])
    start = int(sys.argv[4])
    end = int(sys.argv[5])
    tagset = read_tagset(tagfile)
    train_data = []
    #TODO: change the interface of datapool, no need to use fgen here!
    fgen = english_1st_fgen.FirstOrderFeatureGenerator

    print "loading data..."
    #dp = data_pool.DataPool([(2,5)], data_path,fgen)
    dp = data_pool.DataPool([(start,end)], data_path,fgen)
    sentence_count = 0
    while dp.has_next_data():
    #for i in range(100):
        sentence_count+=1
        data = dp.get_next_data()
        del data.word_list[0]
        del data.pos_list[0]
        train_data.append((data.word_list,data.pos_list))

    print("Sentence Number: %d" % sentence_count)
    
    print "perceptron training..."
    start = time.time()
    feat_vec=avg_perc_train(train_data, tagset, numepochs)
    print time.time()-start
    #dump the model on disk
    dump_vector("fv",numepochs,feat_vec)
    





