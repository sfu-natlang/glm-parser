#
# Global Linear Model Parser
# Simon Fraser University
# NLP Lab
#
# Author: Yulan Huang, Ziqi Wang, Anoop Sarkar
# (Please add on your name if you have authored this file)
#

import copy
from feature.feature_vector import FeatureVector

"""
Some basic comcepts are depicted here:

Global vector: A dict-like object that stores mapping like below:
    {
        'feature_string1': 1.0,
        'feature_string2': 1.0,
        'feature_string3': 1.0,
        ...
    }
    It holds all features derived from all edges in a given tree
    structure, therefore, the global vector contains information
    about every edge in the tree.

Local vector: Similar to the global vector, except that it only
stores features derived from a single edge. In order to derive
a global vector from local vectors, we just aggregate them and
take the union of all local features.

Feature caching: Feature is generally computed given three indexes:
the head index, dependency index, and extra index (sibling, grand child,
or None). Computing features for frequently-queried index combinations
are tiresome, and slows down overall performance, therefore, we decide
to cache some frequently used local vector.

argmax *OR* gold edge set ->
edge ->
(h[ead], d[dpendency], o[ther]) ->
local vector -(aggregate)->
global vector

         (h, d, o)
       |----------->|
argmax |            | feature generator
       |<-----------|
          local_fv
           (same)
       |----------->|
       |            | weight vector database
       |<-----------|
        score (float)

(How argmax query features from fgen)
"""

