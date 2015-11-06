import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from feature import english_1st_fgen, pos_fgen
from data import data_pool
from postag import perc
from weight import weight_vector

def sent_evaluate(result_list, gold_list):
    result_size = len(result_list)
    gold_size = len(gold_list)
    if(result_size!=gold_size): 
        raise ValueError("tag results do not align with gold results")
    correct_num = 0
    for i in range(result_size):
        if result_list[i] == gold_list[i]:
            correct_num += 1
    return correct_num, gold_size

def result_evaluate(unlabeled_correct_num,unlabeled_gold_set_size,correct_num, gold_set_size):
    unlabeled_correct_num += correct_num
    unlabeled_gold_set_size += gold_set_size
    return unlabeled_correct_num, unlabeled_gold_set_size
    
def main():
    data_path = sys.argv[1]
    test_data = []
    correct_num = gold_set_size = 0
    fgen = english_1st_fgen.FirstOrderFeatureGenerator
    tagset = ['CC','CD','DT','EX','FW','IN','JJ','JJR','JJS','LS','MD','NN','NNS','NNP','NNPS','PDT','POS',
    'PRP','PRP$','RB','RBR','RBS','RP','SYM','TO','UH','VB','VBD','VBG','VBN','VBP','VBZ','WDT','WP','WP$',
    'WRB','.',',',':','(',')','``','-LRB-','-RRB-',"''"]
    feat_vec = weight_vector.WeightVector()
    feat_vec.load_posfv("../postag/fv_Iter_1.db")
    print "Evaluating..."
    dp = DataPool([(0,1,22,24)], data_path,fgen)
    #dp = data_pool.DataPool([(2,3)], data_path,fgen)
    while dp.has_next_data():
        data = dp.get_next_data()
        del data.word_list[0]
        del data.pos_list[0]
        test_data.append((data.word_list,data.pos_list))
    for (word_list, pos_list) in test_data:
        output = perc.perc_test(feat_vec.data_dict,word_list,tagset,'WP$')
        cnum, gnum = sent_evaluate(output,pos_list)
        correct_num, gold_set_size = result_evaluate(correct_num,gold_set_size,cnum,gnum)
    acc = float(correct_num) /gold_set_size
    print "whole accraccy: ", acc


if __name__ == "__main__":
    main()
    
