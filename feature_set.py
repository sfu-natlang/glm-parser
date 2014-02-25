
import copy

class DependencyTree():
    """
    A data structure that represents the result of a dependency parser.

    Each class instance stores four types of information. These information
    are: node set, POS set, edge set and edge type. Users could construct
    a dependency tree through these information.

    This class also provides interfaces to manipulate the information, including
    retriving nodes, edges, types, modifying nodes, edges, types, and other
    relevant tasks.
    """

    WORD_ARRAY = 0
    POS_ARRAY = 1
    EDGE_ARRAY = 2
    
    def __init__(self,word_str=None):
        """
        Initialize a dependency tree. If you provide a sentence then the
        initializer could store it as tree nodes. If no initlization parameter
        is provided then it just construct an empty tree.

        :param word_str: A string of words, or a list of words. No ROOT needed
        :type word_str: str/list(str)
        """
        self.pos_list = ['ROOT']
        self.edge_list = {}
        # An empty tree must have at lease one node, the ROOT node
        self.word_list = ['__ROOT__']

        self.working_array_index = 0
        self.working_array = [self.word_list,self.pos_list,self.edge_list]
        
        if isinstance(word_str,list):
            # Do not use the original word list.
            self.word_list += copy.copy(word_str)
        elif isinstance(word_str,str):
            self.word_list += word_str.split()
        elif word_str == None:
            pass
        else:
            raise TypeError("""Cannot process unknown type as
                            initializer: %s""" % (str(type(word_str))))
        return

    def set_working_array(self,array_index):
        """
        Set the current working array, to facilitate __getitem__ method

        :param array_index: Enumeratatable constant
            WORD_ARRAY: Set working array to word array
            POS_ARRAY: ...                   pos array
            EDGE_ARRAY: ...                  edge array
        :type array_index: integer
        """
        if array_index <0 or array_index >= len(self.working_array):
            raise ValueError("Invalid index into working array: %d" %
                             (array_index))
        else:
            self.working_array_index = array_index
        return

    def get_working_array_index(self):
        return self.working_array

    def __getitem__(self,position):
        """
        Return an item in the current working array. This could be used to
        access word_list, pos_list or edge_list

        :param position: Any valid index suitable to current working array
        :type position: Varies according to current working array
        """
        return self.working_array[self.working_array_index][position]

    def __setitem__(self,position,value):
        pass

    def set_pos(self,position,pos_str):
        """
        Set the POS tag of a word of index position. position could by any
        valid word index, however if position is greater than the length of
        word_list - 1 a ValueError will be raised.

        We guarantee that the pos_list could be updated in a non-uniform way
        i.e. users can first initialize the third pos, then the second, then
        the fifth, and so on. They do not need to follow a strict order.
        However, if you jump over some uninitialized pos tags, they will be
        implicitly initialized to empty string, which is not valid.

        :param position: The index where the pos is set
        :type position: integer
        :param pos_str: The POS tag in string
        :type pos_str: str

        :return: True if position is in the range of initialized pos tag, False
        if not
        :rtype: bool
        """
        if position >= len(self.word_list) or position <= 0:
            raise ValueError("Invalid position: %d" % (position))
        
        if position >= len(self.pos_list):
            self.pos_list += ([''] * (position - len(self.pos_list)))
            self.pos_list.append(pos_str)
            return False
        else:
            self.pos_list[position] = pos_str
            return True
    
    def is_valid(self):
        """
        Detects whether a dependency tree instance is a valid one. We define
        valid as:
            (1) The POS list has the same length as the word list
            (2) The first element of the word list is string "__ROOT__"
            (3) The first element of the POS list is a special tag "ROOT"
            (4) There is no empty string (unintialized) pos in pos_list
            (5) Edge list is a list (no matter empty or not)

        :return: True if the criterion above is satisfied. False if not
        :rtype: bool
        """
        if len(self.ord_list) != len(self.pos_list):
            return False
        if self.word_list[0] != "__ROOT__":
            return False
        if self.pos_list[0] != "ROOT":
            return False
        if "" in self.pos_list:
            return False
        if not isinstance(self.edge_list,dict):
            return False

        return True

if __name__ == "__main__":
    dt = DependencyTree("I love computer science")
    dt.set_pos(3,'123')
    dt.set_pos(1,'qwe')
    print dt[3]
    print dt.word_list
    print dt.pos_list
        

class FeatureSet():
    """
    Stores and updates weight vector used in dependency parsing according to
    various features
    """
    def __init__(self):
        pass

    def get_local_scalar(edge_tuple,word_list):
        """
        Return the score of an edge given its edge elements and the context
        """
        pass

    def get_local_vector(edge_tuple,word_list):
        """
        Return the local feature vector of a given edge and the context
        """
        pass

    def update_weight_vector(delta_list):
        """
        Update the weight vector, given a list of deltas that will be added
        up to the current weight vector
        """
        pass
