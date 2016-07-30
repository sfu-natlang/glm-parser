from __future__ import division
import multiprocessing
from weight.weight_vector import WeightVector

import debug.debug
import time
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
        self.w_vector = w_vector
        self.max_iter = max_iter

        if w_vector is not None:
            self.weight_sum_dict = WeightVector()
        return

    def sequential_learn(self, f_argmax, data_pool=None, max_iter=-1, d_filename=None, dump_freq = 1):
        if max_iter <= 0:
            max_iter = self.max_iter
        data_size = len(data_pool.data_list)
        logger.debug("Starting sequential train ... ")

        # sigma_s
        self.weight_sum_dict.clear()

        # for t = 1 ... T
        for t in range(max_iter):
            logger.debug("Iteration %d" % t)
            sentence_count = 1
            argmax_time_total = 0.0

            # for i = 1 ... m
            while data_pool.has_next_data():
                # Retrieve data
                data_instance = data_pool.get_next_data()
                gold_global_vector = data_instance.convert_list_vector_to_dict(data_instance.gold_global_vector)

                logger.info("Iteration %d, Sentence %d of %d, Length %d" % (
                    t,
                    sentence_count,
                    data_size,
                    len(data_instance.get_word_list()) - 1))
                sentence_count += 1

                # argmax
                if debug.debug.time_accounting_flag is True:
                    # with timer
                    before_time = time.clock()
                    current_global_vector = f_argmax(self.w_vector, data_instance)
                    after_time = time.clock()
                    time_usage = after_time - before_time
                    argmax_time_total += time_usage
                    logger.info("Sentence length: %d" % (len(data_instance.get_word_list()) - 1))
                    logger.info("Time usage: %f" % (time_usage, ))
                else:
                    # without timer
                    current_global_vector = f_argmax(self.w_vector, data_instance)

                self.w_vector.iadd(gold_global_vector.feature_dict)
                self.w_vector.iaddc(current_global_vector.feature_dict, -1)

                self.weight_sum_dict.iadd(self.w_vector)
            data_pool.reset_index()

            if d_filename is not None:
                if t % dump_freq == 0 or t == max_iter - 1:
                    tmp = WeightVector()
                    tmp.iaddc(self.weight_sum_dict, 1 / float((t + 1) * data_size))
                    tmp.dump(d_filename + "_Iter_%d.db" % (t + 1))

        self.w_vector.clear()
        self.w_vector.iaddc(self.weight_sum_dict, 1 / float(max_iter * data_size))

        return self.w_vector

    def parallel_learn(self, dp, fv, f_argmax):
        w_vector = WeightVector()
        weight_sum_dict = WeightVector()
        for key in fv.keys():
            w_vector[key] = fv[key][0]
            weight_sum_dict[key] = fv[key][1]

        while dp.has_next_data():
            data_instance = dp.get_next_data()
            gold_global_vector = data_instance.convert_list_vector_to_dict(data_instance.gold_global_vector)
            current_global_vector = f_argmax(w_vector, data_instance)

            w_vector.iadd(gold_global_vector.feature_dict)
            w_vector.iaddc(current_global_vector.feature_dict, -1)

            weight_sum_dict.iadd(w_vector)
        dp.reset_index()

        vector_list = {}
        for key in weight_sum_dict.keys():
            vector_list[str(key)] = (w_vector[key], weight_sum_dict[key])
        return vector_list.items()
