#
# Global Linear Model Parser
# Simon Fraser University
# NLP Lab
#
# Author: Yulan Huang, Ziqi Wang, Anoop Sarkar
# (Please add on your name if you have authored this file)
#

#import cPickle as pickle
import sys

from debug.debug import local_debug_flag

if local_debug_flag is False:
    from hvector._mycollections import mydefaultdict
    from hvector.mydouble import mydouble
else:
    print("Local debug is on. Use dict() and float()")
    mydefaultdict = dict
    mydouble = float

import logging

logging.basicConfig(filename='glm_parser.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

class WeightVector():
    """
    A dictitionary-like object. Used to facilitate class FeatureSet to
    store the features.

    Callables inside the class:
              
    dump()  - Dump the content of the data object into memory. When we are using
              memory dict it will call Pickle to do that. When we are using

    load()  - Load the content of a disk file into the memory. When we are using
              memory dict it will call Pickle to do the load. And when we are
              using shelves it has no effect, since shelves itself is persistent
              object.
    
    keys()  - Return a list of keys in the dictionary.

    has_key() - Check whether a given key is in the dictionary.
    
    Please notice that there is no open() method as in other similar classes.
    Users must provide a file name as well as an operating mode to support
    both persistent and non-persistent (or semi-persistent) operations.
    """
    def __init__(self, filename=None):
        """
        :param store_type: Specify the type of database you want to use
        :type store_type: int
        :param filename: The file name of the database file. If you are using
        memory_dict then this could be given here or in dump(). However if
        you are using shelve or other possible extensions, you must provide
        a file name here in order to establish the connection to the database.
        :type filename: str
        """
        
        # change to hvector
        #self.data_dict = {}
        self.data_dict = mydefaultdict(mydouble)
        
        if not filename == None:
            self.load(filename)
            
        return

    #def get_sub_vector(self, key_list):
        # TODO figure out a more efficient way
    #    sub_vector = mydefaultdict(mydouble)
    #    for k in key_list:
    #        sub_vector[k] = self.data_dict[k]
    #    return sub_vector
        
    def get_vector_score(self, fv):
        score = self.data_dict.evaluate(fv)
        return score

    def load(self,filename):
        """
        Load the dumped memory dictionary Pickle file into memory. Essentially
        you can do this with a shelve object, however it does not have effect,
        since shelve file has been opened once you created the instance.

        Parameter is the same as constructor (__init__).
        """
        logging.debug("Loading Weight Vector from %s " % filename)
        fp = open(filename,"r")
        for line in fp:
            line = line[:-1]
            line = line.split("    ")
            self.data_dict[line[0]] = float(line[1])
        #print self.data_dict
        #self.data_dict = pickle.load(fp)
        fp.close()
        return

    def __getitem__(self,index):
        return self.data_dict[index]

    def __setitem__(self,index,value):
        self.data_dict[index] = value
        return

    def has_key(self,index):
        return self.data_dict.has_key(index)
    
    def pop(self,key):
        self.data_dict.pop(key)
        return
    
    def keys(self):
        """
        Return a list of dictionary keys. This operation is not as expensive
        as the shelve keys() method, so we separate them.
        """
        return self.data_dict.keys()

    def dump(self,filename):
        """
        Called when memory dictionary is used. Dump the content of the dict
        into a disk file using Pickle
        """
        if filename == None:
            print "Skipping dump ..."
            return

        logging.debug("Dumping Weight Vector to %s " % filename)
        logging.debug("Total Feature Num: %d " % len(self.data_dict))
        fp = open(filename,"w")
        for key in self.data_dict.keys():
            fp.write(key + "    " + str(self.data_dict[key]) + "\n")
        #pickle.dump(self.data_dict,fp,-1)
        fp.close()
        return

