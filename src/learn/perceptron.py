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

class Learner():

    def __init__(self, w_vector=None, max_iter=1):
        self.name = "PerceptronLearner"
        """
        :param w_vector: A global weight vector instance that stores
         the weight value (float)
        :param max_iter: Maximum iterations for training the weight vector
         Could be overridden by parameter max_iter in the method
        :return: None
        """
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
                current_global_vector = f_argmax(self.w_vector, data_instance)
                self.update_weight(current_global_vector, gold_global_vector)

            data_pool.reset_index()

            if d_filename is not None:
                if i % dump_freq == 0 or i == max_iter - 1:
                    self.w_vector.dump(d_filename + "_Iter_%d.db"%i)
        return self.w_vector


    def update_weight(self, current_global_vector, gold_global_vector):
        # otherwise, the gold_global_vector will change because of the change in weights
        self.w_vector.iadd(gold_global_vector.feature_dict)
        self.w_vector.iaddc(current_global_vector.feature_dict, -1)
        return

    def parallel_learn(self, dp, fv, f_argmax):
        #dp = data_pool.DataPool(textString=textString[1],fgen=fgen,format_list=format)
        w_vector = weight_vector.WeightVector()
        for key in fv.keys():
            w_vector[key]=fv[key]
        #print data_pool.get_sent_num
        while dp.has_next_data():
            data_instance = dp.get_next_data()
            gold_global_vector = data_instance.convert_list_vector_to_dict(data_instance.gold_global_vector)
            current_global_vector = f_argmax(w_vector, data_instance)

            w_vector.iadd(gold_global_vector.feature_dict)
            w_vector.iaddc(current_global_vector.feature_dict, -1)

        dp.reset_index()

        vector_list = {}
        for key in w_vector.keys():
            vector_list[str(key)] = w_vector[key]

        return vector_list.items()
