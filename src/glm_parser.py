# -*- coding: utf-8 -*-

#
# Global Linear Model Parser
# Simon Fraser University
# NLP Lab
#
# Author: Yulan Huang, Ziqi Wang, Anoop Sarkar
# (Please add on your name if you have authored this file)
#

import parse.ceisner
import parse.ceisner3

from data.data_pool import *
from learn.perceptron import *

from learn.average_perceptron import AveragePerceptronLearner
from learn.perceptron import PerceptronLearner

from evaluate.evaluator import *

from weight.weight_vector import *

import debug.debug
import debug.interact

import timeit

class GlmParser():
    def __init__(self, train_section=[], test_section=[], data_path="./penn-wsj-deps/",
                 l_filename=None, max_iter=1,
                 learner=None,
                 fgen=None,
                 parser=None):

        self.max_iter = max_iter
        self.data_path = data_path

        self.w_vector = WeightVector(l_filename)

        if fgen is not None:
            # Do not instanciate this; used elsewhere
            self.fgen = fgen
        else:
            raise ValueError("You need to specify a feature generator")
        
        self.train_data_pool = DataPool(train_section, data_path, fgen=self.fgen)
        self.test_data_pool = DataPool(test_section, data_path, fgen=self.fgen)
        
        self.parser = parser()

        if learner is not None:
            self.learner = learner(self.w_vector, max_iter)
            #self.learner = PerceptronLearner(self.w_vector, max_iter)
        else:
            raise ValueError("You need to specify a learner")

        self.evaluator = Evaluator()
       
    def sequential_train(self, train_section=[], max_iter=-1, d_filename=None):
        if not train_section == []:
            train_data_pool = DataPool(train_section, self.data_path, fgen=self.fgen)
        else:
            train_data_pool = self.train_data_pool
            
        if max_iter == -1:
            max_iter = self.max_iter
            
        self.learner.sequential_learn(self.compute_argmax, train_data_pool, max_iter, d_filename)
    
    def evaluate(self, test_section=[]):
        if not test_section == []:
            test_data_pool = DataPool(test_section, self.data_path, fgen=self.fgen)
        else:
            test_data_pool = self.test_data_pool

        self.evaluator.evaluate(test_data_pool, self.parser, self.w_vector)
        
    def compute_argmax(self, sentence):
        current_edge_set = self.parser.parse(sentence, self.w_vector.get_vector_score)
        sentence.set_current_global_vector(current_edge_set)
        current_global_vector = sentence.current_global_vector

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
            
    -d:     Path for dumping weight vector. Please also specify a prefix
            of file names, which will be added with iteration count and
            ".db" suffix when dumping the file

            example: "./weight_dump", and the resulting files could be:
            "./weight_dump_Iter_1.db",
            "./weight_dump_Iter_2.db"...

    -i:     Number of iterations
            default 1

    -a:     Turn on time accounting (output time usage for each sentence)
            If combined with --debug-run-number then before termination it also
            prints out average time usage

    --learner=
            Specify a learner for weight vector training
                "perceptron": Use simple perceptron
                "avg_perceptron": Use average perceptron
            default "avg_perceptron"

    --fgen=
            Specify feature generation facility by a python file name (mandatory).
            The file will be searched under /feature directory, and the class
            object that has a get_local_vector() interface will be recognized
            as the feature generator and put into use automatically.

            If multiple eligible objects exist, an error will be reported.

            For developers: please make sure there is only one such class object
            under fgen source files. Even import statement may introduce other
            modules that is eligible to be a fgen. Be careful.

    --parser=
            Specify the parser
                "1st-order" First order parser
                "3rd-order" Third order parser
            default "1st-order"
            Some parser might not work correctly with the infrastructure, which keeps
            changing all the time. If this happens please file an issue on github page

    --debug-run-number=[int]
            Only run the first [int] sentences. Usually combined with option -a to gather
            time usage information
            If combined with -a, then time usage information is available, and it will print
            out average time usage before termination
            *** Caution: Overrides -t (no evaluation will be conducted), and partially
            overrides -b -e (Only run specified number of sentences)

    --interactive
            Use interactive version of glm-parser, in which you have access to some
            critical points ("breakpoints") in the procedure

    --log-feature-request
            Log each feature request based on feature type. This is helpful for
            analyzing feature usage and building feature caching utility.
            Upon exiting the main program will dump feature request information
            into a file "feature_request.log"
    
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

    # Default learner
    learner = AveragePerceptronLearner
    fgen = None
    parser = parse.ceisner3.EisnerParser
    # Main driver is glm_parser instance defined in this file
    glm_parser = GlmParser

    try:
        opt_spec = "ahb:e:t:i:p:l:d:"
        long_opt_spec = ['fgen=', 'learner=', 'parser=', 'debug-run-number=',
                         'force-feature-order=', 'interactive',
                         'log-feature-request']
        opts, args = getopt.getopt(sys.argv[1:], opt_spec, long_opt_spec)
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
            elif opt == '-a':
                print("Time accounting is ON")
                debug.debug.time_accounting_flag = True
            elif opt == '--debug-run-number':
                debug.debug.run_first_num = int(value)
                if debug.debug.run_first_num <= 0:
                    raise ValueError("Illegal integer: %d" %
                                     (debug.debug.run_first_num, ))
                else:
                    print("Debug run number = %d" % (debug.debug.run_first_num, ))
            elif opt == "--learner":
                if value == 'perceptron':
                    learner = PerceptronLearner
                    print("Using perceptron learner")
                elif value == 'avg_perceptron':
                    learner = AveragePerceptronLearner
                    print("Using average perceptron learner")
                else:
                    raise ValueError("Unknown learner: %s" % (value, ))
            elif opt == "--fgen":
                root = 'feature.'
                module = getattr(__import__(root + value, globals(), locals(), [], -1), value)
                class_count = 0
                class_name = None
                for obj_name in dir(module):
                    if hasattr(getattr(module, obj_name), 'get_local_vector'):
                        class_count += 1
                        class_name = obj_name
                        print("Feature generator detected: %s" % (obj_name, ))
                if class_count < 1:
                    raise ValueError("No feature generator found!")
                elif class_count > 1:
                    raise ValueError("Found multiple feature generator!")
                else:
                    fgen = getattr(module, class_name)
                    print("Using feature generator: %s" % (class_name, ))
            elif opt == "--parser":
                if value == '1st-order':
                    parser = parse.ceisner.EisnerParser
                    print("Using first order Eisner parser")
                elif value == "3rd-order":
                    parser = parse.ceisner3.EisnerParser
                    print("Using third order Eisner parser")
                else:
                    raise ValueError("Unknown parser: %s" % (value, ))
            elif opt == '--interactive':
                glm_parser.sequential_train = debug.interact.glm_parser_sequential_train_wrapper
                glm_parser.evaluate = debug.interact.glm_parser_evaluate_wrapper
                glm_parser.compute_argmax = debug.interact.glm_parser_compute_argmax_wrapper
                DataPool.get_data_list = debug.interact.data_pool_get_data_list_wrapper
                learner.sequential_learn = debug.interact.average_perceptron_learner_sequential_learn_wrapper
                print("Enable interactive mode")
            elif opt == '--log-feature-request':
                debug.debug.log_feature_request_flag = True
                print("Enable feature reuqest log")
            else:
                print "Invalid argument, try -h"
                sys.exit(0)
                
        gp = glm_parser(data_path=test_data_path, l_filename=l_filename,
                        learner=learner,
                        fgen=fgen,
                        parser=parser)

        if train_end >= train_begin >= 0:
            gp.sequential_train([(train_begin, train_end)], max_iter, d_filename)

        if not testsection == []:
            gp.evaluate(testsection)

    except getopt.GetoptError, e:
        print("Invalid argument. \n")
        print(HELP_MSG)
        # Make sure we know what's the error
        raise

