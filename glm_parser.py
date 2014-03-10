# -*- coding: utf-8 -*-
import data_set, feature_set, dependency_tree, eisner
import weight_learner, evaluator
import pickle

class GlmParser():
    def __init__(self, filename=None):
        
        if filename != None:
            fp = open(filename, "r")
            pickle.load(fp)
            
        self.fset = feature_set.FeatureSet(
                    dependency_tree.DependencyTree(),
                    'weight.db')
        return
    
    def train(self, section_set=None, data_path=None):
        w_learner = weight_learner.WeightLearner()
        self.fset = w_learner.learn_weight_sections(section_set, data_path)
        return
    
    def unlableled_accuracy(self, section_set=None, data_path=None):
        dataset = data_set.DataSet(section_set, data_path)
        evlt = evaluator.Evaluator()
        evlt.reset()
        while dataset.has_next_data():
            dep_tree = dataset.get_next_data()
            gold_edge_set = \
                set([(head_index,dep_index) for head_index,dep_index,_ in dep_tree.get_edge_list()])
            
            self.fset.switch_tree(dep_tree)
            sent_len = len(dep_tree.get_word_list())
            _, test_edge_set = \
               eisner.EisnerParser().parse(sent_len, self.fset.get_edge_score)
             
            evlt.unlableled_accuracy(test_edge_set, gold_edge_set, True)
        return evlt.get_acc_unlableled_accuracy()
               
              