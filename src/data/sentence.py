#
# Global Linear Model Parser
# Simon Fraser University
# NLP Lab
#
# Author: Yulan Huang, Ziqi Wang, Anoop Sarkar
# (Please add on your name if you have authored this file)
#

import copy
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
    
    def __init__(self, word_list, pos_list=None, edge_set=None):
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

        # Set sibling and grandchild relation
        # i.e. self.grandchild_list and self.sibling_list
        self.set_second_order_relation()
        
        self.f_gen = FeatureGenerator(self)

        # Initialize local feature cache to pre-compute all
        # possible features.
        # Set self.f_vector_dict = {(edge0, edge1): FeatureVector()}
        self.set_feature_vector_dict()

        # Precompute the set of features
        self.gold_global_vector = self.get_global_vector(edge_set)
        return

    def find_sibling_relation(self, edge_list):
        """
        Find all sibling relations:
          |------->>>-----|
        head-->sibling   dep *or*
          |-------<<<-----|
        dep   sibling<--head
        (i.e. we always call the node in the middle as "the sibling")

        :param edge_list: The list of edges represented as tuples

        :return: A list of three-tuples: (head, dep, sibling)
        """
        # We could afford this since this method is only called once
        # when sentence is initialized
        # edge_list could be either list or set, which is a design problem
        edge_list = self.get_edge_list_index_only()

        sibling_list = []
        edge_list_len = self.get_edge_list_len()

        for first_edge_index in range(edge_list_len - 1):
            for second_edge_index in range(first_edge_index + 1,
                                           edge_list_len):
                first_edge_tuple = edge_list[first_edge_index]
                second_edge_tuple = edge_list[second_edge_index]
                # If they do not share the same head, continue
                if first_edge_tuple[0] != second_edge_tuple[0]:
                    continue
                head_index = first_edge_tuple[0]
                dep_index = first_edge_tuple[1]
                sib_index = second_edge_tuple[1]

                # May erase this later!
                assert dep_index != sib_index

                if dep_index > head_index and sib_index > head_index:
                    # We always call the node
                    if dep_index > sib_index:
                        sibling_list.append((head_index, # Head
                                             dep_index,  # Dep
                                             sib_index)) # Sibling
                    else:
                        sibling_list.append((head_index, # Head
                                             sib_index,  # Dep (although the var
                                                         # name is sib_index)
                                             dep_index)) # Sibling
                elif dep_index < head_index and sib_index < head_index:
                    if dep_index > sib_index:
                        sibling_list.append((head_index, # Head
                                             sib_index,  # Dep
                                             dep_index)) # Sibling
                    else:
                        sibling_list.append((head_index, # Head
                                             dep_index,  # Dep
                                             sib_index)) # Sibling

        return sibling_list


    def find_grandchild_relation(self):
        """
        Find all grandchild relation:

        head-->dep-->grandchild *or*
        grandchild<--dep<--head *or*
             |------<<<-----|
        grandchild  head-->dep  *or*
         |------>>>------|
        dep<--head  grandchild

        i.e. There is no order constraint, as long as
        the head, dep and grandchild node could be chained
        using two edges. (In contrast, in sibling relation
        this is not true. Sibling relation requires dep
         and sibling node on the same side of the head. But
         again direction is not a constraint in either cases)
        """
        edge_list = self.get_edge_list_index_only()

        grandchild_list = []
        edge_list_len = self.get_edge_list_len()

        for first_edge_index in range(edge_list_len - 1):
            for second_edge_index in range(first_edge_index + 1,
                                           edge_list_len):
                first_edge_tuple = edge_list[first_edge_index]
                second_edge_tuple = edge_list[second_edge_index]

                if first_edge_tuple[1] == second_edge_tuple[0]:
                    grandchild_list.append((first_edge_tuple[0],   # Head
                                            first_edge_tuple[1],   # dep
                                            second_edge_tuple[1])) # grand child
                elif first_edge_tuple[0] == second_edge_tuple[1]:
                    grandchild_list.append((second_edge_tuple[0],
                                            second_edge_tuple[1],
                                            first_edge_tuple[1]))
        return grandchild_list

    def set_second_order_relation(self):
        """
        Store second order relation into class instance
            * Sibling relation
            * Grand child relation
        """
        # TODO: Clarify the type of edge_list, and constrain the
        # usage of edge_list to only through a method call
        # instead of fetch them directly from the instance
        self.grandchild_list = self.find_grandchild_relation(self.edge_list)
        self.sibling_list = self.find_sibling_relation(self.edge_list)

        return


    # Both 1st and 2nd order
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

        # 1st order
        for head_index, dep_index in self.get_edge_set_index_only():
            local_vector = self.get_local_vector(head_index,dep_index)
            global_vector.aggregate(local_vector)

        # 2nd order sibling
        for head_index, dep_index, sib_index in self.sibling_list:
            local_vector = \
                self.get_second_order_local_vector(head_index,
                                                   dep_index,
                                                   sib_index,
                                                   FeatureGenerator.SECOND_ORDER_SIBLING_ONLY)
            global_vector.aggregate(local_vector)

        # 2nd order grand child
        for head_index, dep_index, grand_index in self.grandchild_list:
            local_vector = \
                self.get_second_order_local_vector(head_index,
                                                   dep_index,
                                                   grand_index,
                                                   FeatureGenerator.SECOND_ORDER_GRANDCHILD_ONLY)
            global_vector.aggregate(local_vector)

        return global_vector
        
    def set_feature_vector_dict(self):
        """
        feature_vector_dict:
            the dictionary of edge to its corresponding feature vector
            i.e.   feature_vector_dict[(0,1)] = FeatureVector()
        """

        # Act as a cache for local vectors, in which some of them
        # might be evaluated for several times, and we want
        # to save computation for the same feature
        self.f_vector_dict = {}
        
        # assume there is no two egde having the same start and end index
        for edge0, edge1 in self.get_edge_list_index_only():
            self.f_vector_dict[(edge0, edge1)] = \
                self.f_gen.get_local_vector(edge0, edge1)
        return


    # def update_feature_vector_dict(self, head_index, dep_index):
    #    self.f_vector_dict[(head_index, dep_index)] = \
    #            self.f_gen.get_local_vector(head_index, dep_index)

    def get_local_vector(self, head_index, dep_index):
        if not (head_index, dep_index) in self.f_vector_dict:
            lv = self.f_gen.get_local_vector(head_index, dep_index)
            #self.update_feature_vector_dict(head_index, dep_index)
        else:
            lv = self.f_vector_dict[(head_index, dep_index)]

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
        #if (feature_type != FeatureGenerator.SECOND_ORDER_SIBLING_ONLY and
        #    feature_type != FeatureGenerator.SECOND_ORDER_GRANDCHILD_ONLY):
        #    raise TypeError("Unknown 2nd order feature type")

        second_order_fv = self.f_gen.get_second_order_local_vector(head_index,
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

