# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 23:00:01 2014

@author: Ella
"""

import data_set, weight_learner

def test_weight_learner():
    section_set = [1]
    wl = weight_learner.WeightLearner()
    wl.learn_weight_source(section_set)
    
if __name__ == "__main__":
    test_weight_learner()
    '''
    ds = data_set.DataSet(section_set=[2])
    i = 0
    while ds.has_next_data():
      
        a = ds.get_next_data()
        
        print a.get_word_list()
        print a.get_pos_list()
        print a.get_edge_list()
        
        i=i+1
    print i
    '''