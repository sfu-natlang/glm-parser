
class EisnerLearner():
    """
    A class that implements the learning alrogithm of dependency graphs.
    """
    def __init__(self,feature_scorer_list):
        # A list of functions that computes the feature vector
        self.feature_scorer_list = feature_scorer_list
        # Initially all parameters are set to 0. The number of parameters is
        # equal to the number of scoring functions
        self.param_vector = [0 for i in range(0,len(feature_scorer_list))]
        # Cache this number to save computation
        self.param_count = len(self.param_vector)
        return

    def adjust_param_vector(self,new_pv):
        

    def local_feature_vector(self,edge_tuple,word_list):
        # A local feature could be derived
        # using the current edge (parent_index,child_index,edge_type) and the
        # word list that provides the context information.
        """
        Computes the local feature vector

        :param edge_tuple: Current edge that is being evaluated
        :type edge_tuple: tuple(integer,integer,str)
        :param word_list: A list of words serving as the context
        :type word_list: list(tuple(str,str))

        :return: A feature vector, each element being the binary score
        :rtype: list(bool/integer) --> Logically it is bool, however ingeter is
        more convenient
        """
        feature_vector = []
        for func in self.feature_scorer_list:
            feature_vector.append(func(edge_tuple,word_list))
        return feature_vector

    def global_feature_vector(self,graph):
        # Iterate through the edge list and accumulate all local vectors
        """
        Computes global feature vector using local features

        :param graph: A tuple containing the words and edges
        :type graph: tuple(list,list)

        :return: A global feature vector
        :rtype: list(integer)
        """
        # Explicitly extract them
        word_list = graph[0]
        edge_list = graph[1]
        
        global_vector = [0 for i in range(0,len(self.param_count))]
        for edge in edge_list:
            local_vector = self.local_feature_vector(edge,word_list)
            # Accumulate
            for i in range(0,self.param_count):
                global_vector[i] += local_vector[i]
        return global_feature_vector

    def weighted_feature_vector(self,global_vector):
        # Iterate through the global vector list and the parameter list
        # ** CAUTION ** you need to compute global vector by yourself, because
        # the global vector might be used in other places, so it is better
        # to explicitly pass it as an argumment instead of wrapping it in
        """
        Computes the weighted feature vector of a dependency graph

        :param global_vector: The global vector
        :type edge_list: list(integer)

        :return: A weighted feature vector
        :rtype: list(integer)
        """
        global_vector = self.global_feature_vector(edge_list,word_list)
        weighted_vector = []
        for i in range(0,param_count):
            weighted_vector.append(float(global_vector[i]) * self.param_list[i])
        return weighted_vector
        
    def parse_file_string(s):
        """
        Parses the string read from the training file.

        :param s: String read from treebank
        :type s: str

        :return: A list of words and a list of edges, i.e. G = (V,E)
        :rtype: tuple(list,list), the first is the word list and the second is
        the edge list
        """
        # Each line represents one word and its relations
        line_list = s.splitlines()
        # list(tuple(word,POS)). ROOT is not shown on the file, however it
        # occupies the first position (index = 0)
        word_list = [('ROOT','ROOT')]
        # list(tuple(parene_node_index,child_node_index,edge_type))
        edge_list = []
        curret_index = 1
        for line in line_list:
            # A list of 4 elements
            # WORD      POS     PARENT INDEX    EDGE TYPE
            line_tuple = line.split()
            word_list.append((line_tuple[0],line_tuple[1]))
            edge_list.append((line_tuple[2],current_index,line_tuple[3]))
            
            # Do not forget this!!!!!!!!!!!!!!!!!!!!!!
            current_index += 1
        return (word_list,edge_list)


