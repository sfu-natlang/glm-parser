from __future__ import division

class Evaluator():
    def __init__(self):
        self.unlabeled_correct_num = 0
        self.unlabeled_gold_set_size = 0
        return
        
    def reset(self):
        self.unlabeled_correct_num = 0
        self.unlabeled_gold_set_size = 0
        return
    
    def _sent_unlabeled_accuracy(self, test_edge_set, gold_edge_set):      
        if isinstance(test_edge_set, list):
            test_edge_set = set(test_edge_set)
        
        if isinstance(gold_edge_set, list):
            gold_edge_set = set(gold_edge_set)
        
        intersect_set = test_edge_set.intersection(gold_edge_set)
        correct_num = len(intersect_set)
        gold_set_size = len(gold_edge_set)
        
        return correct_num, gold_set_size
    
    
    def unlableled_accuracy(self, test_edge_set, gold_edge_set, accumulate=False):      
        correct_num, gold_set_size =\
            self._sent_unlabeled_accuracy(test_edge_set, gold_edge_set)
            
        if accumulate == True:          
            self.unlabeled_correct_num += correct_num
            correct_num = self.unlabeled_correct_num
            
            self.unlabeled_gold_set_size += gold_set_size
            gold_set_size = self.unlabeled_gold_set_size
        
        return correct_num / gold_set_size
        
    def get_acc_unlableled_accuracy(self):
        return self.unlabeled_correct_num / self.unlabeled_gold_set_size