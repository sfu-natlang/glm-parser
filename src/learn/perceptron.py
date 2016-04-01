# -*- coding: utf-8 -*-
import logging
from hvector._mycollections import mydefaultdict
from hvector.mydouble import mydouble
from weight import weight_vector 
from data import data_pool

logging.basicConfig(filename='glm_parser.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

class PerceptronLearner():

    def __init__(self, w_vector=None, max_iter=1):
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
                #data_instance.convert_list_vector_to_dict(data_instance.gold_global_vector)
                gold_global_vector = data_instance.convert_list_vector_to_dict(data_instance.gold_global_vector)
                current_global_vector = f_argmax(data_instance)
                self.update_weight(current_global_vector, gold_global_vector)

            data_pool.reset_index()
            
            if d_filename is not None:
                if i % dump_freq == 0 or i == max_iter - 1:
                    self.w_vector.dump(d_filename + "_Iter_%d.db"%i)


    def update_weight(self, current_global_vector, gold_global_vector):
        # otherwise, the gold_global_vector will change because of the change in weights
        self.w_vector.data_dict.iadd(gold_global_vector.feature_dict)
        self.w_vector.data_dict.iaddc(current_global_vector.feature_dict, -1)
        return

    def parallel_learn(self,dp,fv,parser):
        #dp = data_pool.DataPool(textString=textString[1],fgen=fgen,config_list=config)
        w_vector = weight_vector.WeightVector()
        for key in fv.keys():
            w_vector.data_dict[key]=fv[key]
        #print data_pool.get_sent_num
        while dp.has_next_data():
            data_instance = dp.get_next_data()
            gold_global_vector = data_instance.convert_list_vector_to_dict(data_instance.gold_global_vector)
            current_edge_set = parser.parse(data_instance, w_vector.get_vector_score)
            current_global_vector = data_instance.set_current_global_vector(current_edge_set)
            w_vector.data_dict.iadd(gold_global_vector.feature_dict)
            w_vector.data_dict.iaddc(current_global_vector.feature_dict, -1)

        dp.reset_index()

        vector_list = {}
        for key in w_vector.data_dict.keys():
            vector_list[str(key)] = w_vector.data_dict[key]
    
        return vector_list.items()
       
