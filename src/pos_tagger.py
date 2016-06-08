from data import data_pool
from pos import pos_decode, pos_perctrain, pos_features
from weight import weight_vector
import debug.debug
import debug.interact
import os,sys
import timeit
import time
from collections import defaultdict

class PosTagger():
    def __init__(self, train_regex="", test_regex="", data_path="../../penn-wsj-deps/", tag_file="tagset.txt",
                 max_iter=1,data_format="format/penn2malt.format"):
        self.train_data = self.load_data(train_regex, data_path, data_format)
        self.test_data = self.load_data(test_regex, data_path, data_format)
        self.max_iter = max_iter
        self.default_tag = "NN"

    def load_data(self, regex, data_path, data_format):
        dp = data_pool.DataPool(regex, data_path, config_path=data_format)
        data_list =[]
        sentence_count = 0
        while dp.has_next_data():
            sentence_count+=1
            data = dp.get_next_data()
            word_list = data.column_list["FORM"]
            pos_list = data.column_list["POSTAG"]

            del word_list[0]
            del pos_list[0] # delet Root

            word_list.insert(0, '_B_-1')
            word_list.insert(0, '_B_-2') # first two 'words' are B_-2 B_-1
            word_list.append('_B_+1')
            word_list.append('_B_+2') # last two 'words' are B_+1 B_+2
            pos_list.insert(0,'B_-1')
            pos_list.insert(0,'B_-2')

            pos_feat = pos_features.Pos_feat_gen(word_list)

            gold_out_fv = defaultdict(int)
            pos_feat.get_sent_feature(gold_out_fv,pos_list)

            data_list.append((word_list,pos_list,gold_out_fv))

        print "Sentence Number: %d" % sentence_count
        return data_list

    def perc_train(self, dump_data=True):
        perc = pos_perctrain.PosPerceptron(max_iter=max_iter, default_tag="NN", tag_file="tagset.txt")
        self.w_vector = perc.avg_perc_train(self.train_data)
        if dump_data:
            perc.dump_vector("fv",max_iter,self.w_vector)

    def eveluate(self, fv_path=None):
        tester = pos_decode.Decoder(self.test_data)
        if fv_path is not None:
            feat_vec = weight_vector.WeightVector()
            feat_vec.load(fv_path)
            self.w_vector = feat_vec.data_dict

        acc = tester.get_accuracy(self.w_vector)


if __name__ == '__main__':

    tag_file = sys.argv[1]
    max_iter = int(sys.argv[2])
    data_path = sys.argv[3]
    train_regex = sys.argv[4]
    test_regex = sys.argv[5]

    start_time = time.time()
    tagger = PosTagger(train_regex,test_regex,data_path,tag_file, max_iter)
    tagger.perc_train()
    end_time = time.time()
    training_time = end_time - start_time
    print "Total Training Time: ", training_time

    tagger.eveluate()
