# -*- coding: utf-8 -*-
import feature_set, data_set, feature_vector, dependency_tree
import ceisner
import timeit

class WeightLearner():
    """
    Learns the weight of the features using maximum perceptron algorithm
    """
    
    def __init__(self, iter_num=1):
        """
        Initialize the WeightLearner
        """
        self.MAX_ITERATE = 1
        self.fset = feature_set.FeatureSet(
                    dependency_tree.DependencyTree(),
                    'weight.db')
        return    
    
    def learn_weight_sections(self, section_set=None, data_path=None, output_file='weight'):
        """
        Given the path and specified sections, 
        for each dep_tree in the source
        learn the weight for each feature in that feature set
        
        :param section_set: see section_set in DataSet
        :type section_set: list(int/tuple)
        
        :param data_path: see data_path in DataSet
        :type data_path: str
        """
        dataset = data_set.DataSet(section_set, data_path)
        for i in range(self.MAX_ITERATE):
            while dataset.has_next_data():
                self.update_weight(dataset.get_next_data())  
            self.fset.dump(output_file+'_iter_'+str(i)+'.db')
            self.fset.close()
            dataset.reset()
        return self.fset
            
    def learn_weight_sentences(self,file_name,index=0,data_path=None):
        """
        Given the location for one sentence in the source
        update the weight of the features in that sentence
        
        :param file_name: name of the file that contains the sentence
        :type file_name: str
        
        :param index: location of the sentence in that file, 
                      default 0 (1st sentence)
        :type index: int
        
        :param data_path: path to the data source
        :type data_path: int
        """
        dataset = data_set.DataSet(data_path=data_path)
        self.update_weight(dataset.get_data(file_name, index))
        #TODO add dump file name
        self.fset.dump()
        self.fset.close()
        return
        
    def update_weight(self,dep_tree):
        """
        Given one dependency tree, the function update the weight 
        for each feature in this sentence
        
        :param dep_tree: a class contains the information about the
        word_list, pos_list, edge and the information of edge type
        :type dep_tree: DependencyTree
        
        :return: updated feature set
        :rtype: FeatureSet
        """
        self.fset.switch_tree(dep_tree)
        word_list = dep_tree.get_word_list()
        gold_edge_set = \
            set([(head_index,dep_index) for head_index,dep_index,_ in dep_tree.get_edge_list()])
        #print "gold set:", gold_edge_set
        t = timeit.default_timer()
        
        current_edge_set = \
               ceisner.EisnerParser().parse(len(word_list), self.fset.get_edge_score)
        t = (timeit.default_timer() - t)
        print "eisner time:", t, "sec     sent_length:", str(len(word_list))
        
        if current_edge_set == gold_edge_set:
            return
        
        # calculate the global score
        # assume the length of each local vector in the same sentanse is the same
        # the truth_global_vector will change because of the change in weights
        current_global_vector = self.get_global_vector(current_edge_set)
        #print current_edge_set
        gold_global_vector = self.get_global_vector(gold_edge_set)
        gold_global_vector.eliminate(current_global_vector)
        # print gold_global_vector.feature_dict
        self.fset.update_weight_vector(gold_global_vector)
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
        global_vector = feature_vector.FeatureVector()
        for head_index,dep_index in edge_set:
            local_vector = self.fset.get_local_vector(head_index,dep_index)
            global_vector.aggregate(local_vector)
        return global_vector
        
        
    def get_feature_set(self):
        """
        :return: the updated feature set
        :rtype: FeatureSet
        """
        return self.fset
