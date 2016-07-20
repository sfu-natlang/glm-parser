from __future__ import division
from pos_tagger import PosTagger
import logging

logger = logging.getLogger('EVALUATOR')


class Evaluator():
    def __init__(self):
        self.unlabeled_correct_num = 0
        self.unlabeled_gold_set_size = 0
        return

    def get_statistics(self):
        return self.unlabeled_correct_num, self.unlabeled_gold_set_size

    def _sent_unlabeled_accuracy(self, result_edge_set, gold_edge_set):
        if isinstance(result_edge_set, list):
            result_edge_set = set(result_edge_set)

        if isinstance(gold_edge_set, list):
            gold_edge_set = set(gold_edge_set)

        intersect_set = result_edge_set.intersection(gold_edge_set)
        correct_num = len(intersect_set)
        gold_set_size = len(gold_edge_set)

        logger.debug("result edge set: ")
        logger.debug(result_edge_set)
        logger.debug("gold edge set: ")
        logger.debug(gold_edge_set)
        logger.debug("##############")

        return correct_num, gold_set_size

    def evaluate(self, data_pool, parser, w_vector, tagger=None, sc=None, hadoop=None):
        self.unlabeled_correct_num = 0
        self.unlabeled_gold_set_size = 0

        logger.debug("Start evaluating ...")
        sentence_count = 1
        data_size = len(data_pool.data_list)
        while data_pool.has_next_data():
            sent = data_pool.get_next_data()

            if not hadoop:
                logger.info("Sentence %d of %d, Length %d" % (
                    sentence_count,
                    data_size,
                    len(sent.get_word_list()) - 1))
            sentence_count += 1

            logger.debug("data instance: ")
            logger.debug(sent.get_word_list())
            logger.debug(sent.get_edge_list())

            gold_edge_set = \
                set([(head_index, dep_index) for head_index, dep_index, _ in sent.get_edge_list()])

            sent_len = len(sent.get_word_list())
            test_edge_set = \
                parser.parse(sent, w_vector.get_vector_score, tagger)

            self.unlabeled_accuracy(test_edge_set, gold_edge_set, True)
        data_pool.reset_index()

        logger.info("Feature count: %d" % len(w_vector.keys()))
        logger.info("Unlabeled accuracy: %.12f (%d, %d)" % (self.get_acc_unlabeled_accuracy(), self.unlabeled_correct_num, self.unlabeled_gold_set_size))
        self.unlabeled_attachment_accuracy(data_pool.get_sent_num())
        logger.info("Unlabeled attachment accuracy: %.12f (%d, %d)" % (self.get_acc_unlabeled_accuracy(), self.unlabeled_correct_num, self.unlabeled_gold_set_size))

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

        if accumulate is True:
            self.unlabeled_correct_num += correct_num
            self.unlabeled_gold_set_size += gold_set_size
            logger.debug("Correct_num: %d, Gold set size: %d, Unlabeled correct: %d, Unlabeled gold set size: %d" % (correct_num, gold_set_size, self.unlabeled_correct_num, self.unlabeled_gold_set_size))

        # WARNING: this function returns a value but the caller does not use it!
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
