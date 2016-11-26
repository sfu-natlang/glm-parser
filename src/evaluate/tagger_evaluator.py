from evaluate import logger, EvaluatorBase


class Evaluator(EvaluatorBase):
    def __init__(self, tagger, tagset):
        EvaluatorBase.__init__(self)
        self.tagger = tagger
        self.tagset = tagset
        return

    def sentence_evaluator(self, sent, w_vector):
        local_output = self.tagger.tag(sent, w_vector, self.tagset, self.tagset[0])
        gold_output = sent.get_gold_output()
        if len(local_output) != len(gold_output):
            raise ValueError("""
            TAGGER [ERRO]: Tag results do not align with gold results
            """)
        correct_num = 0
        for i in range(len(local_output)):
            if local_output[i] == gold_output[i]:
                correct_num += 1
        return correct_num, len(gold_output), local_output
