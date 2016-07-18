import os
import sys
import inspect
import time
import pos_viterbi
import logging
from pos_common import *

gottenFile = inspect.getfile(inspect.currentframe())
currentdir = os.path.dirname(os.path.abspath(gottenFile))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

logger = logging.getLogger('EVALUATOR')


class Decoder():
    def __init__(self, test_list=None, tag_file="file://tagset.txt", sparkContext=None):
        self.test_list = test_list
        self.tagset = read_tagset(tag_file, sparkContext)

    def sent_evaluate(self, result_list, gold_list):
        if len(result_list) != len(gold_list):
            raise ValueError("""
            TAGGER [ERRO]: Tag results do not align with gold results
            """)
        correct_num = 0
        for i in range(len(result_list)):
            if result_list[i] == gold_list[i]:
                correct_num += 1
        return correct_num, len(gold_list)

    def get_accuracy(self, w_vec):
        argmax = pos_viterbi.Viterbi()
        correct_num = gold_set_size = 0
        for (word_list, pos_list, fv) in self.test_list:
            output = argmax.perc_test(w_vec, word_list, self.tagset, "NN")
            cnum, gnum = self.sent_evaluate(output, pos_list)
            correct_num += cnum
            gold_set_size += gnum
        acc = float(correct_num) / gold_set_size
        logger.info("Total Accraccy: %f" % acc)
        return acc
