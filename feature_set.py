
from dependency_tree import *
from data_backend import *


class FeatureSet():
    """
    Stores and updates weight vector used in dependency parsing according to
    various features
    """
    def __init__(self,database_filename,dep_tree):
        self.database_filename = database_filename
        # Open the database file
        # self.db = shelve.open(database_filename,writeback=False)
        self.db = DataBackend("shelve_write_through")
        # Store the feature key vector in the instance
        feature_list = self.get_feature_key_list(dep_tree)
        self.feature_key_list = feature_list[0]
        self.feature_str_list = feature_list[1]
        # Callback functions
        self.satisfaction_func = [self.is_satisfied_unigram,
                                  self.is_satisfied_bigram,
                                   ]
        # Save this for later use
        self.dep_tree = dep_tree
        return

    def add_feature_key(self,feature_list,feature_key):
        """
        Add the feature key into feature list. If a key already exists then
        do nothing and return. This is just a shorthand of
            if not feature_key in feature_list:
                feature_list.append(feature_key)
        :param feature_list: A list that holds the feature keys
        :type feature_list: list
        
        :return: True if there are something added to the list, False if not
        :rtype: bool
        """
        if not feature_key in feature_list:
            feature_list.append(feature_key)
            return True
        else:
            return False

    def get_unigram_feature_key_list(self,dep_tree):
        """
        Return a list of features keys, which are basic uni-gram features.
            xi-word, xi-pos
            xi-word
            xi-pos
            xj-word, xj-pos
            xj-word
            xj-pos
        Basic features are represented using a five-tuple:
            (0,xi-word,xi-pos,xj-word,xj-pos)
            
        The starting 0 is used as a type identifier for basic features
        (including both uni-gram and bi-gram).

        If any entry is not used in the feature tuple it is set to empty string

        :param dep_tree: A DependencyTree instance
        :type dep_tree: DependencyTree
        """
        word_list = dep_tree.get_word_list_ref()
        pos_list = dep_tree.get_pos_list_ref()
        # Check whether the dependency tree satisfies the most fundamental
        # requirements of a dependency tree. Especially we are concerning
        # whether the length of pos_list and word_list are the same
        dep_tree.check_valid()
        
        feature_list = []
        # All possible combinations to the possible tags listed above
        for i in range(len(word_list)):
            self.add_feature_key(feature_list,(0,word_list[i],pos_list[i],
                                               None,None))
            self.add_feature_key(feature_list,(0,word_list[i],None,
                                               None,None))
            self.add_feature_key(feature_list,(0,None,pos_list[i],
                                               None,None))

            self.add_feature_key(feature_list,(0,None,None,
                                               word_list[i],pos_list[i]))
            self.add_feature_key(feature_list,(0,None,None,
                                               word_list[i],None))
            self.add_feature_key(feature_list,(0,None,None,
                                               None,pos_list[i]))

        return feature_list

    def get_bigram_feature_key_list(self,dep_tree):
        """
        Return a list of bi-gram basic features, including
            xi-word, xi-pos, xj-word, xj-pos
            xj-pos, xj-word, xj-pos
            xi-word, xj-word, xj-pos
            xi-word, xi-pos, xj-pos
            xi-word, xi-pos, xj-word
            xi-word, xj-word
            xi-pos, xj-pos
            
        :param dep_tree: A DependencyTree instance
        :type dep_tree: DependencyTree        
        """
        word_list = dep_tree.get_word_list_ref()
        pos_list = dep_tree.get_pos_list_ref()

        dep_tree.check_valid()
        feature_list = []

        # Iterate through the head word i and the dependent word j
        for i in range(0,len(word_list)):
            # j starts at 1 since ROOT node cannot be a dependent node
            for j in range(1,len(pos_list)):
                # Cannot depend on itself
                if i == j:
                    continue
                # Now we assume an edge (i,j). It is guaranteed that all pairs
                # will be enumerated in the nested loop
                self.add_feature_key(feature_list,(1,word_list[i],pos_list[i],
                                                   word_list[j],pos_list[j]))
                self.add_feature_key(feature_list,(1,None,pos_list[i],
                                                   word_list[j],pos_list[j]))
                self.add_feature_key(feature_list,(1,word_list[i],None,
                                                   word_list[j],pos_list[j]))
                self.add_feature_key(feature_list,(1,word_list[i],pos_list[i],
                                                   None,pos_list[j]))
                self.add_feature_key(feature_list,(1,word_list[i],pos_list[i],
                                                   word_list[j],None))
                self.add_feature_key(feature_list,(1,word_list[i],None,
                                                   word_list[j],None))
                self.add_feature_key(feature_list,(1,None,pos_list[i],
                                                   None,pos_list[j]))
        return feature_list

    def get_feature_key_list(self,dep_tree):
        feature_key_list = []
        # We are using unigram and bigram features. This is going to be
        # updated in the future
        feature_key_list += self.get_unigram_feature_key_list(dep_tree)
        feature_key_list += self.get_bigram_feature_key_list(dep_tree)

        # Convert these keys to strings. The database can only use string as
        # the index
        feature_str_list = []
        for i in range(0,len(feature_key_list)):
            feature_str_list.append(str(feature_key_list[i]))
        
        return (feature_key_list,feature_str_list)

    def is_satisfied_unigram(self,feature_key,dep_tree,edge_tuple,check=False):
        """
        Calculate whether an edge satisfies the unigram features
        i.e. feature_key[0] == 0
        """
        if check == True and feature_key[0] != 0:
            raise ValueError("Not a unigram feature: %s" % (str(feature_key)))
        word_list = dep_tree.get_word_list_ref()

        head_word = word_list[edge_tuple[0]]
        if feature_key[1] != None and feature_key[1] != head_word:
            return False
        head_pos = word_list[edge_tuple[0]]
        if feature_key[2] != None and feature_key[2] != head_pos:
            return False
        dep_word = word_list[edge_tuple[1]]
        if feature_key[3] != None and feature_key[3] != dep_word:
            return False
        dep_pos = dep_tree.get_pos_list_ref()[edge_tuple[1]]
        if feature_key[4] != None and feature_key[4] != dep_pos:
            return False
        return True

    def is_satisfied_bigram(self,feature_key,dep_tree,edge_tuple,check=False):
        """
        Calculate whether an edge satisfies the unigram features
        i.e. feature_key[0] == 1
        """
        if check == True and feature_key[0] != 1:
            raise ValueError("Not a bigram feature: %s" % (str(feature_key)))
        # Explicitly set check = False to inhibit type checking
        # Or we will get a ValueError
        ret_val = self.is_satisfied_unigram(feature_key,dep_tree,
                                            edge_tuple,False)
        return ret_val

    def is_satisfied(self,feature_key,dep_tree,edge_tuple):
        """
        Calculate whether an edge satisfies a key feature. There are several
        types of key features, so we need to treat them separately.

        :param feature_key: A feature key in feature_key_list
        :type feature_key: tuple
        :param dep_tree: A DependencyTree instance
        :type dep_tree: DependencyTree
        :param edge_tuple: A pair of integers to indicate an edge
        :type edge_tuple: tuple(integer,integer)

        :return: True if the edge satisfies the feature key. False if not
        :rtype: bool
        """
        # Retrieve the callback
        func_index = feature_key[0]
        # Call the function
        ret_val = self.satisfaction_func[func_index](feature_key,
                                                     dep_tree,edge_tuple)
        return ret_val

    def get_local_scalar(self,dep_tree,edge_tuple):
        """
        Return the score of an edge given its edge elements and the context
        """
        param_list = self.get_local_vector(dep_tree,edge_tuple)
        ret_val = 0
        for i in param_list:
            ret_val += i
        return ret_val

    def get_edge_score(self,edge_tuple):
        """
        Almost identical to get_local_scalar, except that it does not need
        a DependencyTree instance. This is usually used to score an edge
        during parsing, where the overall structure is not known yet, and
        we only have to score edges
        """
        local_vector = self.get_local_vector(self.dep_tree,edge_tuple)
        param_list = self.get_param_list(self.dep_tree,edge_tuple)
        if len(local_vector) != len(param_list):
            raise ValueError("Local vector and parameter list do not accord")
        edge_score = 0
        for i in range(0,len(local_vector)):
            if local_vector[i] == 1:
                edge_score += param_list[i]
        return edge_score

    def get_param_list(self,dep_tree,edge_tuple):
        """
        Return the parameter list of current feature key list
        """
        feature_list_length = len(self.feature_str_list)
        param_list = [0] * feature_list_length
        # Find all parameter, i is a feature key, i[0] is the feature type
        # feature_str_list is the string key for using in the database
        # feature_key_list is the tuple for using by the program code
        for i in range(0,feature_list_length):
            # If the value already in the data base
            if self.db.has_key(self.feature_str_list[i]):
                # Check whether it satisfies the feature key
                if self.is_satisfied(self.feature_key_list[i],
                                     dep_tree,edge_tuple):
                    param_list[i] = self.db[self.feature_str_list[i]]
            else:
                # Create new key-value pair, if it does not exist
                self.db[self.feature_str_list[i]] = 0
                
        return param_list

    def get_local_vector(self,dep_tree,edge_tuple):
        local_vector = []
        for i in range(0,len(self.feature_str_list)):
            if self.is_satisfied(self.feature_key_list[i],dep_tree,edge_tuple):
                local_vector.append(1)
            else:
                local_vector.append(0)
        return local_vector

    def update_weight_vector(self,delta_list):
        """
        Update the weight vector, given a list of deltas that will be added
        up to the current weight vector
        """
        # We do not need to check whether the feature exists or not, since we
        # have initialized the database earlier
        for i in range(0,len(self.feature_key_list)):
            temp = self.db[self.feature_str_list[i]]
            temp += delta_list[i]
            self.db[self.feature_str_list[i]] = temp
        return

    def close(self):
        """
        Routine that must be called before exit
        """
        # Write back all pages into database
        self.db.close()
        return

if __name__ == "__main__":
    dt = DependencyTree("I love computer science")
    dt.set_pos(4,'123')
    dt.set_pos(3,'456')
    dt.set_pos(2,'789')
    dt.set_pos(1,'qwe')
    dt.set_edge(0,2,'type1')
    dt.set_edge(0,3,'type2')
    dt.set_edge(2,4,'type97')
    fs = FeatureSet('test.db',dt)
    fs.update_weight_vector([i % 2 for i in range(0,len(fs.feature_key_list))])
    for i in fs.get_local_vector(dt,(2,4)):
        print i
        pass
    print fs.get_local_scalar(dt,(2,4))
    fs.close()
