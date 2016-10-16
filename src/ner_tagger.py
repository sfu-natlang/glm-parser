
# Named Entity Recogniser
# Simon Fraser University
# NLP Lab
# NER 

# This is the main programme of the Part of the Named Entitiy Recognition System.
# Individual modules of the tagger are located in src/ner/


from ner import ner_decode, ner_perctrain, ner_features
from weight import weight_vector
import debug.debug
#import debug.interact
import os,sys
import timeit
import time
import ConfigParser

import argparse
from ConfigParser import SafeConfigParser
from collections import defaultdict


class NerTagger():

    def __init__(self,tag_file="ner_tagset.txt",max_iter=10,train_data="/cs/natlang-data/CoNLL/CoNLL-2003/eng.train", test_data="/cs/natlang-data/CoNLL/CoNLL-2003/eng.testa"):
        #self.brown_data_file = "./ner/brown_cluster.txt"
        #self.brown_data = self.load_data(self.brown_data_file)
        print "NER [INFO]: Loading Training Data"
        self.train_data_file = train_data
        self.train_data = self.loading_data(self.train_data_file)
        print "NER [INFO]: Loading Testing Data"
        self.test_data_file =test_data
        self.test_data = self.loading_data(self.test_data_file)
        print "NER [INFO]: Total Iteration: %d" % max_iter
        
        self.max_iter = max_iter
        self.default_tag = "O"
    
# function to load the training and testing data  
    def loading_data(self, data_file):

        f = open(data_file, 'r')
        f.seek(0)
        sentence = []
        sentence_count = 0
        tags = []
        pos_tag = []
        chunking_tag = []
        data_list = []
        for line in f:
            line = line.strip()
            if line: # Non-empty line
                token = line.split()
                word = token[0]
                tag  = token[3]
                p_tag = token[1] # holds the pos tag
                ch_tag = token[2] # holds the chunking tag
                #appends the word at the end of the list
                sentence.append(word)
                #appends the tag at the end of the list
                tags.append(tag)
                pos_tag.append(p_tag)
                chunking_tag.append(ch_tag)
                
            else: # End of sentence reached
                #converts the sentence list to a tuple and then appends that tuple to the end of the self.x list
                sentence.insert(0, '_B_-1')
                sentence.insert(0, '_B_-2')
                sentence.append('_B_+1')
                sentence.append('_B_+2') # last two 'words' are B_+1 B_+2
                tags.insert(0,'B_-1')
                tags.insert(0,'B_-2')
                tags.append('B_+1')
                tags.append('B_+2')
                pos_tag.insert(0,'B_-1')
                pos_tag.insert(0,'B_-2')
                pos_tag.append('B_+1')
                pos_tag.append('B_+2')
                chunking_tag.insert(0,'B_-1')
                chunking_tag.insert(0,'B_-2')
                chunking_tag.append('B_+1')
                chunking_tag.append('B_+2')

                ner_feat = ner_features.Ner_feat_gen(sentence)
                #print "tags"+str(tag)
                gold_out_fv = defaultdict(int)
		# getiing the gold features for the sentence
                ner_feat.get_sent_feature(gold_out_fv,tags,pos_tag,chunking_tag)

                data_list.append((sentence,pos_tag,chunking_tag,tags,gold_out_fv))
                sentence = []
                tags = []
                pos_tag = []
                chunking_tag = []
                sentence_count += 1
        
            

        print "NER [INFO]: Sentence Number: %d" % sentence_count
        f.close()
        return data_list

# function to load the brown clusters
    
    def load_data(self,brown_file):
        f = open(brown_file,'r')
        f.seek(0)
        data_list = []
        for line in f:
            line = line.strip()
            if line: # Non-empty line
                data_list.append(line)
        f.close()
        return data_list

# function to call the average perceptron algorith implemented in another file 
 
    def perc_train(self, dump_data=True):
        #loc_list = gazateers.LOC_list_formation()
        #per_list = gazateers.PER_list_formation()
        perc = ner_perctrain.NerPerceptron(max_iter=max_iter, default_tag="O", tag_file="ner_tagset.txt")
        self.w_vector = perc.avg_perc_train(self.train_data)
        #self.w_vector = perc.perc_train(self.train_data)
        if dump_data:
            perc.dump_vector("NER",max_iter,self.w_vector)

# function to calulate the accuracy

    def evaluate(self, fv_path=None):
        #loc_list = gazateers.LOC_list_formation()
        #per_list = gazateers.PER_list_formation()
        tester = ner_decode.Decoder(self.test_data)
        if fv_path is not None:
            feat_vec = weight_vector.WeightVector()
            feat_vec.load(fv_path)
            self.w_vector = feat_vec

        acc = tester.get_accuracy(self.w_vector)

MAJOR_VERSION = 0
MINOR_VERSION = 1

if __name__ == '__main__':

    import getopt, sys

   
    max_iter = 10
    tag_file = 'ner_tagset.txt'


    print "NER [INFO]: Training Starts, Time starts"
    start_time = time.time()
    tagger = NerTagger()#TODO: add input data path
    tagger.perc_train()
    end_time = time.time()
    training_time = end_time - start_time
    print "NER [INFO]: Total Training Time: ", training_time

    tagger.evaluate()
