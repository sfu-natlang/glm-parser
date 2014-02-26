
import dependency_tree

class FeatureSet():
    """
    Stores and updates weight vector used in dependency parsing according to
    various features
    """
    def __init__(self):
        pass

    def get_unigram_feature_key_list(self,dep_tree):
        """
        Return a list of features keys, which are basuc uni-gram features.
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
            t = (0,word_list[i],pos_list[i],'','')
            if not t in feature_list:
                feature_list.append(t)

            t = (0,word_list[i],'','','')
            if not t in feature_list:
                feature_list.append(t)

            t = (0,'',pos_list[i],'','')
            if not t in feature_list:
                feature_list.append(t)

            t = (0,'','',word_list[i],pos_list[i])
            if not t in feature_list:
                feature_list.append(t)

            t = (0,'','',word_list[i],'')
            if not t in feature_list:
                feature_list.append(t)

            t = (0,'','','',pos_list[i])
            if not t in feature_list:
                feature_list.append(t)
                
        return feature_list

    def get_bigram_feature_key_list(self,dep_tree):
        word_list = dep_tree.get_word_list_ref()
        pos_list = dep_tree.get_pos_list_ref()

        dep_tree.check_valid()
        feature_list = []

        for i in range(0,len(word_list)):
            for j in range(0,len(pos_list)):
                if i == j:
                    continue
                if i != 0:
                    pass
        
    def get_feature_key_list(self,dep_tree):
        pass

    def get_local_scalar(self,dep_tree):
        """
        Return the score of an edge given its edge elements and the context
        """
        pass

    def get_local_vector(self,dep_tree):
        """
        Return the local feature vector of a given edge and the context
        """
        pass

    def update_weight_vector(self,dep_tree):
        """
        Update the weight vector, given a list of deltas that will be added
        up to the current weight vector
        """
        pass

if __name__ == "__main__":
    dt = DependencyTree("I love computer science")
    dt.set_pos(4,'123')
    dt.set_pos(3,'456')
    dt.set_pos(2,'789')
    dt.set_pos(1,'qwe')
    dt.set_edge(0,2,'type1')
    dt.set_edge(0,3,'type2')
    dt.set_edge(2,4,'type97')
    fs = FeatureSet()
    print fs.get_unigram_feature_key_list(dt)
