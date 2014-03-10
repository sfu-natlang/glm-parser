
import shelve
import pickle

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

    Please notice that there is no open() method as in other similar classes.
    Users must provide a file name as well as an operating mode to support
    both persistent and non-persistent (or semi-persistent) operations.
    """
    def __init__(self,store_type='memory_dict',filename=None):
        if filename == None:
            filename = "default_database.db"
        
        if store_type == 'memory_dict':
            self.data_dict = {}
            self.close = self.dummy
            self.dump = self.dict_dump
            self.load = self.dict_load
        elif store_type == 'shelve_write_through':
            self.data_dict = shelve.open(filename,writeback=False)
            self.close = self.do_close
            self.dump = self.shelve_dump
            self.load = self.dummy
        elif store_type == 'shelve_write_back':
            self.data_dict = shelve.open(filename,writeback=True)
            self.close = self.do_close
            self.dump = self.shelve.dump
            self.load = self.dummy
        else:
            raise ValueError("Unknown store type: %s" % (str(store_type)))
        return

    def dict_load(self,filename):
        """
        Load the dumped memory dictionary Pickle file into memory. Essentially
        you can do this with a shelve object, however it does not have effect,
        since shelve file has been opened once you created the instance.

        Parameter is the same as constructor (__init__).
        """
        fp = open(filename,"r")
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

    def do_close(self):
        self.data_dict.close()
        return
    
    def dummy(self):
        pass
        return

    def dict_dump(self,filename):
        """
        Called when memory dictionary is used. Dump the content of the dict
        into a disk file using Pickle
        """
        fp = open(filename,"w")
        pickle.dump(self.data_dict,fp)
        fp.close()
        return

    def shelve_dump(self,filename):
        """
        Called when persistent daba object is used. This is equivelent of calling
        sync() to the data object
        """
        self.data_dict.sync()
        return
