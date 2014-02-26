# -*- coding: utf-8 -*-
import feature_set
import eisner

class WeightLearner():
    """
    Learns the weight of the features using maximum perceptron algorithm
    """
    def __init__(self):
        self.feature_set = feature_set.FeatureSet()
        return
    
    def learn_weight(training_data_tuple):
        """
        Given the list of the training data, the function learns the weight 
        for each feature in the feature set
        
        :param training_data_tuple: a tuple contains a list of the words in a 
        sentence and a list of all the edges in the dependency structure
        :type training_data_tuple: tuple(list, set(tuple(integer, integer)))
        
        :return: updated feature set
        :rtype: FeatureSet
        """
        word_list, gold_edge_set = training_data_tuple
        while True:
            _, current_edge_set = \
               eisner.EisnerParser(word_list).parse(self.feature_set.get_local_scalar)
            
            # guarantee to converge ???????
            # will the eisner calculate the different trees?
            if current_edge_set == gold_edge_set:
                break
            
            # calculate the global score
            # assume the length of each local vector in the same sentanse is the same
            # the truth_global_vector will change because of the change in weights
            current_global_vector = self.get_global_vector(current_edge_set, word_list)
            glod_global_vector = self.get_global_vector(gold_edge_set, word_list)
            delta_vector = [(truth - current)
                             for truth, current
                             in zip(glod_global_vector, current_global_vector)]
            self.feature_set.update_weight_vector(delta_vector)
        return self.feature_set

    def get_global_vector(edge_set, word_list):
        """
        Calculate the global vector with the current weight, the order of the feature
        score is the same order as the feature set

        :param word_list: The list of ordered words in the sentence
        :type: list
        :param edge_set: the set of edges represented as tuples
        :type: list(tuple(integer, integer))

        :return: The global vector of the sentence with the current weight
        :rtype: list
        """
        global_vector = []
        for edge_tuple in edge_set:
            local_vector = self.feature_set.get_local_vector(word_list, edge_tuple)
            if global_vector == []:
                global_vector = [0 for i in range(len(local_vector))]
            global_vector = [(g+l) for g,l in zip(global_vector, local_vector)]
        return global_vector
