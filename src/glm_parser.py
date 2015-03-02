# -*- coding: utf-8 -*-

#
# Global Linear Model Parser
# Simon Fraser University
# NLP Lab
#
# Author: Yulan Huang, Ziqi Wang, Anoop Sarkar
# (Please add on your name if you have authored this file)
#

from parse.ceisner import *
from data.data_pool import *
from learn.perceptron import *
from learn.average_perceptron import *
from evaluate.evaluator import *

from weight.weight_vector import *
import timeit

class GlmParser():
    def __init__(self, train_section=[], test_section=[], data_path="./penn-wsj-deps/",
                 l_filename=None, max_iter=1):

        self.max_iter = max_iter
        self.data_path = data_path

        self.w_vector = WeightVector(l_filename)
        
        self.train_data_pool = DataPool(train_section, data_path)
        self.test_data_pool = DataPool(test_section, data_path)
        
        self.parser = EisnerParser()
        self.learner = AveragePerceptronLearner(self.w_vector, max_iter)
        #self.learner = PerceptronLearner(self.w_vector, max_iter)
        self.evaluator = Evaluator()
       
    def sequential_train(self, train_section=[], max_iter=-1, d_filename=None):
        if not train_section == []:
            train_data_pool = DataPool(train_section, self.data_path)
        else:
            train_data_pool = self.train_data_pool
            
        if max_iter == -1:
            max_iter = self.max_iter
            
        self.learner.sequential_learn(self.compute_argmax, train_data_pool, max_iter, d_filename)
    
    def evaluate(self, test_section=[]):
        if not test_section == []:
            test_data_pool = DataPool(test_section, self.data_path)
        else:
            test_data_pool = self.test_data_pool

        self.evaluator.evaluate(test_data_pool, self.parser, self.w_vector)
        
    def compute_argmax(self, sentence):
        current_edge_set = self.parser.parse(sentence, self.w_vector.get_vector_score)
        current_global_vector = sentence.get_global_vector(current_edge_set)

        return current_global_vector

HELP_MSG =\
"""

options:
    -h:     Print this help message
    
    -b:     Begin section for training
            (You need to specify both begin and end section)

    -e:     End section for training
            (You need to specify both begin and end section)

    -t:     Test sections for evaluation
            Use section id to specify them, separated with comma (,)
            i.e.  "-t 1,2,3,4,55"
            If not specified then no evaluation will be conducted
    
    -p:     Path to data files (to the parent directory for all sections)
            default "./penn-wsj-deps/"

    -l:     Path to an existing weight vector dump file
            example: "./Weight.db"
            
    -d:     Path for dumping weight vector. Do not specify the suffix
            "db" suffix will be automatically added
            example: "./iter1.db"

    -i:     Number of iterations
            default 1
    
"""

MAJOR_VERSION = 1
MINOR_VERSION = 0

if __name__ == "__main__":
    import getopt, sys
    
    train_begin = -1
    train_end = -1
    testsection = []
    max_iter = 1
    test_data_path = "../../../penn-wsj-deps/"  #"./penn-wsj-deps/"
    l_filename = None
    d_filename = None

    try:
        opt_spec = "hb:e:t:i:p:l:d:"
        opts, args = getopt.getopt(sys.argv[1:], opt_spec)
        for opt, value in opts:
            if opt == "-h":
                print("")
                print("Global Linear Model (GLM) Parser")
                print("Version %d.%d" % (MAJOR_VERSION, MINOR_VERSION))
                print(HELP_MSG)
                sys.exit(0)
            elif opt == "-b":
                train_begin = int(value)
            elif opt == "-e":
                train_end = int(value)
            elif opt == "-t":
                testsection = [int(sec) for sec in value.split(',')]
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
                
        gp = GlmParser(data_path=test_data_path, l_filename=l_filename)
        #start = timeit.default_timer()
        if train_begin >= 0 and train_end >= train_begin:
            gp.sequential_train([(train_begin,train_end)], max_iter, d_filename)
        #end = timeit.default_timer()
        #print end - start
        if not testsection == []:
            gp.evaluate(testsection)

    except getopt.GetoptError, e:
        print "invalid arguments!! \n" + HELP_MSG
        sys.exit(1)

