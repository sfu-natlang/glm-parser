
import perc
import time
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from collections import defaultdict
from feature import english_1st_fgen, pos_fgen
from data.data_pool import *
# To Do: for test!!!!
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

if __name__ == '__main__':
   
    # each element in the feat_vec dictionary is:
    # key=feature_id value=weight
    numepochs = 1
    feat_vec = {}
    tagset = ['CC','CD','DT','EX','FW','IN','JJ','JJR','JJS','LS','MD','NN','NNS','NNP','NNPS','PDT','POS',
    'PRP','PRP$','RB','RBR','RBS','RP','SYM','TO','UH','VB','VBD','VBG','VBN','VBP','VBZ','WDT','WP','WP$','WRB','.',',',':','(',')']
    train_data = []
    data_path = "/Users/vivian/data/penn-wsj-deps/"
    fgen = english_1st_fgen.FirstOrderFeatureGenerator
    data_pool = DataPool([2], data_path, fgen=fgen)
    sentence_count = 1
    while data_pool.has_next_data():
        #print("Sentence %d" % sentence_count)
        sentence_count+=1
        data = data_pool.get_next_data()
        train_data.append((data.word_list,data.pos_list))
    print sentence_count
    start = time.time()
    feat_vec = avg_perc_train(train_data, tagset, numepochs)
    print time.time()-start
    fv = []
    pos_feat = pos_fgen.Pos_feat_gen(data.word_list,data.pos_list)
    pos_feat.get_pos_feature(fv)
    output = perc.perc_test(feat_vec,data.word_list,fv,tagset, tagset[0])
    print output
    print data.pos_list
    
'''   
    #for test:
    data_path = "/Users/vivian/data/penn-wsj-deps/"
    train_data = []
    fgen = english_1st_fgen.FirstOrderFeatureGenerator
    data_pool = DataPool([2],data_path,fgen)
    data = data_pool.get_next_data()
    train_data.append((data.word_list,data.pos_list))
    for (word_list, pos_list) in train_data:
    #generate features for thee word list...      
        fv = []
        pos_feat = pos_fgen.Pos_feat_gen(word_list,pos_list)
        pos_feat.get_pos_feature(fv)
        #print fv
        index = 0
        tagset = ['CC','CD','DT','EX','FW','IN','JJ','JJR','JJS','LS','MD','NN','NNS','NNP',
        'NNPS','PDT','POS','PRP','PRP$','RB','RBR','RBS','RP','SYM','TO','UH','VB','VBD','VBG',
        'VBN','VBP','VBZ','WDT','WP','WP$','WRB','.',',',':','(',')']
        default_tag = tagset[0]
        output = perc.perc_test({},word_list,fv,tagset, default_tag)
        print output
        for word in range(2,len(word_list)-2):
            (index,feats) = get_feats_for_word(index,fv)
            print word_list[word]
            print pos_list[word]
            print index
            print feats

'''
        




