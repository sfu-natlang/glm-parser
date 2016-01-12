import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from feature import english_1st_fgen, pos_fgen
from data import data_pool
from weight import weight_vector
import tagging,perctrain
from collections import defaultdict

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
    
if __name__ == "__main__":
    tagset_path = sys.argv[1]
    data_path = sys.argv[2]
    fv_path = sys.argv[3]
    test_data = []
    fgen = english_1st_fgen.FirstOrderFeatureGenerator
    tagset = perctrain.read_tagset(tagset_path)
    feat_vec = weight_vector.WeightVector()
    feat_vec.load_posfv(fv_path)
    matrix = [[0 for x in range(45)] for x in range(45)] 
    dic = defaultdict(int)
    i = 0
    for t in tagset:
        dic[t] = i
        i+=1

    print "Evaluating..."
    dp = data_pool.DataPool([(0)], data_path,fgen)
    #dp = data_pool.DataPool([(2,3)], data_path,fgen)
    n=0
    while dp.has_next_data():
        data = dp.get_next_data()
        del data.word_list[0]
        del data.pos_list[0]
        test_data.append((data.word_list,data.pos_list))
        n+=1

    correct_num = gold_set_size = 0
    for (word_list, pos_list) in test_data:
        output = tagging.perc_test(feat_vec.data_dict,word_list,tagset,tagset[0])
        cnum, gnum = sent_evaluate(output,pos_list)
        correct_num, gold_set_size = result_evaluate(correct_num,gold_set_size,cnum,gnum)
        for i in range(len(output)):
            gold_index = dic[pos_list[i]]
            out_index = dic[output[i]]
            '''if(gold_index==0):
                print pos_list[i]'''
            matrix[gold_index][out_index] += 1
    acc = float(correct_num) /gold_set_size
    print "whole accraccy: ", acc
    for i in range(45):
        print i, " : "
        for j in range(45):
            print matrix[i][j]," ",
        print