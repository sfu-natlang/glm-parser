import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from data import sentence
from feature import english_1st_fgen, pos_fgen
from data import data_pool


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

    word_list = ["John", "hit", "the", "ball", "with", "the", "bat"]
    pos_feat = pos_fgen.Pos_feat_gen(word_list)
    pos_feat.get_pos_feature(fv,2,'CC','CD')
    for t in fv:
        print t

    return 

if __name__ == "__main__":
    main()
    
