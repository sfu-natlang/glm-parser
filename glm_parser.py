# -*- coding: utf-8 -*-
import data_set, feature_set, dependency_tree, ceisner
import weight_learner, evaluator

class GlmParser():
    def __init__(self, filename=None):
        self.fset = feature_set.FeatureSet(
                    dependency_tree.DependencyTree())
        if filename != None:
            self.fset.load(filename)
        return
    
    def set_feature_set(self, fset):
        self.fset = fset
        return
    
    def train(self, section_set=[(2,21)], data_path=None, output_file="weight"):
        w_learner = weight_learner.WeightLearner()
        self.fset = w_learner.learn_weight_sections(section_set, data_path, output_file)
        return
    
    def unlabeled_accuracy(self, section_set=[0,1,22,24], data_path=None):
        dataset = data_set.DataSet(section_set, data_path)
        evlt = evaluator.Evaluator()
        evlt.reset()
        while dataset.has_next_data():
            dep_tree = dataset.get_next_data()
            gold_edge_set = \
                set([(head_index,dep_index) for head_index,dep_index,_ in dep_tree.get_edge_list()])
            
            self.fset.switch_tree(dep_tree)
            sent_len = len(dep_tree.get_word_list())
            test_edge_set = \
               ceisner.EisnerParser().parse(sent_len, self.fset.get_edge_score)
             
            print "sent acc:", evlt.unlabeled_accuracy(test_edge_set, gold_edge_set, True)
            print "acc acc:", evlt.get_acc_unlabeled_accuracy()
        return evlt.get_acc_unlabeled_accuracy()
               
              
################################################################################
# script for testing glm parser
################################################################################
HELP_MSG =\
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
