from data.data_pool import *
from evaluate.evaluator import *
from weight.weight_vector import *

import debug.debug
import debug.interact

import timeit

"""
This is the entry for unit testing.

All testing files should satisfy:
 - locate in the test folder
 - be a .py file starts with 'test_'
 - contain a test class start with 'Test'
 - the test class should contain a method: run_test(self, fgen, parser, learner, data_pool)

"""
def get_class_from_module(attr_name, module_path, module_name,
                          silent=False):
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


if __name__ == "__main__":
    import os

    # Default learner
    #learner = AveragePerceptronLearner
    learner = get_class_from_module('sequential_learn', 'learn', 'average_perceptron', silent=True)
    # Default feature generator (2dnd, english)
    fgen = get_class_from_module('get_local_vector', 'feature', 'english_2nd_fgen', silent=True)
    parser = get_class_from_module('parse', 'parse', 'ceisner3', silent=True)

    #default data section: section 2
    data_section = [2]
    data_path = "../../penn-wsj-deps/"

    test_count = 0
    pass_count = 0
    for filename in os.listdir('test'):
        if filename.endswith('.py') and filename.startswith('test_'):
            print "***********************************************"
            print "Test: %d" % (test_count)

            test_obj = get_class_from_module('run_test', 'test', filename[:-3], silent=True)
            if hasattr(test_obj, "fgen_name"):
                fgen = get_class_from_module('get_local_vector', 'feature', test.fgen_name, silent=True)
            if hasattr(test_obj, "parser_name"):
                parser = get_class_from_module('parse', 'parse', test.parser_name, silent=True)
            if hasattr(test_obj, "learner_name"):
                parser = get_class_from_module('parse', 'parse', test.learner_name, silent=True)

            data_pool = DataPool(data_section, data_path, fgen)
            test = test_obj()
            test_res = test.run_test(fgen, parser, learner, data_pool)

            if test_res:
                result = "Pass"
                pass_count = pass_count + 1
            else:
                result = "Fail"

            print "result: ", result
            print
            test_count = test_count+1

    if test_count == pass_count:
        total_result = "PASS"
    else:
        total_result = "FAIL"
    print "***********************************************"
    print "*         Test Result: %s                      " % total_result
    print "* Run Tests: %d                                " % test_count
    print "* Pass Tests: %d                               " % pass_count
    print "***********************************************"



