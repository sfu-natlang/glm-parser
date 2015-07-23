import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from data import sentence
from feature import english_1st_fgen

def setup():
    word_list = ["John", "hit", "the", "ball", "with", "the", "bat"]
    pos_list = [ "N", "V", "D", "N", "P", "D", "N"]
    edge_set = {(2,5): "some property"}
    fgen = english_1st_fgen.FirstOrderFeatureGenerator
    sent = sentence.Sentence(word_list, pos_list, edge_set, fgen)
    return sent

def print_fv_and_clear(fv):
    if len(fv) > 0:
        for i in fv:
            print i
        while len(fv) > 0:
            fv.pop()

def main():
    sent = setup()
    fv = []
    direction, dist = sent.f_gen.get_dir_and_dist(2, 5)
    print "Unigram features"
    fv = sent.f_gen.get_unigram_feature(2, 5, direction, dist)
    print_fv_and_clear(fv)
    print "Bigram features"
    fv = sent.f_gen.get_bigram_feature(2, 5, direction, dist)
    print_fv_and_clear(fv)
    print "In-between features"
    fv = sent.f_gen.get_in_between_feature(2, 5, direction, dist)
    print_fv_and_clear(fv)
    print "Surrounding features"
    fv = sent.f_gen.get_surrounding_feature(2, 5, direction, dist)
    print_fv_and_clear(fv)

    return 

if __name__ == "__main__":
    main()
    
