# -*- coding: utf-8 -*-
from data.data_pool import *
from parse.ceisner import *
from learn.perceptron import *
from learn.average_perceptron import *
from evaluate.evaluator import *

from weight.weight_vector import *
import timeit

class GlmParser():
    def __init__(self, train_section=[], test_section=[], data_path="./penn-wsj-deps/",
                 l_filename=None, max_iter=1):

        self.max_iter = max_iter

        self.w_vector = WeightVector(l_filename)
        
        self.train_data_pool = DataPool(train_section, data_path)
        self.test_data_pool = DataPool(test_section, data_path)
        
        self.parser = EisnerParser()
        self.learner = PerceptronLearner(self.w_vector, max_iter)
        self.evaluator = Evaluator()
        
    def sequential_train(self, train_section=[], max_iter=-1, d_filename=None):
        if not train_section == []:
            train_data_pool = data_pool.DataPool(train_section, data_path)
        else:
            train_data_pool = self.train_data_pool
            
        if max_iter == -1:
            max_iter = self.max_iter
            
        self.learner.sequential_learn(self.compute_argmax, train_data_pool, max_iter, d_filename)
    
    def evaluate(self, test_section=[]):
        if not test_section == []:
            test_data_pool = data_pool.DataPool(test_section, data_path)
        else:
            test_data_pool = self.test_data_pool

        self.evaluator.evaluate(test_data_pool, self.parser, self.w_vector)
        
    def compute_argmax(self, sentence):
        current_edge_set = self.parser.parse(sentence, self.w_vector.get_vector_score)
        current_global_vector = sentence.get_global_vector(current_edge_set)

        return current_global_vector

HELP_MSG =\
"""

script for train and test glm_parser

options:
    -h:     help message
    
    -b:     begining section of training data
    -e:     ending section of training data
    (   training would not be processed
        unless both begin and ending section is specfied    )

    -t:     test sections
            list of sections that should be used in accuracy testing
            please seperate the sections with ','
            i.e.  "-t 1,2,3,4,55"
    (   accuracy test would not be processed
        if testing sections are not specified   )
    
    -p:     test data path, default: "./penn-wsj-deps/"

    -l:     path to load weight vector file
            (Including full name, i.e. Weight.db)
            
    -d:     path to dump weight vector file
            (Including prefix of name
            i.e. Weight, the file name would be Weight_Iter_1.db)
    
"""

if __name__ == "__main__":
    import getopt, sys
    
    train_begin = 2
    train_end = 2
    testsection = [2]
    max_iter = 1
    test_data_path = "../../../penn-wsj-deps/"  #"./penn-wsj-deps/"
    l_filename = None
    d_filename = None

    try:
        opt_spec = "hb:e:t:i:p:l:d:"
        opts, args = getopt.getopt(sys.argv[1:], opt_spec)
        for opt, value in opts:
            if opt == "-h":
                print HELP_MSG
                sys.exit(0)
            elif opt == "-b":
                train_begin = int(value)
            elif opt == "-e":
                train_end = int(value)
            elif opt == "-t":
                testsection = [int(sec) for sec in value.split(',')]
                test = True
            elif opt == "-p":
                test_data_path = value
            elif opt == "-i":
                max_iter = int(value)
            elif opt == "-l":
                l_filename = value
            elif opt == "-d":
                d_filename = value
            else:
                print "invalid input, see -h"
                sys.exit(0)
                
        gp = GlmParser([(train_begin,train_end)], testsection, test_data_path, l_filename)
        #start = timeit.default_timer()
        #gp.sequential_train(max_iter=max_iter, d_filename=d_filename)
        #end = timeit.default_timer()
        #print end - start
        gp.evaluate()

    except getopt.GetoptError, e:
        print "invalid arguments!! \n" + HELP_MSG
        sys.exit(1)

