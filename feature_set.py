import shelve
from dependency_tree import *


class FeatureSet():
    """
    Stores and updates weight vector used in dependency parsing according to
    various features
    """
    def __init__(self,database_filename,dep_tree):
        self.database_filename = database_filename
        # Open the database file
        self.db = shelve.open(database_filename,writeback=True)
        # Store the feature key vector in the instance
        self.feature_key_list = self.get_feature_key_list(dep_tree)
        # Callback functions
        self.satisfation_func = [self.is_satisfied_unigram,
                                 self.is_satisfied_bigram,
                                   ]
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
        return feature_key_list

    def is_satisfied_unigram(self,feature_key,dep_tree,edge_tuple):
        """
        Calculate whether an edge satisfies the unigram features
        i.e. feature_key[0] == 0
        """
        if feature_key[0] != 0:
            raise ValueError("Not a unigram feature: %s" % (str(feature_key)))
        head_word = dep_tree.get_word_list_ref()[edge_tuple[0]]
        head_pos = dep_tree.get_pos_list_ref()[edge_tuple[0]]
        dep_word = dep_tree.get_word_list_ref()[edge_tuple[1]]
        dep_pos = dep_tree.get_pos_list_ref()[edge_tuple[1]]
        if feature_key[1] != None and feature_key[1] != head_word:
            return False
        elif feature_key[2] != None and feature_key[2] != head_pos:
            return False
        elif feature_key[3] != None and feature_key[3] != dep_word:
            return False
        elif feature_key[4] != None and feature_key[4] != dep_pos:
            return False
        else:
            return True

    def is_satisfied_bigram(self,feature_key,dep_tree,edge_tuple):
        """
        Calculate whether an edge satisfies the unigram features
        i.e. feature_key[0] == 1
        """
        if feature_key[0] != 1:
            raise ValueError("Not a bigram feature: %s" % (str(feature_key)))
        return self.is_satisfied_unigram(feature_key,dep_tree,edge_tuple)

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
        # Call the function. We need to pass self manually
        return satisfaction_func[func_index](self,feature_key,
                                             dep_tree,edge_tuple)

    def get_local_scalar(self,dep_tree,edge_tuple):
        """
        Return the score of an edge given its edge elements and the context
        """
        param_list = self.get_local_vector(dep_tree,edge_tuple)
        ret_val = 0
        for i in param_list:
            ret_val += i
        return ret_val

    def get_local_vector(self,dep_tree,edge_tuple):
        """
        Return the local feature vector of a given edge and the context
        """
        param_list = []
        # Find all parameter, i is a feature key, i[0] is the feature type
        for i in self.feature_key_list:
            # If the value already in the data base
            if self.db.has_key(i):
                # Check whether it satisfies the feature key
                if self.is_satisfied(i,dep_tree,edge_tuple):
                    param_list.append(self.db[i])
                else:
                    param_list.append(0)
            else:
                param_list.append(0)
                # Create new key-value pair, if it does not exist
                self.db[i] = 0
                
        return param_list

    def update_weight_vector(self,delta_list):
        """
        Update the weight vector, given a list of deltas that will be added
        up to the current weight vector
        """
        # We do not need to check whether the feature exists or not, since we
        # have initialized the database earlier
        for i in self.feature_key_list:
            self.db[i] += delta_list
        return

    def close():
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
    for i in fs.get_unigram_feature_key_list(dt):
        print i
