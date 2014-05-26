# -*- coding: utf-8 -*-
import copy

class PerceptronLearner():

    def __init__(self, parser,w_vector, max_iter=1):
        self.parser = parser
        self.w_vector = w_vector
        self.max_iter = max_iter
        return

    def sequential_learn(self, data_pool=None, max_iter=-1, d_filename=None):
        if max_iter <= 0:
            max_iter = self.max_iter
            
        print "Starting sequantial train..."
        for i in range(max_iter):
            print "Iteration:", i
            
            while data_pool.has_next_data():
                self.learn(data_pool.get_next_data())

            data_pool.reset()
            if not d_filename == None:
                self.w_vector.dump(d_filename + "_Iter_%d.db"%i)
            

    def learn(self, sent):
        gold_edge_set = \
            set([(head_index,dep_index) for head_index,dep_index,_ in sent.get_edge_list()])
        current_edge_set = \
               self.parser.parse(sent, self.w_vector.get_vector_score)

        if current_edge_set == gold_edge_set:
            return

        # calculate the global score
        gold_global_vector = sent.gold_global_vector
        current_global_vector = sent.get_global_vector(current_edge_set)

        #start = timeit.default_timer()
        self.update_weight(current_global_vector, gold_global_vector)
        #end = timeit.default_timer()

        #print end - start

    def update_weight(self, current_global_vector, gold_global_vector):
        # otherwise, the gold_global_vector will change because of the change in weights
        self.w_vector.data_dict.iadd(gold_global_vector.feature_dict)
        self.w_vector.data_dict.iaddc(current_global_vector.feature_dict, -1)
        return
       
