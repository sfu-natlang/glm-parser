import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import pos_viterbi
import time

class PosEvaluator():
    def __init__(self, test_list=None, tag_file="tagset.txt"):
        self.test_list = test_list
        self.tagset = self.read_tagset(tag_file)

    def read_tagset(self, file_path):
        tagset = []
        with open(file_path,"r") as in_file:
            for line in in_file:
                line = line.strip()
                tagset.append(line)
        return tagset

    def sent_evaluate(self, result_list, gold_list):
        result_size = len(result_list)
        gold_size = len(gold_list)
        if(result_size!=gold_size): 
            raise ValueError("tag results do not align with gold results")
        correct_num = 0
        for i in range(result_size):
            if result_list[i] == gold_list[i]:
                correct_num += 1
        return correct_num, gold_size

    def result_evaluate(self, unlabeled_correct_num,unlabeled_gold_set_size,correct_num, gold_set_size):
        unlabeled_correct_num += correct_num
        unlabeled_gold_set_size += gold_set_size
        return unlabeled_correct_num, unlabeled_gold_set_size

    def get_accuracy(self, w_vec):
        argmax = pos_viterbi.Viterbi()
        correct_num = gold_set_size = 0
        for (word_list, pos_list) in self.test_list:
            output = argmax.perc_test(w_vec,word_list,self.tagset,"NN")
            cnum, gnum = self.sent_evaluate(output,pos_list)
            correct_num, gold_set_size = self.result_evaluate(correct_num,gold_set_size,cnum,gnum)
        acc = float(correct_num) /gold_set_size
        print "whole accraccy: ", acc
        return acc
    
