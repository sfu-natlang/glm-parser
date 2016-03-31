#! /usr/bin/python
from __future__ import division
import sys
import ner_viterbi
import time,copy,logging
import os,sys,inspect
from collections import defaultdict


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from weight import weight_vector
# Debug output flag
debug = False




class Trainer:
    def __init__(self):
        self.tags = set()
        self.weight_vec = defaultdict(float)
        self.sentences = []
        self.ner_tags = []

    def read_training_data(self, training_file):
        """
        Read the conll2003 english training file
        :param training_file: the path of the training file
        """
        if debug: sys.stdout.write("Reading training data...\n")

        file = open(training_file, 'r')
        # file.seek(0) sets the file's current reading position at offset 0
        file.seek(0)
        sentence = []
        tags = []
        for line in file:
            #String.strip([chars]);
            #returns a copy of the string in which all chars have been stripped from the beginning and the end of the string.
            #e.g str = "0000000this is string example....wow!!!0000000"; 
            #    print str.strip( '0' )
            # answer: this is string example....wow!!!
            line = line.strip()
            if line: # Non-empty line
                #method split() returns a list of all the words in the string, using a delimiter (splits on all whitespace if left unspecified)
                token = line.split()
                word = token[0]
                tag  = token[3]
                #appends the word at the end of the list
                sentence.append(word)
                #appends the tag at the end of the list
                tags.append(tag)
            else: # End of sentence reached
                #converts the sentence list to a tuple and then appends that tuple to the end of the self.x list
                self.sentences.append(tuple(sentence))
                self.ner_tags.append(tuple(tags))
                #set object is an unordered collection of items and don't have duplicate items
                #set.update(other, ...)
                #Update the set, adding elements from all others
                # so self.tags.update(tags) keeps only the distinct # of tags for that sentence
                self.tags.update(tags)
                sentence = []
                tags = []
        file.close()

    def contains_upper(self,s):
        return any(char.isupper() for char in s)

    def sent_feat_gen(self, fv, sent, tags):
        for i in range(3, len(sent)-2):
            word = sent[i]
            tag = tags[i]
            fv[('TAG',word),tag]+=1
            fv[('PREFIX',word[:3]),tag]+=1
            fv[('SUFFIX',word[-3:]),tag]+=1
            fv[('BIGRAM',tags[i-1],tag)]+=1
            fv[('TRIGRAM',tags[i-2],tags[i-1]),tag]+=1
            if self.contains_upper(word):
                fv[("HasUpperCase"),tag]+=1


    def reset_weights(self):
        """
        Reset all the weights to zero in the weight vector.
        """
        for feature in self.weight_vec:
            self.weight_vec[feature] = 0


    def perceptron_algorithm(self, iterations):
        """
        Run the perceptron algorithm to estimate (or improve) the weight vector.
        """
        self.reset_weights()
        num_updates = 0
        avg_vec = defaultdict(float)
        feat_count = defaultdict(int)
        last_iter = {}
        num_updates = 0
        argmax = ner_viterbi.Viterbi()
        for iteration in range(iterations):
            num_mistakes = 0
            for i in range(len(self.sentences)):
                #list(self.x[i]) converts the given tuple into a list.
                sentence = list(self.sentences[i])
                #list(self.y[i]) converts the given sentence tuple into a list.
                tags = list(self.ner_tags[i])

                # Find the best tagging sequence using the Viterbi algorithm
                predict_tags = argmax.perc_test(self.weight_vec, sentence, self.tags)
                num_updates += 1

                if predict_tags != tags:
                    num_mistakes += 1
                    labels = copy.deepcopy(sentence)
                    out_cp = copy.deepcopy(predict_tags)
                    tags_cp = copy.deepcopy(tags)

                    labels.insert(0, '_B_-1')
                    labels.insert(0, '_B_-2') # first two 'words' are B_-2 B_-1
                    labels.append('_B_+1')
                    labels.append('_B_+2') # last two 'words' are B_+1 B_+2

                    out_cp.insert(0,'B_-1')
                    out_cp.insert(0,'B_-2')

                    tags_cp.insert(0,'B_-1')
                    tags_cp.insert(0,'B_-2')

                    #pos_feat = pos_features.Pos_feat_gen(labels)

                    gold_out_fv = defaultdict(int)
                    self.sent_feat_gen(gold_out_fv,labels, tags_cp)
                    cur_out_fv = defaultdict(int)
                    self.sent_feat_gen(cur_out_fv,labels, out_cp)
                    feat_vec_update = defaultdict(int)

                    for feature in gold_out_fv.keys():
                        feat_vec_update[feature]+=gold_out_fv[feature]
                        feat_count[feature]+=gold_out_fv[feature]
                    for feature in cur_out_fv.keys():
                        feat_vec_update[feature]-=cur_out_fv[feature]
                    for upd_feat in feat_vec_update.keys():
                        if feat_vec_update[upd_feat] != 0:
                            self.weight_vec[upd_feat] += feat_vec_update[upd_feat]
                            if (upd_feat) in last_iter:
                                avg_vec[upd_feat] += (num_updates - last_iter[upd_feat]) * self.weight_vec[upd_feat]
                            else:
                                avg_vec[upd_feat] = self.weight_vec[upd_feat]
                            last_iter[upd_feat] = num_updates
            
            print "number of mistakes:", num_mistakes, " iteration:", iteration+1
            #dump_vector("fv",round,weight_vec,last_iter,avg_vec, num_updates)
        for feat in self.weight_vec:
            if feat in last_iter:
                avg_vec[feat] += (num_updates - last_iter[feat]) * self.weight_vec[feat]
            else:
                avg_vec[feat] = self.weight_vec[feat]
            self.weight_vec[feat] = avg_vec[feat] / num_updates
        self.dump_vector("NER", iterations, self.weight_vec)

    def dump_vector(self, filename, i, fv):
        w_vector = weight_vector.WeightVector()
        w_vector.data_dict.iadd(fv)
        w_vector.dump(filename + "_Iter_%d.db"%i)

def main(training_file):
    """
    """

    trainer = Trainer()

    # Read the training data (x, y)
    trainer.read_training_data(training_file)

    # Compute the weight vector using the Perceptron algorithm
    trainer.perceptron_algorithm(2)


def usage():
    sys.stderr.write("""
    Usage: python ner_training.py [training_file]\n
        Find the weight vector for ner tagging.\n""")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
    main(sys.argv[1])
    #main("eng.train")