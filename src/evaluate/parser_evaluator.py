from evaluate import logger, EvaluatorBase


class Evaluator(EvaluatorBase):
    def __init__(self, parser, tagger):
        EvaluatorBase.__init__(self)
        self.parser = parser
        self.tagger = tagger
        return

    def __sentence_evaluator(self, sent, w_vector):
        gold_edge_set = \
            set([(head_index, dep_index)
                for head_index, dep_index, _ in sent.get_edge_list()])

        sent_len = len(sent.get_word_list())
        test_edge_set = \
            self.parser.parse(sent, w_vector.get_vector_score, self.tagger)

        if isinstance(test_edge_set, list):
            test_edge_set = set(test_edge_set)

        if isinstance(gold_edge_set, list):
            gold_edge_set = set(gold_edge_set)

        intersect_set = test_edge_set.intersection(gold_edge_set)
        correct_num = len(intersect_set)
        gold_set_size = len(gold_edge_set)
        return correct_num, gold_set_size

    def sequentialEvaluate(self,
                           data_pool,
                           w_vector,
                           sparkContext=None,
                           hadoop=None):

        return EvaluatorBase.sequentialEvaluate(self,
                                                data_pool,
                                                w_vector,
                                                self.__sentence_evaluator,
                                                sparkContext,
                                                hadoop)

    def parallelEvaluate(self,
                         data_pool,
                         w_vector,
                         sparkContext,
                         hadoop):

        return EvaluatorBase.parallelEvaluate(self,
                                              data_pool,
                                              w_vector,
                                              self.__sentence_evaluator,
                                              sparkContext,
                                              hadoop)
