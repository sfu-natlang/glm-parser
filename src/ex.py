
import os,sys,inspect
from os import listdir
from os.path import isfile, join, isdir
from data import data_pool
from pyspark import SparkContext
from feature import english_1st_fgen
from learn import readTrainData
N = 2 # number of shards


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


if __name__ == '__main__':
	#fgen = get_class_from_module('get_local_vector', 'feature', 'english_1st_fgen',silent=True)
	fgen = english_1st_fgen.FirstOrderFeatureGenerator
	parser = get_class_from_module('parse', 'parse', 'ceisner',
                                   silent=True)
	sl = readTrainData.Learner(fgen,parser)
	#data_path = "/Users/vivian/data/penn-wsj-deps/"
	#count = count_sent(data_path, "sec")
	#print count
	#output_dir = "/Users/vivian/data/shards/"
	#partition_data(data_path,count,output_dir)
	#count = sl.count_sent(output_dir, "file")
	#print count
	output_dir = "/Users/vivian/data/shards/"
	sl.spark_train(output_dir,1)
	


