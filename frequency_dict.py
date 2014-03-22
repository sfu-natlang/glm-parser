
from data_backend import DataBackend
import copy
import sys

class FreqDict():

    REMOVE_SMALL = 0
    REMOVE_LARGE = 1
    RAW = 2
    
    """
    A frequency dictionary for training GLM parser. This could be
    treated as an optimization for the standard process of training. The
    goal is to cut off those words whose frequency is less than a given
    threshold, to make it faster to train the parser.
    """
    def __init__(self,threshold=None,filename=None):
        """
        Initialize an instance of FreqDict. The threshold is given as a
        paremeter. Any word with a frequency smaller than this value will
        be cut off.

        :param threshold: The smallest freqency for a word that will not be
        cut off. If this is None then you need to provide an extra parameter
        when dumping the dict onto disk
        :type threshold: int
        :param filename: The file name you want to dump. If this is not provided
        here then you need to give the parameter to the dump procedure.
        :type filename: str
        """
        # Save the value for later use
        self.threshold = threshold
        # Create a new dict for storing words (we use DataBackend)
        self.db = DataBackend('memory_dict',filename)
        # What filter() will return if a word has small frequency
        self.default_return = None
        # When created the instance is raw dict
        self.db['__USE__'] = 'dict_raw'
        # Bind the method
        self.bind_method()
        return

    def register_default_return(self,default):
        """
        Set a default return value is a word is filtered out, i.e. the word
        is not in the dict or list when calling filter()
        """
        self.default_return = default
        return

    def add_word(self,word):
        """
        Add a word into the dictionary. This will increase the count by 1

        :param word: The word you want to add
        :type word: str
        """
        if self.db.has_key(word):
            self.db[word] += 1
        else:
            self.db[word] = 1
        return

    def add_tree(self,dep_tree):
        """
        Add all words from a tree into the dictionary. This will be done by
        calling add_word

        :param dep_tree: A dependency tree instance
        :type dep_tree: DependencyTree
        """
        for word in dep_tree.word_list:
            self.add_word(word)
        return

    def remove_large_freq(self,threshold=None):
        """
        Remove all words whose frequency is larger than the threshold given.
        The threshold in the parameter is optional. If it is not None then
        it will override the one given in __init__, or we will use the value
        given in __init__. If both are None, an error will be raised.

        :param threshold: The threshold used to cut off words
        :type threshold: int
        """
        # Override self.threshold
        if threshold == None:
            threshold = self.threshold
        # raise exception if both are None
        if threshold == None:
            raise ValueError("Must provide a threshold value")

        for word in self.db.keys():
            if self.db[word] > threshold:
                self.db.pop(word)
                
        # We are eliminating those too large, so this is a dict_small
        self.db['__USE__'] = 'dict_small'

        return

    def remove_small_freq(self,threshold=None):
        """
        Similar to remove_large_freq, except that it removes those whose
        frequency is too small. This is not recommended for using, and is not
        the default mode to cut off words. Only use this is you are sure there
        will be unseen words during the training.
        """
        if threshold == None:
            threshold = self.threshold
        if threshold == None:
            raise ValueError("Must provide a threshold value")

        for word in self.db.keys():
            if self.db[word] <= threshold:
                self.db.pop(word)

        self.db['__USE__'] = 'dict_large'
        return

    def filter(self,word):
        """
        This is only a stub, and will be replaced by other call backs.

        In general, this function returns the word if its frequency is large
        and return a default return if the frequency is small
        """
        raise TypeError("You have not bound the proper method yet")
        return

    def filter_dict_large(self,word):
        if self.db.has_key(word):
            return word
        else:
            return self.default_return

    def filter_dict_small(self,word):
        if self.db.has_key(word):
            return self.default_return
        else:
            return word

    def filter_dict_raw(self,word):
        sys.stderr.write("WARNING: Raw type used for filter()\n")
        return word
        
    def bind_method(self):
        """
        Bind the correct functions to the method name.
        """
        use = self.db['__USE__']
        if use == 'dict_small':
            self.filter = self.filter_dict_small
        elif use == 'dict_large':
            self.filter = self.filter_dict_large
        elif use == 'dict_raw':
            self.filter = self.filter_dict_raw
        else:
            raise TypeError("Unknown type when binding: %s" % (use))
        return

    def load(self,filename=None):
        """
        Load a dumped file from the disk. It will construct a new dictionary in
        the memory. If you would like to remove the frequency and only keeps
        the words, please use convert()
        """
        if filename == None:
            filename = self.filename
        if filename == None:
            raise ValueError("You must provide a file name")
        
        self.db.load(filename)
        # Bind correct method according to the type we have just loaded
        # i.e. self.db['__USE__']
        self.bind_method()
        
        return

    def dump(self,filename=None,threshold=None,mode=REMOVE_LARGE):
        """
        Dump the freq dict into the disk

        :param filename: An optional file name. If this is provided then it will
        override the one given in __init__()
        :type filename: str
        :param threshold: An optional threshold for removing words. If this is
        provided then it will override the one given in __init__()
        :type threshold: int
        :param mode: Controls whether to remove the larger frequency words
        (mode = 0) or smaller frequency words (mode = 1) or no remove (mode = 2)
        :type mode: int
        """
        if filename == None:
            filename = self.filename
        if filename == None:
            raise ValueError("You must provide a file name")

        if mode == FreqDict.REMOVE_LARGE:
            self.remove_large_freq(threshold)
        elif mode == FreqDict.REMOVE_SMALL:
            self.remove_small_freq(threshold)
        elif mode == FreqDict.RAW:
            pass
        else:
            raise ValueError("Unknown mode: %d" % (mode))
        
        self.db.dump(filename)

    def __getitem__(self,word):
        """
        Operator overloading for adding a word. Please notice that this is
        __getitem__, and will change the frequency of the word. Logically
        speaking this is not a good design, however I did this because it
        looks more concise.
        """
        self.add_word(word)
        return

if __name__ == "__main__":
    fd = FreqDict()
    fd['wzq'];fd['wzq'];fd['wzq'];fd['wzq'];fd['wzq'];fd['wzq']
    fd['www'];fd['www'];fd['www'];fd['www']
    fd['123'];fd['123'];fd['123'];fd['123'];fd['123']
    fd['456'];
    fd.dump(filename="freqdict_test.db",threshold=5,mode=FreqDict.REMOVE_SMALL)
    fd.load(filename="freqdict_test.db")
    for i in fd.db.keys():
        print i,fd.db[i]
