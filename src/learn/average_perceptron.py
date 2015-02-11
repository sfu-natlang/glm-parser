from __future__ import division
import logging
import multiprocessing
from hvector._mycollections import mydefaultdict
from hvector.mydouble import mydouble
from weight.weight_vector import *

logging.basicConfig(filename='glm_parser.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

class AveragePerceptronLearner():

    def __init__(self, w_vector, max_iter=1):
        """
        :param w_vector: A global weight vector instance that stores
         the weight value (float)
        :param max_iter: Maximum iterations for training the weight vector
         Could be overridden by parameter max_iter in the method
        :return: None
        """
        logging.debug("Initialize AveragePerceptronLearner ... ")
        self.w_vector = w_vector
        self.max_iter = max_iter
        
        self.weight_sum_dict = mydefaultdict(mydouble)
        self.last_change_dict = mydefaultdict(mydouble)
        self.c = 1
        return

    def sequential_learn(self, f_argmax, data_pool, max_iter=-1, d_filename=None):
        if max_iter <= 0:
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

                # Calculate yi' = argmax
                data_instance = data_pool.get_next_data()
                gold_global_vector = data_instance.gold_global_vector
                current_global_vector = f_argmax(data_instance)
                delta_global_vector = gold_global_vector - current_global_vector
                
                # update every iteration (more convenient for dump)
                if data_pool.has_next_data():
                    # i yi' != yi
                    if not current_global_vector == gold_global_vector:
                        # for each dimension s in delta_global_vector 
                        for s in delta_global_vector.keys():
                            self.weight_sum_dict[s] += self.w_vector[s] * (self.c - self.last_change_dict[s])
                            self.last_change_dict[s] = self.c
                        
                        # update weight and weight sum
                        self.w_vector.data_dict.iadd(delta_global_vector.feature_dict)
                        self.weight_sum_dict.iadd(delta_global_vector.feature_dict)

                else:
                    for s in self.last_change_dict.keys():
                        self.weight_sum_dict[s] += self.w_vector[s] * (self.c - self.last_change_dict[s])
                        self.last_change_dict[s] = self.c
                        
                    if not current_global_vector == gold_global_vector:
                        self.w_vector.data_dict.iadd(delta_global_vector.feature_dict)
                        self.weight_sum_dict.iadd(delta_global_vector.feature_dict)

                self.c += 1

            # Reset index, while keeping the content intact
            data_pool.reset_index()

            if not d_filename == None:
                p_fork = multiprocessing.Process(
                    target=self.dump_vector,
                    args=(d_filename, t))
                
                p_fork.start()
                #self.w_vector.dump(d_filename + "_Iter_%d.db"%t)
        
        self.w_vector.data_dict.clear()

        self.avg_weight(self.w_vector, self.c - 1)

        return

    def avg_weight(self, w_vector, count):
        if count > 0:
            w_vector.data_dict.iaddc(self.weight_sum_dict, 1 / count)
        
    def dump_vector(self, d_filename, i):
        d_vector = WeightVector()
        self.avg_weight(d_vector, self.c-1)
        d_vector.dump(d_filename + "_Iter_%d.db"%i)
        d_vector.data_dict.clear()
