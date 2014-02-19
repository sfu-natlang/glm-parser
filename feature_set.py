

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
