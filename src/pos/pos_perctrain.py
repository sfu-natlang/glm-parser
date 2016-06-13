
from __future__ import division
import time,copy,logging
import os,sys,inspect
from collections import defaultdict
import pos_features,pos_viterbi

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

        self.tagset = self.read_tagset(tag_file)
    # read the valid output tags for the task
    def read_tagset(self, file_path):
        tagset = []
        with open(file_path,"r") as in_file:
            for line in in_file:
                line = line.strip()
                tagset.append(line)
        return tagset

    def avg_perc_train(self, train_data):
        if len(self.tagset) <= 0:
            raise valueError("Empty tagset")
        argmax = pos_viterbi.Viterbi()
        weight_vec = defaultdict(float)
        avg_vec = defaultdict(float)
        feat_count = defaultdict(int)
        last_iter = {}
        num_updates = 0
        epochs = self.max_iter

        for round in range(0,epochs):
            num_mistakes = 0
            trian_sent = 0

            for (word_list, pos_list, gold_out_fv) in train_data:

                output = argmax.perc_test(weight_vec,word_list,self.tagset,self.default_tag)
                num_updates += 1

                if output != pos_list:
                    num_mistakes += 1
                    '''
                    labels = copy.deepcopy(word_list)
                    out_cp = copy.deepcopy(output)
                    pos_cp = copy.deepcopy(pos_list)

                    labels.insert(0, '_B_-1')
                    labels.insert(0, '_B_-2') # first two 'words' are B_-2 B_-1
                    labels.append('_B_+1')
                    labels.append('_B_+2') # last two 'words' are B_+1 B_+2

                    out_cp.insert(0,'B_-1')
                    out_cp.insert(0,'B_-2')

                    pos_cp.insert(0,'B_-1')
                    pos_cp.insert(0,'B_-2')
                    '''
                    pos_feat = pos_features.Pos_feat_gen(word_list)

                    #compute current features
                    cur_out_fv = defaultdict(int)
                    pos_feat.get_sent_feature(cur_out_fv,output)

                    feat_vec_update = defaultdict(int)

                    for feature in gold_out_fv:
                        feat_vec_update[feature]+=gold_out_fv[feature]
                        feat_count[feature]+=gold_out_fv[feature]
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

            print "number of mistakes:", num_mistakes, " iteration:", round+1
            #dump_vector("fv",round,weight_vec,last_iter,avg_vec, num_updates)
        for feat in weight_vec:
            if feat in last_iter:
                avg_vec[feat] += (num_updates - last_iter[feat]) * weight_vec[feat]
            else:
                avg_vec[feat] = weight_vec[feat]
            weight_vec[feat] = avg_vec[feat] / num_updates
        return weight_vec

    def dump_vector(self, filename, i, fv):
        w_vector = weight_vector.WeightVector()
        w_vector.data_dict.iadd(fv)
        w_vector.dump(filename + "_Iter_%d.db"%i)

    def dump_vector_per_iter(self, filename, i, weight_vec, last_iter, avg_vec, num_updates):
        fv = copy.deepcopy(weight_vec)
        av = copy.deepcopy(avg_vec)
        for feat in fv:
            if feat in last_iter:
                av[feat] += (num_updates - last_iter[feat]) * fv[feat]
            else:
                av[feat] = fv[feat]
            fv[feat] = av[feat] / num_updates

        w_vector = weight_vector.WeightVector()
        w_vector.data_dict.iadd(fv)
        i=i+1
        w_vector.dump(filename + "_Iter_%d.db"%i)
"""
if __name__ == '__main__':
    # each element in the feat_vec dictionary is:
    # key=feature_id value=weight
    tagfile = sys.argv[1]
    max_iter = int(sys.argv[2])
    data_path = sys.argv[3]
    regex = sys.argv[4]
    formatValue = sys.argv[5]

    perc = PosPerceptron(max_iter=max_iter, default_tag="NN", tag_file="tagset.txt")

    print "loading data..."

    train_data = []
    dp = data_pool.DataPool(regex, data_path, format_path=formatValue)

    # building the training data
    sentence_count = 0
    while dp.has_next_data():
        sentence_count+=1
        data = dp.get_next_data()
        word_list = data.column_list["FORM"]
        pos_list = data.column_list["POSTAG"]
        del word_list[0]
        del pos_list[0]
        train_data.append((word_list,pos_list))

    print "Sentence Number: %d" % sentence_count

    print "perceptron training..."
    start = time.time()
    feat_vec=perc.avg_perc_train(train_data)
    print time.time()-start
    #dump the model on disk
    perc.dump_vector("fv",max_iter,feat_vec)

    print "evaluating..."

    test_data = train_data[:2]
    tester = pos_evaluate.PosEvaluator(test_data)
    tester.get_accuracy(feat_vec)
"""
