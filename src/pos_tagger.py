from data import data_pool
from pos import pos_evaluate, pos_perctrain
from weight import weight_vector
import debug.debug
import debug.interact
import os,sys
import timeit
import time

class PosTagger():
    def __init__(self, train_regex="", test_regex="", data_path="../../penn-wsj-deps/", tag_file="tagset.txt",
                 max_iter=1,config="config/penn2malt.config"):
        self.train_data = self.load_data(train_regex, data_path, config)
        self.test_data = self.load_data(test_regex, data_path,config)
        self.max_iter = max_iter
        self.default_tag = "NN"

    def load_data(self, regex, data_path, config):
        dp = data_pool.DataPool(regex, data_path, config_path=config)
        data_list =[]
        sentence_count = 0
        while dp.has_next_data():
            sentence_count+=1
            data = dp.get_next_data()
            word_list = data.column_list["FORM"]
            pos_list = data.column_list["POSTAG"]
            del word_list[0]
            del pos_list[0]
            data_list.append((word_list,pos_list))

        print "Sentence Number: %d" % sentence_count
        return data_list

    def perc_train(self, dump_data=True):
        perc = pos_perctrain.PosPerceptron(max_iter=max_iter, default_tag="NN", tag_file="tagset.txt")
        self.w_vector = perc.avg_perc_train(self.train_data)
        if dump_data:
            perc.dump_vector("fv",max_iter,self.w_vector)

    def eveluate(self, fv_path=None):
        tester = pos_evaluate.PosEvaluator(self.test_data)
        if fv_path is not None:
            feat_vec = weight_vector.WeightVector()
            feat_vec.load_posfv(fv_path)
            self.w_vector = feat_vec.data_dict
            
        acc = tester.get_accuracy(self.w_vector)

    
if __name__ == '__main__':

    tag_file = sys.argv[1]
    max_iter = int(sys.argv[2])
    data_path = sys.argv[3]
    train_regex = sys.argv[4]
    test_regex = sys.argv[5]

    tagger = PosTagger(train_regex,test_regex,data_path,tag_file, max_iter)
    tagger.perc_train()
    tagger.eveluate()
