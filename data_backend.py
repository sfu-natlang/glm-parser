from shelve import *

class DataBackend():
    """
    A dictitionary-like object. Used to facilitate class FeatureSet to
    store the features.
    """
    def __init__(self,store_type='memory_dict',filename=None):
        if filename == None:
            filename = "default_database.db"
        
        if store_type == 'memory_dict':
            self.data_dict = {}
            self.close = self.dummy
        elif store_type == 'shelve_write_through':
            self.data_dict = shelve.open(filename,writeback=False)
            self.close = self.do_close
        elif store_type == 'shelve_write_back':
            self.data_dict = shelve.open(filename,writeback=True)
            self.close = self.do_close
        else:
            raise ValueError("Unknown store type: %s" % (str(store_type)))
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
