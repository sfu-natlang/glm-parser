# -*- coding: utf-8 -*-
import copy

class PerceptronLearner():

    def __init__(self, w_vector, max_iter=1):
        self.w_vector = w_vector
        self.max_iter = max_iter
        return

    def sequential_learn(self, f_argmax, data_pool=None, max_iter=-1, d_filename=None):
        if max_iter <= 0:
            max_iter = self.max_iter
            
        print "Starting sequantial train..."
        for i in range(max_iter):
            print "Iteration:", i
            
            while data_pool.has_next_data():
                dada_instance = data_pool.get_next_data()
                gold_global_vector = dada_instance.gold_global_vector
                current_global_vector = f_argmax(dada_instance)
                self.update_weight(current_global_vector, gold_global_vector)

            data_pool.reset()
            if not d_filename == None:
                self.w_vector.dump(d_filename + "_Iter_%d.db"%i)


    def update_weight(self, current_global_vector, gold_global_vector):
        # otherwise, the gold_global_vector will change because of the change in weights
        self.w_vector.data_dict.iadd(gold_global_vector.feature_dict)
        self.w_vector.data_dict.iaddc(current_global_vector.feature_dict, -1)
        return
       
