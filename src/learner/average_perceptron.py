from __future__ import division
from weight.weight_vector import WeightVector
from learner import logger


class Learner(object):

    name = "AveragePerceptronLearner"

    def __init__(self, w_vector=None, max_iter=1):
        """
        :param w_vector: A global weight vector instance that stores
         the weight value (float)
        :param max_iter: Maximum iterations for training the weight vector
         Could be overridden by parameter max_iter in the method
        :return: None
        """
        logger.debug("Initialise AveragePerceptronLearner ... ")
        self.max_iter = max_iter
        self.total_sent = 0
        self.weight_sum_dict = {}
        return

    def sequential_learn(self, f_argmax, data_pool=None, max_iter=-1, d_filename=None, dump_freq = 1):
        if max_iter <= 0:
            max_iter = self.max_iter
        data_size = len(data_pool.data_list)
        logger.debug("Starting sequential train ... ")

        fv = {}

        # for t = 1 ... T
        for t in range(max_iter):
            logger.info("Starting Iteration %d" % t)
            logger.info("Initial Number of Keys: %d" % len(fv.keys()))

            vector_list = self.parallel_learn(data_pool=data_pool,
                                              init_w_vector=fv,
                                              f_argmax=f_argmax,
                                              log=True,
                                              info="Iteration %d, " % t)
            fv = self.iteration_proc(vector_list)
            if d_filename is not None:
                if t % dump_freq == 0 or t == max_iter - 1:
                    tmp = self.export()
                    tmp.dump(d_filename + "_Iter_%d.db" % (t + 1))

        return self.export()

    def parallel_learn(self, data_pool, init_w_vector, f_argmax, log=False, info=""):
        w_vector = WeightVector()
        weight_sum_dict = WeightVector()
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

            w_vector.iadd(gold_global_vector.feature_dict)
            w_vector.iaddc(current_global_vector.feature_dict, -1)

            weight_sum_dict.iadd(w_vector)
        data_pool.reset_index()

        vector_list = {}
        for key in weight_sum_dict.keys():
            vector_list[str(key)] = (w_vector[key], weight_sum_dict[key], 1)
        vector_list['sent_num'] = (0, 0, data_pool.get_sent_num())
        return vector_list.items()

    def iteration_proc(self, vector_list):
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
