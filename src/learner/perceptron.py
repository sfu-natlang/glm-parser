from __future__ import division
from weight.weight_vector import WeightVector
from learner.perceptron_base import PerceptronLearnerBase

from learner import logger
from feature.feature_vector import FeatureVector

__version__ = '1.0.0'


class Learner(PerceptronLearnerBase):

    name = "PerceptronLearner"

    def __init__(self, w_vector=None, max_iter=1):
        """
        :param w_vector: A global weight vector instance that stores
         the weight value (float)
        :return: None
        """
        PerceptronLearnerBase.__init__(self, w_vector)
        self.w_vector = {}
        return

    def _iteration_learn(self,
                         data_pool,
                         init_w_vector,
                         f_argmax,
                         log=False,
                         info=""):

        w_vector = WeightVector()
        for key in init_w_vector.keys():
            w_vector[key] = init_w_vector[key]
        sentence_count = 1

        while data_pool.has_next_data():
            data_instance = data_pool.get_next_data()
            if log:
                logger.info(info + "Sentence %d of %d, Length %d" % (
                            sentence_count,
                            data_pool.get_sent_num(),
                            len(data_instance.get_word_list()) - 1))
            sentence_count += 1

            gold_global_vector = FeatureVector(data_instance.gold_global_vector)
            current_global_vector = f_argmax(w_vector, data_instance)

            w_vector.iadd(gold_global_vector.feature_dict)
            w_vector.iaddc(current_global_vector.feature_dict, -1)

        data_pool.reset_index()

        vector_list = {}
        for key in w_vector.keys():
            vector_list[str(key)] = (w_vector[key], 1)

        return vector_list.items()

    def _iteration_proc(self, vector_list):
        w_vector = {}
        self.w_vector = {}
        for (feat, (weight, count)) in vector_list:
            self.w_vector[feat] = float(weight) / float(count)
            w_vector[feat] = float(weight) / float(count)
        return w_vector

    def export(self):
        w_vector = WeightVector()
        for feat in self.w_vector:
            w_vector[feat] = self.w_vector[feat]
        return w_vector
