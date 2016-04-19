import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from postag import tagging,perctrain

def test_viterbi():
    tagset = ['CC','CD','DT','EX','FW','IN','JJ','JJR','JJS','LS','MD','NN','NNS','NNP','NNPS','PDT','POS',
    'PRP','PRP$','RB','RBR','RBS','RP','SYM','TO','UH','VB','VBD','VBG','VBN','VBP','VBZ','WDT','WP','WP$',
    'WRB','.',',',':','(',')']
    fv = []
    train_data = []
    feat_vec = {}
    feat_vec = perctrain.avg_perc_train(train_data, tagset, 1)
    test_list = ['The', 'new', 'rate', 'will', 'be', 'payable', 'Feb.', '15', '.']
    output = tagging.perc_test(feat_vec,test_list,tagset,tagset[1])
    true_output = ['DT', 'JJ', 'NN', 'MD', 'VB', 'JJ', 'NNP', 'CD', '.']
    print true_output
    print output
    #feat_vec = tagging.avg_perc_train(train_data, tagset, 1)
    #print feat_vec
    
if __name__ == "__main__":
    test_viterbi()