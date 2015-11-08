
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
                labels.insert(0,'_B-1')
                labels.insert(0, '_B-2') # first two 'words' are B_-2 B_-1
                labels.append("_B+1")
                labels.append("_B+2")
                pos_feat = pos_fgen.Pos_feat_gen(labels)
                pre1 = 'B_-1'
                pre2 = 'B_-2'
                for i in range(2,len(labels)-2):
                    out_fv = []
                    pos_feat.get_pos_feature(out_fv,i,pre1,pre2)
                    pre2 = pre1
                    pre1 = output[i-2]
                    feat_vec_update = defaultdict(int)
                    for j in range(len(out_fv)):
                        out_feat = out_fv[j]
                        feat_vec_update[out_feat,output[i-2]] += -1
                        feat_vec_update[out_feat,pos_list[i-2]] += 1
                    for (upd_feat, upd_tag) in feat_vec_update:
                        if feat_vec_update[upd_feat, upd_tag] != 0:
                            weight_vec[upd_feat, upd_tag] += feat_vec_update[upd_feat,upd_tag]
                            if (upd_feat, upd_tag) in last_iter:
                                avg_vec[upd_feat, upd_tag] += (num_updates - last_iter[upd_feat, upd_tag]) * weight_vec[upd_feat, upd_tag]
                            else:
                                avg_vec[upd_feat, upd_tag] = weight_vec[upd_feat, upd_tag]
                            last_iter[upd_feat, upd_tag] = num_updates
            trian_sent+=1
            #print "training sentence:", trian_sent
        #print >>sys.stderr, "number of mistakes:", num_mistakes
    for (feat, tag) in weight_vec:
        if (feat, tag) in last_iter:
            avg_vec[feat, tag] += (num_updates - last_iter[feat, tag]) * weight_vec[feat, tag]
        else:
            avg_vec[feat, tag] = weight_vec[feat, tag]
        weight_vec[feat, tag] = avg_vec[feat, tag] / num_updates
    return weight_vec

def dump_vector(filename, i, fv):
    w_vector = weight_vector.WeightVector()
    w_vector.data_dict.iadd(fv)
    w_vector.dump(filename + "_Iter_%d.db"%i)

if __name__ == '__main__':
    # each element in the feat_vec dictionary is:
    # key=feature_id value=weight
    tagfile = sys.argv[1]
    data_path = sys.argv[2]
    numepochs = int(sys.argv[3])
    tagset = read_tagset(tagfile)
    train_data = []
    #TODO: change the interface of datapool, no need to use fgen here!
    fgen = english_1st_fgen.FirstOrderFeatureGenerator

    print "loading data..."
    dp = data_pool.DataPool([(2)], data_path,fgen)
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
    feat_vec = avg_perc_train(train_data, tagset, numepochs)
    print time.time()-start
    #dump the model on disk
    dump_vector("fv",numepochs,feat_vec)
    





