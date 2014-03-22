
from data_backend import DataBackend

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
        return

    def add_word(self,word):
        """
        Add a word into the dictionary. This will increase the count by 1

        :param word: The word you want to add
        :type word: str
        """
        self.db[word] += 1
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

        for word in db.keys():
            if db[word] > threshold:
                db.pop(word)
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

        for word in db.keys():
            if db[word] <= threshold:
                db.pop(word)
        return

    def dump(self,filename=None,threshold=None,mode=FreqDict.REMOVE_LARGE):
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
        elif mode == FreqDist.RAW:
            pass
        else:
            raise ValueError("Unknown mode: %d" % (mode))
        
        self.db.dump(filename)
