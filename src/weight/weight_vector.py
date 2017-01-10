#
# Global Linear Model Parser
# Simon Fraser University
# NLP Lab
#
# Author: Yulan Huang, Ziqi Wang, Anoop Sarkar, Jetic Gu
# (Please add on your name if you have authored this file)
#

from hvector._mycollections import mydefaultdict
from hvector.mydouble import mydouble
from ast import literal_eval
from data.file_io import fileRead, fileWrite
import logging

logger = logging.getLogger('WEIGHTVECTOR')


class WeightVector(mydefaultdict):
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
    def __init__(self, filename=None, sparkContext=None):
        """
        :param store_type: Specify the type of database you want to use
        :type store_type: int
        :param filename: The file name of the database file. If you are using
        memory_dict then this could be given here or in dump(). However if
        you are using shelve or other possible extensions, you must provide
        a file name here in order to establish the connection to the database.
        :type filename: str
        """
        super(WeightVector, self).__init__(mydouble)

        if filename is not None:
            self.load(filename, sparkContext)

    def get_vector_score(self, fv):
        return self.evaluate(fv)

    def load(self, filename, sparkContext=None):
        """
        Load the dumped memory dictionary Pickle file into memory. Essentially
        you can do this with a shelve object, however it does not have effect,
        since shelve file has been opened once you created the instance.

        Parameter is the same as constructor (__init__).
        """
        logger.info("Loading Weight Vector from %s " % filename)

        f = fileRead(filename, sparkContext)

        for line in f:
            line = line.split("    ")
            # the key is suppose to be of str types
            # do NOT change it
            self[line[0]] = float(line[1])

    def dump(self, filename, sparkContext=None):
        """
        Called when memory dictionary is used. Dump the content of the dict
        into a disk file using Pickle
        """
        if filename is None:
            logger.info("Skipping dump ...")
            return
        f = []
        for k, v in self.iteritems():
            f.append(str(k) + "    " + str(v))

        logger.info("Dumping Weight Vector to %s " % fileWrite(filename, f, sparkContext))
        logger.info("Total Feature Num: %d " % len(self))
