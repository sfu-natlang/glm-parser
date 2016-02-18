from __future__ import division
import logging
import multiprocessing
from hvector._mycollections import mydefaultdict
from hvector.mydouble import mydouble
from weight.weight_vector import *
from data.data_pool import *
# Time accounting and control
import debug.debug
import time
import sys

from pyspark import SparkContext


logging.basicConfig(filename='glm_parser.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

class ParallelPerceptronLearner():

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

    def set_section_list(self, section_set):
        """
        Initialize self.section_list as a list containing section
        numbers that we are going to use for training

        Argument section_set is a list of tuples or integers:

        +------------------------------------------------------+
        |   tuples    representing the range of the section,   |
        |             i.e. (1,3) means range 1,2,3             |
        |------------------------------------------------------|
        |   int       single section number                    |
        +------------------------------------------------------+

        :param section_set: the sections to be used
        :type section_set: list(tuple/int)
        """
        # First get all sections that are specified using integers
        section_list = [section for section in section_set if isinstance(section, int)]

            # Then, make all tuple (x, y) a list [x, x + 1, .. , y]
        section_sets = \
            map(lambda section_tuple: range(section_tuple[0], section_tuple[1]+1),
                    [st for st in section_set if isinstance(st, tuple)])

        for s_set in section_sets:
            section_list = section_list + s_set

            # We always train using increasing order
        return section_list

    def parallel_learn(self, f_argmax, data_path, train_section=[], max_iter=-1, d_filename=None, fgen=None,parser=None):
        data_list = []
        sentence_count = 0
        if train_section == []:
            train_section= [(0,21)]
        
        train_section = self.set_section_list(train_section)
        sc = SparkContext(appName="iterParameterMixing", master="local[10]")
        train_section = sc.parallelize(train_section).cache()

        # To Do: from perceptron to average perceptron
        def avg_perc_train(train_section,parser,fv,data_path, fgen):
            data_pool = DataPool(train_section, data_path, fgen)
            w_vector = WeightVector()
            for key in fv.keys():
                w_vector.data_dict[key]=fv[key]
            #print data_pool.get_sent_num
            while data_pool.has_next_data():
                sentence = data_pool.get_next_data()
                gold_global_vector = sentence.gold_global_vector
                current_edge_set = parser.parse(sentence, w_vector.get_vector_score)
                sentence.set_current_global_vector(current_edge_set)
                current_global_vector = sentence.current_global_vector
                #current_global_vector = f_argmax(data_instance)
                w_vector.data_dict.iadd(gold_global_vector.feature_dict)
                w_vector.data_dict.iaddc(current_global_vector.feature_dict, -1)
            vector_list = []
            for key in w_vector.data_dict.keys():
                vector_list.append((str(key),w_vector.data_dict[key]))
            
            return vector_list

        fv = {}
        for key in self.w_vector.data_dict.keys():
            fv[str(key)]=w_vector.data_dict[key]
        for round in range(max_iter):
            weight_vector = sc.broadcast(fv)
            feat_vec_list = train_section.mapPartitions(lambda t: avg_perc_train(t,parser,weight_vector.value,data_path,fgen))
            #feat_vec_list = feat_vec_list.reduce(lambda a, b: a + b)
            feat_vec_list = feat_vec_list.combineByKey((lambda x: (x,1)),
                             (lambda x, y: (x[0] + y, x[1] + 1)),
                             (lambda x, y: (x[0] + y[0], x[1] + y[1]))).collect()
            
            for (feat, (a,b)) in feat_vec_list:
                fv[feat] = float(a)/float(b)
        self.w_vector.data_dict.clear()
        self.w_vector.data_dict.iadd(fv)
        sc.stop()

    
