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
debug = False


class Decoder:
    def __init__(self):
        self.weight_vec = {}
        self.sentences = []
        self.pos_tags = []
        self.chunks = []
        self.ner_tags = []
        self.tags = set()

    def tag_data(self, test_file):
        argmax = ner_viterbi.Viterbi()
        infile = open(test_file, 'r')
        # file.seek(0) sets the file's current reading position at offset 0
        infile.seek(0)
        sentence = []
        pos_tag = []
        chunk = []
        ner_tag = []
        for line in infile:
            line = line.strip()
            if line: # Non-empty line
                #method split() returns a list of all the words in the string, using a delimiter (splits on all whitespace if left unspecified)
                token = line.split()
                word = token[0]
                ptag  = token[1]
                ctag = token[2]
                nertag = token[3]
                #appends the word at the end of the list
                sentence.append(word)
                pos_tag.append(ptag)
                chunk.append(ctag)

                #appends the tag at the end of the list
                ner_tag.append(nertag)
            else: # End of sentence reached
                #converts the sentence list to a tuple and then appends that tuple to the end of the self.x list
                self.sentences.append(tuple(sentence))
                self.pos_tags.append(tuple(pos_tag))
                self.chunks.append(tuple(chunk))
                self.ner_tags.append(tuple(ner_tag))
                self.tags.update(ner_tag)
                sentence = []
                pos_tag = []
                chunk = []
                ner_tag = []
        infile.close()

        target = open('out_file.txt', 'w')
        for i in range(len(self.sentences)):
            sentence = list(self.sentences[i])
            pos_tag = list(self.pos_tags[i])
            ner_tag = list(self.ner_tags[i])
            tags = argmax.perc_test(self.weight_vec, sentence, self.tags)
            for n in range(len(sentence)):
                target.write("%s %s %s %s\n" % (sentence[n], pos_tag[n], ner_tag[n], tags[n]))
            target.write("\n")

        target.close()

    def reset_weights(self):
        """
        Reset all the weights to zero in the weight vector.
        """
        for feature in self.weight_vec:
            self.weight_vec[feature] = 0

    def read_weights(self, weight_file):
        """
        Read the previously determined weight vector(features and values) from the input file.
        :param weight_file the path of the weight vector 
        """
        #self.reset_weights()
        feat_vec = weight_vector.WeightVector()
        feat_vec.load(weight_file)
        self.weight_vec = feat_vec.data_dict



def main(test_file, weight_file):
    decoder = Decoder()
    argmax = ner_viterbi.Viterbi()
    # Read the previously determined weight vector
    decoder.read_weights(weight_file)
    #for i in fv:
    #    if (feat, tag) in decoder.weight_vec.keys():
    #        print "!!"

    # Find the most likely tag sequence for each sentence in the data file
    decoder.tag_data(test_file)

def usage():
    sys.stderr.write("""
    Usage: python ner_evaluate.py [test_file] [weight_file]\n
        Find the ner tags for the test file.\n""")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)
    main(sys.argv[1],sys.argv[2])
    #main("eng.train")
