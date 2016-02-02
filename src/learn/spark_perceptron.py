from __future__ import division
import logging
import multiprocessing
from hvector._mycollections import mydefaultdict
from hvector.mydouble import mydouble
from weight.weight_vector import *
# Time accounting and control
import debug.debug
import time
import sys

from pyspark import SparkContext


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
        return

    def parallel_learn(self, f_argmax, data_pool=None, max_iter=-1, d_filename=None, dump_freq=1):
                # sigma_s
        self.weight_sum_dict.clear()
        self.last_change_dict.clear()
        self.c = 1

        data_list = []
        sentence = 0
        while data_pool.has_next_data():
            sentence_count+=1
            data = dp.get_next_data()
            data_list.append(data)

        sc = SparkContext(appName="iterParameterMixing")
        train_data = sc.parallelize(data_list).cache()
        def avg_perc_train(train_data,w_vector,f_argmax):
            while train_data.has_next_data():
                data_instance = data_pool.get_next_data()
                gold_global_vector = data_instance.gold_global_vector
                current_global_vector = f_argmax(data_instance)
                        # otherwise, the gold_global_vector will change because of the change in weights
                w_vector.data_dict.iadd(gold_global_vector.feature_dict)
                w_vector.data_dict.iaddc(current_global_vector.feature_dict, -1)
            return weight_vector.items()
        for round in range(0,epochs):
            fv = {}
            weight_vector = self.w_vector
            feat_vec_list = train_data.mapPartitions(lambda t: avg_perc_train(t, weight_vector))
            feat_vec_list = feat_vec_list.combineByKey((lambda x: (x,1)),
                             (lambda x, y: (x[0] + y, x[1] + 1)),
                             (lambda x, y: (x[0] + y[0], x[1] + y[1]))).collect()
            self.w_vector.data_dict.clear()
            for (feat, (a,b)) in feat_vec_list:
                fv[feat] = float(a)/float(b)
            self.w_vector.data_dict.iadd(fv)
        sc.stop()

    
