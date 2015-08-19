# -*- coding: utf-8 -*-
import logging

logging.basicConfig(filename='glm_parser.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

class PerceptronLearner():

    def __init__(self, w_vector, max_iter=1):
        logging.debug("Initialize PerceptronLearner ... ")
        self.w_vector = w_vector
        self.max_iter = max_iter
        return

    def sequential_learn(self, f_argmax, data_pool=None, max_iter=-1, d_filename=None, dump_freq = 1):
        if max_iter <= 0:
            max_iter = self.max_iter
            
        logging.debug("Starting sequantial train...")
        for i in range(max_iter):
            logging.debug("Iteration: %d" % i)
            logging.debug("Data size: %d" % len(data_pool.data_list))
 
            while data_pool.has_next_data():
                data_instance = data_pool.get_next_data()
                gold_global_vector = data_instance.gold_global_vector
                current_global_vector = f_argmax(data_instance)
                self.update_weight(current_global_vector, gold_global_vector)

            data_pool.reset_index()
            if d_filename is not None:
                if t % dump_freq == 0 or t == max_iter - 1:
                    self.w_vector.dump(d_filename + "_Iter_%d.db"%i)


    def update_weight(self, current_global_vector, gold_global_vector):
        # otherwise, the gold_global_vector will change because of the change in weights
        self.w_vector.data_dict.iadd(gold_global_vector.feature_dict)
        self.w_vector.data_dict.iaddc(current_global_vector.feature_dict, -1)
        return
       
