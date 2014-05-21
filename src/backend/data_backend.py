
import shelve
import cPickle as pickle
import sys

from hvector._mycollections import mydefaultdict
from hvector.mydouble import mydouble

class DataBackend():
    """
    A dictitionary-like object. Used to facilitate class FeatureSet to
    store the features.

    Callables inside the class:

    close() - Close the dictionary file. It has not effect when we are using
              memory dict. However when using other persistent objects remember
              to close it before quitting
              
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
    def __init__(self,store_type='memory_dict',filename=None):
        """
        :param store_type: Specify the type of database you want to use
        :type store_type: int
        :param filename: The file name of the database file. If you are using
        memory_dict then this could be given here or in dump(). However if
        you are using shelve or other possible extensions, you must provide
        a file name here in order to establish the connection to the database.
        :type filename: str
        """
        if filename == None:
            filename = "default_database.db"
            
        self.store_type = store_type
        
        if store_type == 'memory_dict':
            # change to hvector
            #self.data_dict = {}
            self.data_dict = mydefaultdict(mydouble)
            self.close = self.dummy
            self.dump = self.dict_dump
            self.load = self.dict_load
            self.keys = self.dict_keys
        elif store_type == 'shelve_write_through':
            self.data_dict = shelve.open(filename,writeback=False)
            self.close = self.do_close
            self.dump = self.shelve_dump
            self.load = self.dummy2
            self.keys = self.shelve_keys
        elif store_type == 'shelve_write_back':
            self.data_dict = shelve.open(filename,writeback=True)
            self.close = self.do_close
            self.dump = self.shelve_dump
            self.load = self.dummy2
            self.keys = self.shelve_keys
        else:
            raise ValueError("Unknown store type: %s" % (str(store_type)))
        return

    
    def get_vector_score(self, fv):
        if self.store_type == 'memory_dict':
            score = self.data_dict.evaluate(fv.keys())
        else:
            score = 0
            # Iterate through each feature that appears with the edge
            for i in fv.keys():
                # If there is a parameter record (i.e. not 0) we just use that
                if self.data_dict.has_key(i):
                    score += self.data_dict[i]
                else:
                    pass
                    # If not then we do not add (since it is 0)
                    # But we will add the entry into the database
                    #self.db[i] = 0
                    #####################
                    # This will cause us lots of trouble, including making
                    # the size of the database bloat to an unacceptable size
                    # and introducing a large error in the estimation of the
                    # feature number.
        return score
    
    def dict_load(self,filename):
        """
        Load the dumped memory dictionary Pickle file into memory. Essentially
        you can do this with a shelve object, however it does not have effect,
        since shelve file has been opened once you created the instance.

        Parameter is the same as constructor (__init__).
        """
        fp = open(filename,"rb")
        self.data_dict = pickle.load(fp)
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

    def shelve_keys(self):
        """
        This operation is very slow because the database must lookup the disk
        file and extract all keys from the file. So we print a warning message
        to inform the user.
        """
        sys.stderr.write("""Warning: Calling keys() mehtod on a shelve object
                            may cause severe performance degrade.\n""")
        return self.data_dict.keys()
    
    def dict_keys(self):
        """
        Return a list of dictionary keys. This operation is not as expensive
        as the shelve keys() method, so we separate them.
        """
        return self.data_dict.keys()

    def do_close(self):
        self.data_dict.close()
        return
    
    def dummy(self):
        pass
        return

    def dummy2(self,empty):
        pass
        return

    def dict_dump(self,filename=None):
        """
        Called when memory dictionary is used. Dump the content of the dict
        into a disk file using Pickle
        """
        if filename == None:
            filename = self.filename
        if filename == None:
            raise ValueError("You must provide a file name")
        fp = open(filename,"wb")
        pickle.dump(self.data_dict,fp,-1)
        fp.close()
        return

    def shelve_dump(self,filename=None):
        """
        Called when persistent daba object is used. This is equivelent of calling
        sync() to the data object

        :param filename: Not used. This is already given in __init__()
        :type filename: None
        """
        self.data_dict.sync()
        return
