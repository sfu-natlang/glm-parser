# -*- coding: utf-8 -*-
from data import data_pool
from parse import ceisner
from learn import perceptron
from evaluate import evaluator

class GlmParser():
    def __init__(self, train_section=[], test_section=[], data_path="./penn-wsj-deps/", max_iter=1):

        self.max_iter = max_iter
        
        self.train_data_pool = data_pool.DataPool(train_section, data_path)
        self.test_data_pool = data_pool.DataPool(test_section, data_path)
        self.parser = ceisner.EisnerParser()
        self.learner = perceptron.PerceptronLearner()
        self.evaluator = evaluator.Evaluator()
        

    def sequential_train(self, max_iter=-1):

        print "Starting sequantial train..."
        
        if max_iter < 0:
            max_iter = self.max_iter

        for i in range(max_iter):
            while self.train_data_pool.has_next_data():
                self.learner.learn(
                    self.train_data_pool.get_next_data(),
                    self.parser)

    def evaluate(self, test_section=[]):
        if not test_section == []:
            test_data_pool = data_pool.DataPool(test_section, data_path)
        else:
            test_data_pool = self.test_data_pool

        self.evaluator.evaluate(test_data_pool, self.parser, self.learner.fset)
        



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
    
"""

if __name__ == "__main__":
    import getopt, sys
    
    train_begin = 2
    train_end = 2
    testsection = [2]
    
    test_data_path = "../../../penn-wsj-deps/"  #"./penn-wsj-deps/"

    try:
        opt_spec = "hb:e:t:d:o:p:"
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
            else:
                print "invalid input, see -h"
                sys.exit(0)
                
        gp = GlmParser([(train_begin,train_end)], testsection, test_data_path)
        gp.sequential_train()
        gp.evaluate()

    except getopt.GetoptError, e:
        print "invalid arguments!! \n" + HELP_MSG
        sys.exit(1)

#############################################################################
#    Old GLM-Parser
#############################################################################
"""
from backend import data_set, dependency_tree
from feature import feature_set
from learn import weight_learner
from evaluate import evaluator

class GlmParserOld():
    def __init__(self, filename=None):
        self.evlt = evaluator.Evaluator()
        self.fset = feature_set.FeatureSet(
                    dependency_tree.DependencyTree())
        if filename != None:
            self.fset.load(filename)
        return
    
    def get_evaluator(self):
        return self.evlt

    def set_feature_set(self, fset):
        self.fset = fset
        return
    
    def train(self, section_set=[(2,21)], data_path=None, output_file="weight", dump=True):
        w_learner = weight_learner.WeightLearner(self.fset)
        self.fset = w_learner.learn_weight_sections(section_set, data_path, output_file, dump)
        return
    
    def unlabeled_accuracy(self, section_set=[0,1,22,24], data_path=None):
        dataset = data_set.DataSet(section_set, data_path)
        #evlt = evaluator.Evaluator()
        self.evlt.reset()
        while dataset.has_next_data():
            dep_tree = dataset.get_next_data()
            gold_edge_set = \
                set([(head_index,dep_index) for head_index,dep_index,_ in dep_tree.get_edge_list()])
            
            self.fset.switch_tree(dep_tree)
            sent_len = len(dep_tree.get_word_list())
            test_edge_set = \
               ceisner.EisnerParser().parse(sent_len, self.fset.get_edge_score)
             
            #print "sent acc:", 
            self.evlt.unlabeled_accuracy(test_edge_set, gold_edge_set, True)
            #print "acc acc:", self.evlt.get_acc_unlabeled_accuracy()
        return self.evlt.get_acc_unlabeled_accuracy()
               
"""            
################################################################################
# script for testing glm parser -- old
################################################################################
#HELP_MSG =\
"""

script for train and test glm_parser

options:
    -h:     help message
    
    -b:     begining section of training data
    -e:     ending section of training data
    (   training would not be processed
        unless both begin and ending section is specfied    )

    -a:     list of sections that should be used in accuracy testing
            please seperate the sections with ','
            i.e.  "-a 1,2,3,4,55"
    (   accuracy test would not be processed
        if testing sections are not specified   )
    
    -d:     name of the db file to load for parsing
    -o:     prefix of the name of the output file
            default: "weight"
            the name would be prefix + iteration number
            i.e. "weight_iter_0.db"
    -t:     test data path, default: "./penn-wsj-deps/" 
    
"""
"""
if __name__ == "__main__":
    import getopt, sys
    db_name = None
    train = False
    test = False
    train_begin = -1
    train_end = -1
    #trainsection = [(2,21)]
    #testsection = [0,1,22,24]
    output_file = "weight"
    test_data_path = "./penn-wsj-deps/"
    try:
        opt_spec = "hb:e:a:d:o:t:"
        opts, args = getopt.getopt(sys.argv[1:], opt_spec)
        for opt, value in opts:
            if opt == "-h":
                print HELP_MSG
                sys.exit(0)
            elif opt == "-b":
                train_begin = int(value)
            elif opt == "-e":
                train_end = int(value)
            elif opt == "-a":
                testsection = [int(sec) for sec in value.split(',')]
                test = True
            elif opt == "-d":
                db_name = value
            elif opt == "-o":
                output_file = value
            elif opt == "-t":
                test_data_path = value
            else:
                print "invalid input, see -h"
                sys.exit(0)
                
        if train_begin >= 0 and train_end >= 0:
            trainsection = [(train_begin, train_end)]
            train = True
            
        gp = GlmParser(db_name)
        if train:
            print output_file, trainsection
            gp.train(trainsection, test_data_path, output_file)
        if test:
            print gp.unlabeled_accuracy(testsection, test_data_path)
    except getopt.GetoptError, e:
        print "invalid arguments!! \n" + HELP_MSG
        sys.exit(1)
"""
