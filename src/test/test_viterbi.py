import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from postag import perc

def test_viterbi():
    '''tagset = ['CC','CD','DT','EX','FW','IN','JJ','JJR','JJS','LS','MD','NN','NNS','NNP','NNPS','PDT','POS',
    'PRP','PRP$','RB','RBR','RBS','RP','SYM','TO','UH','VB','VBD','VBG','VBN','VBP','VBZ','WDT','WP','WP$',
    'WRB','.',',',':','(',')']
    fv = []
    dp = data_pool.DataPool([2], "/Users/vivian/data/penn-wsj-deps/",english_1st_fgen.FirstOrderFeatureGenerator)
    i = 0
    while dp.has_next_data():
        data = dp.get_next_data()
        print data.word_list
        print data.pos_list
        pos_feat = pos_fgen.Pos_feat_gen(data.word_list)
        pos_feat.get_pos_feature(fv,3,'CC','CD')
        for t in fv:
            print t
        break
    return '''
    word_list = ["John", "hit", "the", "ball", "with", "the", "bat"]
    feat_vec = {}
    tagset = ['CC','CD','DT','EX','FW','IN','JJ','JJR','JJS','LS','MD','NN','NNS','NNP','NNPS','PDT','POS',
    'PRP','PRP$','RB','RBR','RBS','RP','SYM','TO','UH','VB','VBD','VBG','VBN','VBP','VBZ','WDT','WP','WP$',
    'WRB','.',',',':','(',')']
    default_tag = tagset[0]
    output = perc.perc_test(feat_vec, word_list, tagset, default_tag)
    print 'testing....'
    print output

if __name__ == "__main__":
    test_viterbi()