import os
import sys
import inspect
import time
import pos_viterbi
import logging
from pos_common import read_tagset

gottenFile = inspect.getfile(inspect.currentframe())
currentdir = os.path.dirname(os.path.abspath(gottenFile))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

logger = logging.getLogger('EVALUATOR')


class Evaluator():
    def __init__(self):
        self.correct_num = 0
        self.gold_set_size = 0
        return

    def evaluate(self, data_pool, w_vector, tagset):
        self.correct_num = 0
        self.gold_set_size = 0

        def sent_evaluate(result_list, gold_list):
            if len(result_list) != len(gold_list):
                raise ValueError("""
                TAGGER [ERRO]: Tag results do not align with gold results
                """)
            self.correct_num = 0
            for i in range(len(result_list)):
                if result_list[i] == gold_list[i]:
                    self.correct_num += 1
            return self.correct_num, len(gold_list)

        argmax = pos_viterbi.Viterbi()

        logger.debug("Start evaluating ...")
        sentence_count = 1
        data_size = len(data_pool.data_list)
        while data_pool.has_next_data():
            sent = data_pool.get_next_data()

            logger.info("Sentence %d of %d, Length %d" % (
                sentence_count,
                data_size,
                len(sent.get_word_list()) - 1))
            sentence_count += 1

            output = argmax.tag(sent, w_vector, tagset, "NN")

            cnum, gnum = sent_evaluate(output, sent.get_pos_list())

            self.correct_num += cnum
            self.gold_set_size += gnum

        data_pool.reset_index()

        acc = float(self.correct_num) / self.gold_set_size
        logger.info("Feature count: %d" % len(w_vector.keys()))
        logger.info("Total Accraccy: %d" % acc)
        return acc