class Sentence():
    """
    A data structure that represents the result of a dependency parser.

    Each class instance stores four types of information. These information
    are: node set, POS set, edge set and edge type. Users could construct
    a dependency tree through these information.

    This class also provides interfaces to manipulate the information, including
    retriving nodes, edges, types, modifying nodes, edges, types, and other
    relevant tasks.

    Data member:

    +=======================================================================+
    | gold_global_vector: A vector that contains all features for all       |
    |                     edges, including first order and second order     |
    | current_global_vector: Similar to gold_global_vector, except that     |
    |                        it is derived from current edge set, rather    |
    |                        than the optimal gold edge set                 |
    |                        Only valid after call to                       |
    |                        set_current_global_vector()                    |
    +=======================================================================+
    """
    
    def __init__(self, word_list, pos_list=None, edge_set=None, fgen=None):
        """
        Initialize a dependency tree. If you provide a sentence then the
        initializer could store it as tree nodes. If no initlization parameter
        is provided then it just construct an empty tree.

        Edge set is a dict object, but it is also pre-computed into a list
        of edges and cached inside the instance. The objective is to avoid
        computing edges each time they are needed. Similarily the total
        number of edges is cached, though it is just a notational convenience

        :param word_list: A list of words. We assume ROOT has been added
        :type word_list: list(str)
        :param pos_list: A list of POS tag. We assume ROOT has been added
        :type pos_list: list(str)
        :param edge_set: A dictionary object, whose keys are all edges
                        (first element being the head and second element being the dep)
                        and values are edge property
        :type edge_set: dict[(int, int)] -> str
        :param fgen: Feature generator class
        :type fgen: Feature Generator class object
        """
        # Used to compute cache key from (h, d, o, type) tuple
        self.cache_key_func = hash
        self.set_word_list(word_list)
        self.set_pos_list(pos_list)
        # This will store the dict, dict.keys() and len(dict.keys())
        # into the instance
        self.set_edge_list(edge_set)
        # Initialize a feature cache with first order features
        # from gold edge set
        self.set_feature_cache()

        # Each sentence instance has a exclusive fgen instance
        # we could store some data inside fgen instance, such as cache
        # THIS MUST BE PUT AFTER set_edge_list()
        self.f_gen = fgen(self)

        # Pre-compute the set of gold features
        self.gold_global_vector = self.get_global_vector(self.edge_list_index_only)
        # During initialization is has not been known yet. We will fill this later
        self.current_global_vector = None
        return

    def set_current_global_vector(self, edge_list):
        """
        This is similar to caching the gold global vector. Current global vector
        is derived from current edge set, which is a result from parser. Since this
        global vector may be used several times, it improves perfprmance to cache
        it inside the instance.

        The cache needs to be refreshed every time a new current edge set is
        available.

        :param edge_list: Return value from parser
        :return: None
        """
        self.current_global_vector = self.get_global_vector(edge_set)
        return


    def dump_feature_request(self, suffix):
        """
        See the same function in class FeatureGeneratorBase
        """
        self.f_gen.dump_feature_request(suffix)
        return


    # Both 1st and 2nd order
    def get_global_vector(self, edge_list):
        """
        Calculate the global vector with the current weight, the order of the feature
        score is the same order as the feature set

        Global vector currently consists of three parts: the first order fatures,
        second order sibling features, and third order features. We compute them
        separately, although there are options of computing them in single call,
        we choose not to use it regarding code redability.
        
        :return: The global vector of the sentence with the current weight
        :rtype: list
        """
        global_vector = self.f_gen.recover_feature_from_edges(edge_list)

        return global_vector


    def get_local_vector(self, head_index, dep_index):
        """
        Return first order local vector, given the head index and dependency index

        Just a wrapper to self.get_second_order_local_vector()
        """

        lv = self.get_second_order_local_vector(head_index, dep_index, 0, 0)

        return lv


    def get_second_order_local_vector(self, head_index, dep_index,
                                      another_index,
                                      feature_type):
        """
        Return second order local vector (and probably with 1st order vector).

        Argument another_index could be either sibling index or
        grand child index. It is implicitly defined by argument
        feature_type.

        For possible values of feature_type, please refer to
        FeatureGenerator.get_second_order_local_vector() doc string.

        """
        second_order_fv = self.f_gen.get_local_vector(head_index,
                                                      dep_index,
                                                      [another_index],
                                                      feature_type)

        return second_order_fv

    
    def set_word_list(self,word_list):
        """
        :param word_list: A list of words. There is no __ROOT__
        :type word_list: list(str)
        """
        self.word_list = ['__ROOT__'] + word_list
        return

    def set_pos_list(self,pos_list):
        """
        Set the POS array in bulk. All data in pos_list will be copied, so
        users do not need to worry about data reference problems.

        :param pos_list: A list that holds POS tags for all words in word_list
        :type pos_list: list(str)
        """
        self.pos_list = ['ROOT'] + pos_list
        return

    def set_edge_list(self,edge_list):
        """
        Initialize the edge_list using a dictionary which contains edges.

        :param edge_list: A dictionary that contains edges in a format like
            tuple(integer,integer):str
        :type edge_list: dict(tuple(integer,integer,str))
        """
        self.edge_list = edge_list
        # Let's do it this way. SHOULD be refeactored later
        self.edge_list_index_only = edge_list.keys()
        self.edge_list_len = len(self.edge_list_index_only)
        return

    def get_edge_list_len(self):
        """
        Return the length of the edge list

        Basically the return value is equivalent to the length
        of self.edge_list.keys(), or, the length of self.edge_list_index_only
        """
        return self.edge_list_len

    def get_word_list(self):
        """
        Return the word list. The return value is a new copy so users could
        modify that without worrying about changing the internal data structure

        :return: A list of words
        :rtype: list(str)
        """
        return self.word_list

    def get_pos_list(self):
        """
        Return the POS tag list. The return value is a new copy so users could
        modify that without worrying about changing the internal data structure

        :return: A list of POS tags
        :rtype: list(str)
        """
        return self.pos_list

    def get_edge_list(self):
        """
        Return a list of all existing edges

        *** OBSOLETE *** Avoid using this method. Unless you really want to
        carry a third (useless) element in return object

        :return: A list of tuples, the first two elements are head index and
            dependent index, and the last element is edge type
        :rtype: tuple(integer,integer,str)
        """
        return [(i[0],i[1],self.edge_list[i]) for i in self.edge_list.keys()]

    def get_edge_list_index_only(self):
        """
        Return a list of tuples, and each tuple represents an edge.

        Since edge information is actually stored in a dictionary object
        with properties attached to that edge, and sometimes we only need
        the two indexes of an edge, this method is implemented as a getter
        to fetch the pre-cached self.edge_list_index_only object

        :return: A list of tuples representing edge sets
        :rtype: list(tuple(int, int))
        """
        return self.edge_list_index_only


# Unit test

def test():
    word_list = ['__ROOT__', 'I', 'am', 'a', 'HAL9000', 'computer', '.']
    pos_list = ['POS-ROOT', 'POS-I', 'POS-am', 'POS-a', 'POS-HAL9000', 'POS-computer',
                'POS-.']
    edge_set = {(0, 2): 'root-to-am', (0, 1): 'artificial-edge',
                (2, 4): 'artificial-edge2',
                (2, 3): 'ae3'}

    s = Sentence(word_list, pos_list, edge_set)
    print(s.grandchild_list)
    print(s.sibling_list)

if __name__ == '__main__':
    test()
