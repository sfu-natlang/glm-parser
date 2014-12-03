import copy,sys
sys.path.append("../")

from feature.feature_generator import FeatureGenerator
from feature.feature_vector import FeatureVector

class Sentence():
    """
    A data structure that represents the result of a dependency parser.

    Each class instance stores four types of information. These information
    are: node set, POS set, edge set and edge type. Users could construct
    a dependency tree through these information.

    This class also provides interfaces to manipulate the information, including
    retriving nodes, edges, types, modifying nodes, edges, types, and other
    relevant tasks.
    """
    
    def __init__(self, word_list, pos_list=None, edge_set=None, spine_list=None):
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
        self.set_spine_list(spine_list);
            
        self.f_gen = FeatureGenerator(self)
        
        self.set_feature_vector_dict()
        self.gold_global_vector = self.get_global_vector(edge_set)
        return

    def get_global_vector(self, edge_set):
        """
        Calculate the global vector with the current weight, the order of the feature
        score is the same order as the feature set

        :param edge_set: the set of edges represented as tuples
        :type: list(tuple(integer, integer))
        
        :return: The global vector of the sentence with the current weight
        :rtype: list
        """
        global_vector = FeatureVector()
        for head_index,dep_index in edge_set:
            local_vector = self.get_local_vector(head_index,dep_index)
            global_vector.aggregate(local_vector)
        return global_vector
        
    def set_feature_vector_dict(self):
        """
        feature_vector_dict:
            the dictionary of edge to its corresponding feature vector
            i.e.   feature_vector_dict[(0,1)] = FeatureVector()
        """
        
        self.f_vector_dict = {}
        
        # assume there is no two egde having the same start and end index
        for edge, tag in self.edge_list.iteritems():
            self.f_vector_dict[(edge[0], edge[1])] =\
                self.f_gen.get_local_vector(edge[0], edge[1])
        return

    def update_feature_vector_dict(self, head_index, dep_index):
        self.f_vector_dict[(head_index, dep_index)] =\
                self.f_gen.get_local_vector(head_index, dep_index)
        
    def get_local_vector(self, head_index, dep_index):
        if not (head_index, dep_index) in self.f_vector_dict:
            lv = self.f_gen.get_local_vector(head_index, dep_index)
            #self.update_feature_vector_dict(head_index, dep_index)
        else:
            lv = self.f_vector_dict[(head_index, dep_index)]

        return lv#self.f_vector_dict[(head_index, dep_index)]
    
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
    
    def set_spine_list(self, spine_list):
        self.spine_list = spine_list

    def get_spine_list(self):
        return self.spine_list
