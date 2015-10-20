import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from data import sentence
from feature import english_1st_fgen, pos_fgen
from data import data_pool
def setup():
    word_list = ["John", "hit", "the", "ball", "with", "the", "bat", "A22", "a-a"]
    pos_list = [ "N", "V", "D", "N", "P", "D", "N", "N", "N"]
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
    tagset = ['CC','CD','DT','EX','FW','IN','JJ','JJR','JJS','LS','MD','NN','NNS','NNP','NNPS','PDT','POS',
    'PRP','PRP$','RB','RBR','RBS','RP','SYM','TO','UH','VB','VBD','VBG','VBN','VBP','VBZ','WDT','WP','WP$',
    'WRB','.',',',':','(',')']
    fv = []
    #print sent.f_gen.word_list
    #pos_feat = pos_fgen.Pos_feat_gen(sent)
    #pos_feat.get_pos_feature(fv)
    '''direction, dist = sent.f_gen.get_dir_and_dist(2, 5)
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
    for t in fv:
        print t'''
    dp = data_pool.DataPool([2], "/Users/vivian/data/penn-wsj-deps/",english_1st_fgen.FirstOrderFeatureGenerator)
    i = 0
    while dp.has_next_data():
        data = dp.get_next_data()
        print data.word_list
        print data.pos_list
        pos_feat = pos_fgen.Pos_feat_gen(data.word_list, tagset)
        pos_feat.get_pos_feature(fv)
        for t in fv:
            print t
        break
    return 

if __name__ == "__main__":
    main()
    
