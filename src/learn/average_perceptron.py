from __future__ import division
import logging
from hvector._mycollections import mydefaultdict
from hvector.mydouble import mydouble

logging.basicConfig(filename='glm_parser.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

class AveragePerceptronLearner():

    def __init__(self, w_vector, max_iter=1):
        logging.debug("Initialize AveragePerceptronLearner ... ")
        self.w_vector = w_vector
        self.max_iter = max_iter
        
        self.weight_sum_dict = mydefaultdict(mydouble)
        self.last_change_dict = mydefaultdict(mydouble)
        self.c = 1
        return

    def sequential_learn(self, f_argmax, data_pool, max_iter=-1, d_filename=None):
        if max_iter <=0:
            max_iter = self.max_iter

        logging.debug("Starting sequential train ... ")

        # sigma_s
        self.weight_sum_dict.clear()
        self.last_change_dict.clear()
        self.c = 1

        # for t = 1 ... T
        for t in range(max_iter): 
            logging.debug("Iteration: %d" % t)
            logging.debug("Data size: %d" % len(data_pool.data_list))

            # for i = 1 ... m
            while data_pool.has_next_data():
            #for k in range(2):
                
                # Calculate yi' = argmax
                data_instance = data_pool.get_next_data()
                gold_global_vector = data_instance.gold_global_vector
                current_global_vector = f_argmax(data_instance)
                delta_global_vector = gold_global_vector - current_global_vector
                
                # if t != T or i != m
                if not t == max_iter-1 or data_pool.has_next_data():

                    # i yi' != yi
                    if not current_global_vector == gold_global_vector:
                        # for each dimension s in delta_global_vector 
                        for s in delta_global_vector.keys():
                            self.weight_sum_dict[s] += self.w_vector[s] * (self.c - self.last_change_dict[s])
                            self.last_change_dict[s] += 1
                        
                        # update weight and weight sum
                        self.w_vector.data_dict.iadd(delta_global_vector.feature_dict)
                        self.weight_sum_dict.iadd(delta_global_vector.feature_dict)
                        self.c += 1
                else:
                    for s in self.last_change_dict.keys():
                        self.weight_sum_dict[s] += self.w_vector[s] * (self.c - self.last_change_dict[s])

                    if not current_global_vector == gold_global_vector:
                        self.w_vector.data_dict.iadd(delta_global_vector.feature_dict)
                        self.weight_sum_dict.iadd(delta_global_vector.feature_dict)

            data_pool.reset()
        
        self.w_vector.data_dict.clear()
        self.w_vector.data_dict.iaddc(self.weight_sum_dict, 1/self.c)
        
        return
                     
