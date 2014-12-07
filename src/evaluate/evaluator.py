from __future__ import division
import logging

logging.basicConfig(filename='glm_parser.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


class Evaluator():
    def __init__(self):
        self.unlabeled_correct_num = 0
        self.unlabeled_gold_set_size = 0
        return
        
    def reset(self):
        self.unlabeled_correct_num = 0
        self.unlabeled_gold_set_size = 0
        return

    def get_statistics(self):
        return self.unlabeled_correct_num, self.unlabeled_gold_set_size

    def _sent_unlabeled_accuracy(self, result_edge_set, gold_edge_set):      
        if isinstance(result_edge_set, list):
            result_edge_set = set(result_edge_set)
        else:
        	print "result not set"
        
        if isinstance(gold_edge_set, list):
            gold_edge_set = set(gold_edge_set)
        else:
        	print "gold not set"
        
        intersect_set = result_edge_set.intersection(gold_edge_set)
        correct_num = len(intersect_set)
        gold_set_size = len(gold_edge_set)
        
        return correct_num, gold_set_size

    def evaluate(self, data_pool, parser, w_vector):
        logging.debug("Start evaluating ...")
        logging.info("Feature count: %d" % len(w_vector.data_dict))
        while data_pool.has_next_data():  
            sent = data_pool.get_next_data()
            
            gold_edge_set = \
                set([(head_index,dep_index) for head_index,dep_index,_ in sent.get_edge_list()])
            
            sent_len = len(sent.get_word_list())
            test_edge_set = \
               parser.parse(sent, w_vector.get_vector_score)
             
            #print "sent acc:", 
            self.unlabeled_accuracy(test_edge_set, gold_edge_set, True)
            #print "acc acc:", self.evlt.get_acc_unlabeled_accuracy()
        logging.info("Unlabeled accuracy: %.12f (%d, %d)" % (self.get_acc_unlabeled_accuracy(), self.unlabeled_correct_num, self.unlabeled_gold_set_size))

        self.unlabeled_attachment_accuracy(data_pool.get_sent_num())
        logging.info("Unlabeled attachment accuracy: %.12f (%d, %d)" % (self.get_acc_unlabeled_accuracy(), self.unlabeled_correct_num, self.unlabeled_gold_set_size))

    
    def unlabeled_accuracy(self, result_edge_set, gold_edge_set, accumulate=False):
        """
        calculate unlabeled accuracy of the glm-parser
        unlabeled accuracy = # of corrected edges in result / # of all corrected edges
        
        :param result_edge_set: the edge set that needs to be evaluated
        :type result_edge_set: list/set
        
        :param gold_edge_set: the gold edge set used for evaluating
        :type gold_edge_set: list/set
        
        :param accumulate:  True -- if evaluation result needs to be remembered
                            False (default) -- if result does not needs to be remembered 
        :type accumulate: boolean
        
        :return: the unlabeled accuracy
        :rtype: float
        """
        correct_num, gold_set_size =\
            self._sent_unlabeled_accuracy(result_edge_set, gold_edge_set)
            
        if accumulate == True:          
            self.unlabeled_correct_num += correct_num
            #correct_num = self.unlabeled_correct_num
            
            self.unlabeled_gold_set_size += gold_set_size
            #gold_set_size = self.unlabeled_gold_set_size
            print correct_num, gold_set_size, self.unlabeled_correct_num, self.unlabeled_gold_set_size 
        return correct_num / gold_set_size
        
    def get_acc_unlabeled_accuracy(self):
        return self.unlabeled_correct_num / self.unlabeled_gold_set_size

    def unlabeled_attachment_accuracy(self, sent_num):
        """
        calculate unlabled attachment accuracy of glm-parser
        unlabeled attachment accuracy = # of corrected tokens in result / # of all corrected tokens
        # of corrected tokens in result = # of corrected edges in result + # of sentences in data set
        # of all corrected tokens = # of all corrected edges + # of sentences in data set
        """
        
        self.unlabeled_correct_num += sent_num
        self.unlabeled_gold_set_size += sent_num
        
        return
