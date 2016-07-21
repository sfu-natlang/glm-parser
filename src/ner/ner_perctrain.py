# This is the machine learning algorithm of the Named Entity Recogniser Tagger.
# This contains an implementation of both average perceptron method as well as perceptron method

from __future__ import division
import time,copy,logging
import os,sys,inspect
from collections import defaultdict
import ner_features, ner_viterbi, ner_tagset

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from weight import weight_vector

class NerPerceptron():

    def __init__(self, w_vector=None, max_iter=1, default_tag="O", tag_file="ner_tagset.txt"):
        self.w_vector = w_vector
        self.max_iter = max_iter
        self.default_tag = default_tag
        self.tagset = ner_tagset.read_ner_tagset()
        print "NER [DEBUG]: Trainer Loaded"

# function to perform average perceptron method

    def avg_perc_train(self, train_data):
        print "NER [INFO]: Training using the Average Perceptron Method"
        if len(self.tagset) <= 0:
            raise valueError("NER [ERROR]: tagset doesnt contain anything")
        argmax = ner_viterbi.Viterbi()
        weight_vec = defaultdict(float)
        average_vec = defaultdict(float)
        last_iter = {}
        c = 0
	# max_iter is the number of times the training happens on the train data
        for iteration in range(self.max_iter):
            print "NER [INFO]: Iteration number  %d"%iteration
            mistakes = 0

            for (word_list,pos_list,chunk_list,ner_list, gold_out_fv) in train_data:
                print "\rNER [INFO]: %d sentences trained"%c,
                output = argmax.perc_test(weight_vec,word_list,pos_list,chunk_list,self.tagset,self.default_tag)
                c += 1
                #print "output"+str(output)
                #print "ner_list"+str(ner_list)
                if output != ner_list:
                    mistakes += 1

                    # Initialise
                    cur_out_fv = defaultdict(int)
                    weight_delta = defaultdict(int)

                    # Get a
                    ner_feat = ner_features.Ner_feat_gen(word_list)
                    ner_feat.get_sent_feature(cur_out_fv,output,pos_list,chunk_list)

                    # Get Delta
                    for item in gold_out_fv:
                        weight_delta[item] += gold_out_fv[item]
                    for item in cur_out_fv:
                        weight_delta[item] -= cur_out_fv[item]

                    # Process Delta
                    for item in weight_delta:
                        if weight_delta[item] != 0:

                            weight_vec[item] += weight_delta[item]

                            if (item) in last_iter:
                                average_vec[item] += (c - last_iter[item]) * weight_vec[item]
                            else:
                                average_vec[item] = weight_vec[item]

                            last_iter[item] = c

            print "\rNER [INFO]: Number of mistakes after the iteration:", mistakes
        
        for item in weight_vec:
            if item in last_iter:
                average_vec[item] += (c - last_iter[item]) * weight_vec[item]
            else:
                average_vec[item] = weight_vec[item]

            weight_vec[item] = average_vec[item] / c
        print "NER [DEBUG]: Training is Completed"
        return weight_vec

# function to perform perceptron method

    def perc_train(self,train_data):
        # insert your code here
        default_tag = tagset[0]
        feat_vec = defaultdict(int)
        epochs = max_iter
        for round in range(0,epochs):
            num_mistakes = 0
            for (word_list,pos_list,chunk_list, ner_list,gold_out_fv) in train_data:
                output = argmax.perc_test(feat_vec,word_list,pos_list,chunk_list, self.tagset, self.default_tag)
                if output != ner_list:
                    num_mistakes += 1
                    output.insert(0,'B_-1')
                    output.insert(0,'B_-2')
                    a = defaultdict(int)
                    w_delta = defaultdict(int)

                    # Get a
                    ner_feat = ner_features.Ner_feat_gen(word_list)
                    ner_feat.get_sent_feature(a,output,pos_list,chunk_list)
                    
                    for item in gold_out_fv:
                        w_delta[item] += gold_out_fv[item]
                    for item in a:
                        w_delta[item] -= a[item]

                    for item in w_delta:
                        if w_delta[item] != 0:
                            feat_vec[item] += w_delta[item]
        print >>sys.stderr, "number of mistakes:", num_mistakes
        return feat_vec

# function to dump the features into a files after the complete training    

    def dump_vector(self, filename, iteration, fv):
        print "NER [INFO]: Dumping weight_vec to " + filename + "_Iter_%d.db"%iteration
        w_vector = weight_vector.WeightVector()
        w_vector.iadd(fv)
        w_vector.dump(filename + "_Iter_%d.db"%iteration)

# function to dump features after evey loop through the training data

    def dump_vector_per_iter(self, filename, iteration, weight_vec, last_iter, avg_vec, num_updates):
        print "NER [INFO]: Dumping weight_vec to " + filename + "_Iter_%d.db"%iteration
        fv = copy.deepcopy(weight_vec)
        av = copy.deepcopy(avg_vec)
        for feat in fv:
            if feat in last_iter:
                av[feat] += (num_updates - last_iter[feat]) * fv[feat]
            else:
                av[feat] = fv[feat]
            fv[feat] = av[feat] / num_updates

        w_vector = weight_vector.WeightVector()
        w_vector.iadd(fv)
        i=i+1
        w_vector.dump(filename + "_Iter_%d.db"%iteration)
