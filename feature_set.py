
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
        """
        Return the current working array index

        :return: working array index
        :rtype: 
        """
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
        """
        Call the __setitem__ method of current working array. This method
        is a shorthand, so it will not help you to automatically create
        empty strings if the index (i.e. position) is out of bound. If
        such feature is desired please call set_pos or other methods instead.
        """
        self.working_array[self.working_array_index][position] = value
        return

    def set_pos_list(self,pos_list):
        """
        Set the POS array in bulk. All data in pos_list will be copied, so
        users do not need to worry about data reference problems.

        :param pos_list: A list that holds POS tags for all words in word_list
        :type pos_list: list(str)
        """
        self.pos_list = copy.copy(pos_list)
        # Do not forget to change this !!!!! Or the reference will remain the
        # old one
        self.working_array[self.POS_ARRAY] = self.pos_list
        return

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

    def get_word_list(self):
        """
        Return the word list. The return value is a new copy so users could
        modify that without worrying about changing the internal data structure

        :return: A list of words
        :rtype: list(str)
        """
        return copy.copy(word_list)

    def get_pos_list(self):
        """
        Return the POS tag list. The return value is a new copy so users could
        modify that without worrying about changing the internal data structure

        :return: A list of POS tags
        :rtype: list(str)
        """
        return copy.copy(pos_list)

    def check_valid(self):
        t = self.is_valid()
        if t[0] == True and t[1] == 0:
            return
        elif t[1] == 1:
            raise ValueError("The length of pos_list and word_list not same")
        elif t[1] == 2:
            raise ValueError("The first word is not __ROOT__")
        elif t[1] == 3:
            raise ValueError("The first POS is not ROOT")
        elif t[1] == 4:
            raise ValueError("There is empty string in pos_list")
        elif t[1] == 5:
            raise ValueError("The edge_list is not a Python dictionary")
        else:
            raise ValueError("Unknown return value. Something went wrong!")
        return
    
    def is_valid(self):
        """
        Detects whether a dependency tree instance is a valid one. We define
        valid as:
            (1) The POS list has the same length as the word list
            (2) The first element of the word list is string "__ROOT__"
            (3) The first element of the POS list is a special tag "ROOT"
            (4) There is no empty string (unintialized) pos in pos_list
            (5) Edge list is a dictionary (no matter empty or not)
            (6) Every node except the ROOT node should have at least
                and at most one head node

        :return: A tuple. The first element is a boolean to indicate whether the
            above criterion has been satisfied. The second element is the number
            of the rule that is not satisfied, or 0 if all are satisfied
        :rtype: tuple(bool,integer)
        """
        if len(self.ord_list) != len(self.pos_list):
            return (False,1)
        if self.word_list[0] != "__ROOT__":
            return (False,2)
        if self.pos_list[0] != "ROOT":
            return (False,3)
        if "" in self.pos_list:
            return (False,4)
        if not isinstance(self.edge_list,dict):
            return (False,5)
        # Iterate through 
        for dep_index in range(1,len(self.word_list)):
            count = 0
            for head_index in range(0,len(self.word_list)):
                if (head_index != dep_index and
                    self.is_edge(head_index,dep_index)):
                    count += 1
            if count != 1:
                return (False,6)

        return (True,0)

    def set_edge(self,head_index,dep_index,dep_type):
        """
        Set the type of a dependency edge. If the edge is not already present
        then this methof implicitly add that edge.

        :param head_index: The index of the heaf node
        :type head_index: integer
        :param dep_index: The index of the dependent node
        :type dep_index: integer
        :param dep_type: The type of dependency
        :type dep_type: str

        :return: True if a new value has been added. False if we are modifying
            existing value
        :rtype: bool
        """
        edge_tuple = (head_index,dep_index)
        if self.edge_list.has_key(edge_tuple):
            # Do not move this before the if stratement!!
            self.edge_list[edge_tuple] = dep_type
            return False
        else:
            self.edge_list[edge_tuple] = dep_type
            return True

    def get_edge(self,head_index,dep_index):
        """
        Return the edge type if edge (head_index,dep_index) exitsis, or None
        if no such edge exist.

        :param head_index: The index of the heaf node
        :type head_index: integer
        :param dep_index: The index of the dependent node
        :type dep_index: integer

        :return: Edge type string if edge exists, None if not.
        :rtype: str/None
        """
        edge_tuple = (head_index,dep_index)
        if self.edge_list.has_key(edge_tuple):
            return self.edge_list[edge_tuple]
        else:
            return None

    def is_edge(self,head_index,dep_index):
        """
        Judge whether there is an edge between two nodes
        """
        edge_tuple = (head_index,dep_index)
        if self.edge_list.has_key(edge_tuple):
            return True
        else:
            return False

    def get_dependent_list(self,head_index):
        """
        Return a list of node index, which are the children node of a head node

        :param head_index: The index of the heaf node
        :type head_index: integer

        :return: A list of integers, which are the indices of the children node
        :rtype: list(integer)
        """
        return [i[1] for i in self.edge_list.keys() if i[0] == head_index]

    def get_head_index(self,dep_index):
        """
        Given a dependent node, return its head_index. If the dependent does not
        have a head node then just return -1 (presumably it is root node,
        however it might be any node that does not have a head node. Users
        should maintain the integrity state)

        :param dep_index: The index of the dependent node
        :type dep_index: integer

        :return: non-negative if head node exists. -1 if not.
        :rtype: integer
        """
        for edge_tuple in self.edge_list.keys():
            if edge_tuple[1] == dep_index:
                return edge_tuple[0]
        return -1

    def get_edge_list(self):
        """
        Return a list of all existing edges

        :return: A list of tuples, the first two elements are head index and
            dependent index, and the last element is edge type
        :rtype: tuple(integer,integer,str)
        """
        return [(i[0],i[1],self.edge_list[i]) for i in self.edge_list.keys()]
    
if __name__ == "__main__":
    dt = DependencyTree("I love computer science")
    dt.set_pos(3,'123')
    dt.set_pos(1,'qwe')
    dt.set_edge(0,2,'type1')
    dt.set_edge(0,3,'type2')
    dt.set_edge(2,4,'type97')
    print dt.get_head_index(4)
    print dt.get_edge_list()
        

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
