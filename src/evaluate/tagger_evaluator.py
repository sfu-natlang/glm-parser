from evaluate import logger, EvaluatorBase


class Evaluator(EvaluatorBase):
    def __init__(self, tagger, tagset):
        EvaluatorBase.__init__(self)
        self.tagger = tagger
        self.tagset = tagset
        return

    def sentence_evaluator(self, sent, w_vector):
        result_list = self.tagger.tag(sent, w_vector, self.tagset, "NN")
        gold_list = sent.get_pos_list()
        if len(result_list) != len(gold_list):
            raise ValueError("""
            TAGGER [ERRO]: Tag results do not align with gold results
            """)
        correct_num = 0
        for i in range(len(result_list)):
            if result_list[i] == gold_list[i]:
                correct_num += 1
        return correct_num, len(gold_list)
