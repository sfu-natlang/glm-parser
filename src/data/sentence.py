#
# Global Linear Model Parser
# Simon Fraser University
# NLP Lab
#
# Author: Yulan Huang, Ziqi Wang, Anoop Sarkar
# (Please add on your name if you have authored this file)
#
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
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
    def __init__(self, column_list={}, field_name_list=[], fgen=None):
        """
        Initialize a dependency tree.

        :param column_list: A dict of data columns.
        :type column_list: dict(list)

        :param field_name_list: A list of the data columns
        :type field_name_list: list(str)
        """
        self.column_list = column_list
        self.field_name_list = field_name_list
    
        self.cache_key_func = hash

        # add ROOT to FORM and POSTAG
        edge_list = self.construct_edge_set()
        if "FORM" in self.column_list.keys():
            self.column_list["FORM"] = ["__ROOT__"] + self.column_list["FORM"]
        else:
            sys.exit("'FORM' is needed in Sentence but it's not in config file")

        if "POSTAG" in self.column_list.keys():
            self.column_list["POSTAG"] = ["ROOT"] + self.column_list["POSTAG"]
        else:
            sys.exit("'POSTAG' is needed in Sentence but it's not in config file")

        # This will store the dict, dict.keys() and len(dict.keys())
        # into the instance
        self.set_edge_list(edge_list)

        # Each sentence instance has a exclusive fgen instance
        # we could store some data inside fgen instance, such as cache
        # THIS MUST BE PUT AFTER set_edge_list()
        if fgen is not None:
            self.f_gen = fgen()
            rsc_list = []
            for field_name in self.f_gen.care_list:
                rsc_list.append(self.fetch_column(field_name))

            self.f_gen.init_resources(rsc_list)

            # Pre-compute the set of gold features
            self.gold_global_vector = self.get_global_vector(self.edge_list_index_only)
            # During initialization is has not been known yet. We will fill this later
            # self.current_global_vector = None

            self.set_second_order_cache()
        return

    def construct_edge_set(self):
        """
        Construct the edge set for the given sentence.
        Appends the edge set in self.column_list, appends edge_set column name
        in self.field_name_list, and returns edge_set dict
        """

        if not "HEAD" in self.column_list.keys():
            sys.exit("'HEAD' is needed in Sentence but it's not in config file")
        if not "DEPREL" in self.column_list.keys():
            sys.exit("'DEPREL' is needed in Sentence but it's not in config file")

        self.column_list["edge_set"] = {}

        length = len(self.column_list["HEAD"])
        for i in range(length):
            head = self.column_list["HEAD"][i]
            deprel = self.column_list["DEPREL"][i]
	    if head.isdigit():
                node_key = (int(head), i + 1)
                self.column_list["edge_set"][node_key] = deprel
        return self.column_list["edge_set"]
            
    def return_column_list(self):
        return self.column_list

    def return_field_name_list(self):
        return self.field_name_list

    def fetch_column(self, field_name):
        """
        Return the column given the field name.
        
        :param field_name: Name of the field you want to fetch.
        :type field_name: str
        """

        if field_name in self.column_list.keys():
            return self.column_list[field_name]
        else:
            sys.exit("'" + field_name + "' is needed in Sentence but it's not in config file")

    def set_current_global_vector(self, edge_list):
        """
        This is similar to caching the gold global vector. Current global vector
        is derived from current edge set, which is a result from parser. Since this
        global vector may be used several times, it improves performance to cache
        it inside the instance.

        The cache needs to be refreshed every time a new current edge set is
        available.

        :param edge_list: Return value from parser
        :return: None
        """
        
        #self.current_global_vector = self.convert_list_vector_to_dict(self.get_global_vector(edge_list))
        #~self.cache_feature_for_edge_list(edge_list)

        return self.convert_list_vector_to_dict(self.get_global_vector(edge_list))

    def set_second_order_cache(self):
        self.second_order_cache = {}
        return


    def dump_feature_request(self, suffix):
        """
        See the same function in class FeatureGeneratorBase
        """
        self.f_gen.dump_feature_request(suffix)
        return

    #~def cache_feature_for_edge_list(self, edge_list):
    #~    # Compute cached feature for a given edge list
    #~    self.f_gen.cache_feature_for_edge_list(edge_list)
    #~    return

    def convert_list_vector_to_dict(self, fv):
        ret_fv = FeatureVector()
        for i in fv:
            ret_fv[i] += 1
        return ret_fv


    # Both 1st and 2nd order
    def get_global_vector(self, edge_list):
        """
        Calculate the global vector with the current weight, the order of the feature
        score is the same order as the feature set

        Global vector currently consists of three parts: the first order features,
        second order sibling features, and third order features. We compute them
        separately, although there are options of computing them in single call,
        we choose not to use it regarding code readability.
        
        :return: The global vector of the sentence with the current weight
        :rtype: list
        """
        global_vector = self.f_gen.recover_feature_from_edges(edge_list)

        #return self.convert_list_vector_to_dict(global_vector)
        return global_vector


    def get_local_vector(self, 
                         head_index,
                         dep_index,
                         another_index_list = [],
                         feature_type = 0):
        """
        Return local vector from fgen

        Argument another_index could be either sibling index or
        grand child index. It is implicitly defined by argument
        feature_type. 
        
        The last two arguments will not be used by english_
        1st_fgen

        For possible values of feature_type, please refer to
        FeatureGenerator.get_second_order_local_vector() doc string.

        """


        lv = self.f_gen.get_local_vector(head_index,
                                         dep_index,
                                         another_index_list,
                                         feature_type)

        return lv


    '''
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
        #key = (head_index, dep_index, another_index, feature_type)
        #if key in self.second_order_cache:
        #    return self.second_order_cache[key]

        second_order_fv = self.f_gen.get_local_vector(head_index,
                                                      dep_index,
                                                      [another_index],
                                                      feature_type)

        #self.second_order_cache[key] = second_order_fv

        # Optimization: return a list to compute weight vector
        return second_order_fv
    '''
        
    '''
    def set_word_list(self,word_list):
        """
        :param word_list: A list of words. There is no __ROOT__
        :type word_list: list(str)
        """
        self.word_list = ['__ROOT__'] + word_list
        return
    '''

    '''
    def set_pos_list(self,pos_list):
        """
        Set the POS array in bulk. All data in pos_list will be copied, so
        users do not need to worry about data reference problems.

        :param pos_list: A list that holds POS tags for all words in word_list
        :type pos_list: list(str)
        """
        self.pos_list = ['ROOT'] + pos_list
        return
    '''

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
        return self.fetch_column("FORM")

    def get_pos_list(self):
        """
        Return the POS tag list. The return value is a new copy so users could
        modify that without worrying about changing the internal data structure

        :return: A list of POS tags
        :rtype: list(str)
        """
        return self.fetch_column("POSTAG")

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
    lines = ['Rudolph   NNP 2   NMOD','Agnew    NNP 16  SUB','.  .   16  P', '']
    config_list = ['FORM', 'POSTAG', 'HEAD', 'DEPREL', '2', '3']
    column_list = {}
    for field in config_list:
        if not(field.isdigit()):
            column_list[field] = []
            
    length = len(config_list) - 2

    for line in lines:
        print line
        if line != '':
            entity = line.split()
            for i in range(length):
                if not(config_list[i].isdigit()):
                    column_list[config_list[i]].append(entity[i])
        else:
            if not(config_list[0].isdigit()) and column_list[config_list[0]] != []:
                sent = Sentence(column_list, config_list)
                print sent.column_list['FORM']
            column_list = {}
            for field in config_list:
                if not (field.isdigit()):
                    column_list[field] = []



if __name__ == '__main__':
    test()
