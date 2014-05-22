import copy
from feature.feature_set import FeatureSet

class DataEntity():
    """
    A data structure that represents the result of a dependency parser.

    Each class instance stores four types of information. These information
    are: node set, POS set, edge set and edge type. Users could construct
    a dependency tree through these information.

    This class also provides interfaces to manipulate the information, including
    retriving nodes, edges, types, modifying nodes, edges, types, and other
    relevant tasks.
    """
    
    def __init__(self, word_list, pos_list, edge_set):
        """
        Initialize a dependency tree. If you provide a sentence then the
        initializer could store it as tree nodes. If no initlization parameter
        is provided then it just construct an empty tree.

        :param word_str: A string of words, or a list of words. No ROOT needed
        :type word_str: str/list(str)
        """
        
        self.set_word_list(word_list)
        self.set_pos_list(pos_list)
        self.set_edge_list(edge_set)
        
        self.update_feature_vector_dict()
        return

    def update_feature_vector_dict(self):
        """
        feature_vector_dict:
            the dictionary of edge to its corresponding feature vector
            i.e.   feature_vector_dict[(0,1)] = FeatureVector()
        """

        f_set = FeatureSet(self)
        self.f_vector_dict = {}
        
        # assume there is no two egde having the same start and end index
        for edge, tag in self.edge_list.iteritems():
            self.f_vector_dict[(edge[0], edge[1], tag)] =\
                f_set.get_local_vector(edge[0], edge[1])
        return
    
    def set_word_list(self,word_list):
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
        return

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

        :return: A list of tuples, the first two elements are head index and
            dependent index, and the last element is edge type
        :rtype: tuple(integer,integer,str)
        """
        return [(i[0],i[1],self.edge_list[i]) for i in self.edge_list.keys()]

