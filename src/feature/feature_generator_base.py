
#
# Global Linear Model Parser
# Simon Fraser University
# NLP Lab
#
# Author: Yulan Huang, Ziqi Wang, Anoop Sarkar
# (Please add on your name if you have authored this file)
#

import debug.debug

#################################################################################################
# Notes on writing modularized feature generator:
#
# 1. The base class defined in this file specifies a common interface, which should be followed
#    by your customized fgen. But whether to inherit from this class is of your choice, and it
#    is not enforced, since in some cases we know inheritance will not improve readability of
#    code, and will degrade performance
# 2. Each fgen class should be stored in a separate file, and each file should only have one
#    class having the "get_local_vector()" interface (i.e. there must be only one class who has
#    a method called get_local_vector). If multiple choice is possible then the behavior is undefined
# 3. Please make sure there is no direct "from ... import ..." statement, unless you are confirmed
#    such statements will not introduce any class with a get_local_vector() interface
#################################################################################################


class FeatureGeneratorBase:
    """
    Base class for all feature generators. All feature generator must inherit from this class,
    and should implement all interfaces defined below

    Exposed data member and methods

    +===========================================================================================+
    | self.key_gen_func : Key generation callback (default str)                                 |
    | self.word_list : Word list                                                                |
    | self.pos_list : POS list                                                                  |
    | self.compute_five_gram()                                                                  |
    | self.add_dir_and_dist() : Add direction and distance                                      |
    +===========================================================================================+
    """

    # See __init__ below
    key_gen_func = str

    def __init__(self, sent):
        """
        Initialize the feature generator with a sentence object. Also pre-compute and
        cache some desired data (e.g. five-gram)

        This method stores word_list and pos_list inside the instance. Do NOT re-implement
        this in children classes.

        If children classes must include more functionality in the initializer, please define
        their own in respective children classes, and call super class __init__

        Feature vector are represented as key-weight (fixed to 1 for later use) pairs. The key
        value is derived from feature objects, which are tuples with strings and integers being
        their elements. Therefore, we need to specify a key generating function to derive
        the key value from tuples.

        :param sent: Sentence instance
        :type sent: class Sentence instance
        """
        self.word_list = sent.get_word_list()
        self.pos_list = sent.get_pos_list()
        # Pre-compute and cache five-gram for this sentence
        self.compute_five_gram()

        # Feature request log is kept under class, not instance, because instance
        # do not share data
        if debug.debug.log_feature_request_flag is True:
            self.feature_request_log = {}

        return

    def log_feature_request(self, h, d, o, t):
        """
        Log every feature inside fv into feature request log

        Please make sure fv does not include any decorated features (with
        dir and dist)
        """
        key = str((h, d, o, t))

        if key in self.feature_request_log:
            self.feature_request_log[key] += 1
        else:
            self.feature_request_log[key] = 1

        return

    def dump_feature_request(self, suffix):
        """
        Dump feature request for this instance of fgen into a file named
            "feature_request_[suffix].log"
        """
        if debug.debug.log_feature_request_flag is True:
            filename = "feature_request_%s.log" % (suffix, )
            fp = open(filename, 'w')
            for i in self.feature_request_log:
                fp.write("'%s' %s\n" % (str(i),
                                      self.feature_request_log[i]))
            fp.close()

        return

    def compute_five_gram(self):
        """
        Computes a five gram feature based on the current word_list. The five
        gram is a list having the same length as the word_list, and it will be
        used to construct five gram features.

        Each list entry at position i correponds to the word at the same position
        in word_list, or None if the length of that word is already less than 5.
        This makes it easier to judge whether the length of a word is more than
        five, making it unnecessary to compute the length each time.
        """
        # Flush the old one
        self.five_gram_word_list = []
        # Compute a five_gram for all words. Pleace notice that for
        # those words less than 5 characters, we just push a None into
        # the list, therefore we could judge the length of the word against
        # 5 by reading the corresponding position in five_gram_word_list
        # instead of calculating it each time.
        for word in self.word_list:
            if len(word) > 5:
                self.five_gram_word_list.append(word[0:5])
            else:
                self.five_gram_word_list.append(None)
        return

    def get_local_vector(self, head_index, dep_index, other_index_list=None,
                         feature_type=None):
        """
        This defines a template for common interface: All functionality of its children
        classes is exposed by this method.

        The most simple case is 1st-order feature, where a head index and dependency index
        suffices. However, for more complicated cases, such as second order dependency, there
        is one more node (sibling or grandchild), and therefore other_index_list provides extra
        information for higher order features.

        For even higher (>2) order features, other_index_list serves as a list of extra nodes,
        and no additional argument is needed. The semantics of other_index_list is determined
        by children classes, and is not specified here. As long as class author and caller adhere
        to the same convention, no constraint is enforced (but the explanation above is recommended)

        Argument feature_type holds any other information for feature generation. For first order
        features this argument is not used. For second order features, this argument serves as
        an indicator of whether to generate sibling or grandchild feature. For even higher order
        features, this argument could contain more than one piece of information, the structure
        of which is left to sub-class author.
        """
        # It's pure virtual function
        raise NotImplementedError

    def add_dir_and_dist(self, fv, head_index, dep_index):
        """
        Add additional distance and direction information in a given feature
        vector. All existing features will be iterated through, and new
        features will be constructed based on these existing features as well
        as the edge information. All distance are calculated into the bucket
        of 1 2 3 4 5 and 10, i.e. if some dist is more than 5 but less than 10
        then it will be counted as 5. If some dist is more than 10 then it is
        counted as 10.

        The decorated features are also tuples, the first element being the
        original tuple, the second and the third being the dir and dist:

            ([original_feature],dir,dist)

        :param head_index: The index of the head node
        :type head_index: integer
        :param dep_index: The index of the dependency node
        :type dep_node: integer
        """
        if head_index < dep_index:
            dist = dep_index - head_index + 1
            direction = 0 #'R'
        else:
            dist = head_index - dep_index + 1
            direction = 1 #'L'

        if dist > 5:
            if dist < 10:
                dist = 5
            else:
                dist = 10

        key_gen_func = self.key_gen_func
        # This is dangerous: we are modifying the dict while adding content
        for feature in fv.keys():
            new_feature_str = key_gen_func((feature,direction,dist))
            fv[new_feature_str] = 1

        return

    def recover_feature_from_edges(self, edge_list):
        """
        This is a optional interface for any usable feature generator. This method
        extracts every possible relation from a list of edges (trivial for 1st order
        features, but non-trivial for high orders), and apply them to feature generator.

        Return feature vector object as get_local_vector()
        """
        raise NotImplemented
