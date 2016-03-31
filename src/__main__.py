from data.data_pool import *

from evaluate.evaluator import *

from weight.weight_vector import *

import debug.debug
import debug.interact

import timeit
import time
import glm_parser

def get_class_from_module(attr_name, module_path, module_name,
                          silent=False):
    """
    This procedure is used by argument processing. It returns a class object
    given a module path and attribute name.

    Basically what it does is to find the module using module path, and then
    iterate through all objects inside that module's namespace (including those
    introduced by import statements). For each object in the name space, this
    function would then check existence of attr_name, i.e. the desired interface
    name (could be any attribute fetch-able by getattr() built-in). If and only if
    one such desired interface exists then the object containing that interface
    would be returned, which is mostly a class, but could theoretically be anything
    object instance with a specified attribute.

    If import error happens (i.e. module could not be found/imported), or there is/are
    no/more than one interface(s) existing, then exception will be raised.

    :param attr_name: The name of the desired interface
    :type attr_name: str
    :param module_path: The path of the module. Relative to src/
    :type module_path: str
    :param module_name: Name of the module e.g. file name
    :type module_name: str
    :param silent: Whether to report existences of interface objects
    :return: class object
    """
    # Load module by import statement (mimic using __import__)
    # We first load the module (i.e. directory) and then fetch its attribute (i.e. py file)
    module_obj = getattr(__import__(module_path + '.' + module_name,
                                    globals(),   # Current global
                                    locals(),    # Current local
                                    [],          # I don't know what is this
                                    -1), module_name)
    intf_class_count = 0
    intf_class_name = None
    for obj_name in dir(module_obj):
        if hasattr(getattr(module_obj, obj_name), attr_name):
            intf_class_count += 1
            intf_class_name = obj_name
            if silent is False:
                print("Interface object %s detected\n\t with interface %s" %
                      (obj_name, attr_name))
    if intf_class_count < 1:
        raise ImportError("Interface object with attribute %s not found" % (attr_name, ))
    elif intf_class_count > 1:
        raise ImportError("Could not resolve arbitrary on attribute %s" % (attr_name, ))
    else:
        class_obj = getattr(module_obj, intf_class_name)
        return class_obj


MAJOR_VERSION = 1
MINOR_VERSION = 0


if __name__ == "__main__":
    import getopt, sys
    
    train_regex = ''
    test_regex = ''
    max_iter = 1
    test_data_path = "../../penn-wsj-deps/"  #"./penn-wsj-deps/"
    l_filename = None
    d_filename = None
    dump_freq = 1
    parallel_flag = False
    shards_number = 1

    # Default learner
    #learner = AveragePerceptronLearner
    learner = get_class_from_module('sequential_learn', 'learn', 'average_perceptron',
                                    silent=True)
    # Default feature generator (2dnd, english)
    fgen = get_class_from_module('get_local_vector', 'feature', 'english_2nd_fgen',
                                 silent=True)
    parser = get_class_from_module('parse', 'parse', 'ceisner3',
                                   silent=True)
    # Default config file: penn2malt
    config = 'config/penn2malt.txt'
    # parser = parse.ceisner3.EisnerParser
    # Main driver is glm_parser instance defined in this file
    glm_parser = glm_parser.GlmParser

    try:
        opt_spec = "aht:i:p:l:d:f:r:s:"
        long_opt_spec = ['train=','test=','fgen=', 
             'learner=', 'parser=', 'config=', 'debug-run-number=',
                         'force-feature-order=', 'interactive',
                         'log-feature-request',"spark"]
        opts, args = getopt.getopt(sys.argv[1:], opt_spec, long_opt_spec)
        for opt, value in opts:
            if opt == "-h":
                print("")
                print("Global Linear Model (GLM) Parser")
                print("Version %d.%d" % (MAJOR_VERSION, MINOR_VERSION))
                print(HELP_MSG)
                sys.exit(0)
            elif opt == "-s":
                shards_number = int(value)
                parallel_flag = True
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
            elif opt == '-f':
                dump_freq = int(value)
            elif opt == '--train':
                train_regex = value
            elif opt == '--test':
                test_regex = value
            elif opt == '--debug-run-number':
                debug.debug.run_first_num = int(value)
                if debug.debug.run_first_num <= 0:
                    raise ValueError("Illegal integer: %d" %
                                     (debug.debug.run_first_num, ))
                else:
                    print("Debug run number = %d" % (debug.debug.run_first_num, ))
            elif opt =="--spark":
                parallel_flag = True
            elif opt == "--learner":
                if parallel_flag:
                    learner = get_class_from_module('parallel_learn', 'learn', value)
                else:
                    learner = get_class_from_module('sequential_learn', 'learn', value)
                print("Using learner: %s (%s)" % (learner.__name__, value))
            elif opt == "--fgen":
                fgen = get_class_from_module('get_local_vector', 'feature', value)
                print("Using feature generator: %s (%s)" % (fgen.__name__, value))
            elif opt == "--parser":
                parser = get_class_from_module('parse', 'parse', value)
                print("Using parser: %s (%s)" % (parser.__name__, value))
            elif opt == '--interactive':
                glm_parser.sequential_train = debug.interact.glm_parser_sequential_train_wrapper
                glm_parser.evaluate = debug.interact.glm_parser_evaluate_wrapper
                glm_parser.compute_argmax = debug.interact.glm_parser_compute_argmax_wrapper
                DataPool.get_data_list = debug.interact.data_pool_get_data_list_wrapper
                learner.sequential_learn = debug.interact.average_perceptron_learner_sequential_learn_wrapper
                print("Enable interactive mode")
            elif opt == '--log-feature-request':
                debug.debug.log_feature_request_flag = True
                print("Enable feature request log")
            elif opt == '--config':
                config = value;
            else:
                print "Invalid argument, try -h"
                sys.exit(0)
              
        gp = glm_parser(train_regex, test_regex, data_path=test_data_path, l_filename=l_filename,
                        learner=learner,
                        fgen=fgen,
                        parser=parser,
                        config=config,
                        spark = parallel_flag)

        training_time = None


        if train_regex is not '':
            start_time = time.time()
            if parallel_flag:
                parallel_learn = get_class_from_module('parallel_learn', 'learn', 'spark_train') 
                gp.parallel_train(train_regex,max_iter,shards_number,pl=parallel_learn)
            else: 
                gp.sequential_train(train_regex, max_iter, d_filename, dump_freq)
            end_time = time.time()
            training_time = end_time - start_time
            print "Total Training Time: ", training_time

        if test_regex is not '':
            print "Evaluating..."
            gp.evaluate(training_time, test_regex)

    except getopt.GetoptError, e:
        print("Invalid argument. \n")
        print(HELP_MSG)
        # Make sure we know what's the error
        raise
