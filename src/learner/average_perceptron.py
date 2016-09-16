from __future__ import division
from weight.weight_vector import WeightVector
from learner.perceptron_base import PerceptronLearnerBase

from learner import logger

__version__ = '1.0.0'


class Learner(PerceptronLearnerBase):

    name = "AveragePerceptronLearner"

    def __init__(self, w_vector=None):
        """
        :param w_vector: A global weight vector instance that stores
         the weight value (float)
        :return: None
        """
        PerceptronLearnerBase.__init__(self, w_vector)
        self.total_sent = 0
        self.weight_sum_dict = {}
        return

    def _iteration_learn(self,
                         data_pool,
                         init_w_vector,
                         f_argmax,
                         log=False,
                         info=""):

        w_vector = WeightVector()
        weight_sum_dict = WeightVector()
        last_change_dict = WeightVector()
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
            gold_global_vector = data_instance.convert_list_vector_to_dict(data_instance.gold_global_vector)
            current_global_vector = f_argmax(w_vector, data_instance)

            delta_global_vector = gold_global_vector - current_global_vector

            # update every iteration (more convenient for dump)
            if data_pool.has_next_data():
                if not current_global_vector == gold_global_vector:
                    for s in delta_global_vector.keys():
                        weight_sum_dict[s] += w_vector[s] * (sentence_count - last_change_dict[s])
                        last_change_dict[s] = sentence_count

                    w_vector.iadd(delta_global_vector.feature_dict)
                    weight_sum_dict.iadd(delta_global_vector.feature_dict)
            else:
                for s in last_change_dict.keys():
                    weight_sum_dict[s] += w_vector[s] * (sentence_count - last_change_dict[s])
                    last_change_dict[s] = sentence_count

                if not current_global_vector == gold_global_vector:
                    w_vector.iadd(delta_global_vector.feature_dict)
                    weight_sum_dict.iadd(delta_global_vector.feature_dict)

        data_pool.reset_index()

        vector_list = {}
        for key in weight_sum_dict.keys():
            vector_list[str(key)] = (w_vector[key], weight_sum_dict[key], 1)
        vector_list['sent_num'] = (0, 0, data_pool.get_sent_num())
        return vector_list.items()

    def _iteration_proc(self, vector_list):
        w_vector = {}
        for (feat, (weight, weight_sum, count)) in vector_list:
            if feat == 'sent_num':
                self.total_sent += count
            else:
                w_vector[feat] = float(weight) / float(count)
                if feat not in self.weight_sum_dict:
                    self.weight_sum_dict[feat] = 0
                self.weight_sum_dict[feat] += float(weight_sum)
        return w_vector

    def export(self):
        w_vector = WeightVector()
        for feat in self.weight_sum_dict:
            w_vector[feat] = self.weight_sum_dict[feat] / self.total_sent
        return w_vector
