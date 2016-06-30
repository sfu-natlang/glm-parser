from __future__ import division
import logging
import multiprocessing
from weight.weight_vector import WeightVector

import debug.debug
import time

logging.basicConfig(filename='glm_parser.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

class Learner(object):

    def __init__(self, w_vector=None, max_iter=1):
        """
        :param w_vector: A global weight vector instance that stores
         the weight value (float)
        :param max_iter: Maximum iterations for training the weight vector
         Could be overridden by parameter max_iter in the method
        :return: None
        """
        logging.debug("Initialize AveragePerceptronLearner ... ")
        self.w_vector = w_vector
        self.max_iter = max_iter

        if w_vector is not None:
            self.weight_sum_dict = WeightVector()
            self.last_change_dict = WeightVector()
            self.c = 1
        return

    def learner_name(self):
        return "AveragePerceptronLearner"

    def sequential_learn(self, f_argmax, data_pool=None, max_iter=-1, d_filename=None, dump_freq = 1):
        if max_iter <= 0:
            max_iter = self.max_iter

        logging.debug("Starting sequential train ... ")

        # sigma_s
        self.weight_sum_dict.clear()
        self.last_change_dict.clear()
        self.c = 1

        # for t = 1 ... T
        for t in range(max_iter):
            logging.debug("Iteration: %d" % t)
            logging.debug("Data size: %d" % len(data_pool.data_list))
            sentence_count = 1
            argmax_time_total = 0.0

            # for i = 1 ... m
            while data_pool.has_next_data():
                print("Iteration: %d, Sentence %d" % (t, sentence_count))
                sentence_count += 1
                # Calculate yi' = argmax
                data_instance = data_pool.get_next_data()
                gold_global_vector = data_instance.convert_list_vector_to_dict(data_instance.gold_global_vector)

                if debug.debug.time_accounting_flag is True:
                    before_time = time.clock()
                    current_global_vector = f_argmax(self.w_vector, data_instance)
                    after_time = time.clock()
                    time_usage = after_time - before_time
                    argmax_time_total += time_usage
                    print("Sentence length: %d" % (len(data_instance.get_word_list()) - 1))
                    print("Time usage: %f" % (time_usage, ))
                    logging.debug("Time usage %f" % (time_usage, ))
                else:
                    # Just run the procedure without any interference
                    current_global_vector = f_argmax(self.w_vector, data_instance)

                delta_global_vector = gold_global_vector - current_global_vector

                # update every iteration (more convenient for dump)
                if data_pool.has_next_data():
                    # i yi' != yi
                    if not current_global_vector == gold_global_vector:
                        # for each element s in delta_global_vector
                        for s in delta_global_vector.keys():
                            self.weight_sum_dict[s] += self.w_vector[s] * (self.c - self.last_change_dict[s])
                            self.last_change_dict[s] = self.c

                        # update weight and weight sum
                        self.w_vector.iadd(delta_global_vector.feature_dict)
                        self.weight_sum_dict.iadd(delta_global_vector.feature_dict)

                else:
                    for s in self.last_change_dict.keys():
                        self.weight_sum_dict[s] += self.w_vector[s] * (self.c - self.last_change_dict[s])
                        self.last_change_dict[s] = self.c

                    if not current_global_vector == gold_global_vector:
                        self.w_vector.iadd(delta_global_vector.feature_dict)
                        self.weight_sum_dict.iadd(delta_global_vector.feature_dict)

                self.c += 1

                if debug.debug.log_feature_request_flag is True:
                    data_instance.dump_feature_request("%s" % (sentence_count, ))

                # If exceeds the value set in debug config file, just stop and exit
                # immediately
                if sentence_count > debug.debug.run_first_num > 0:
                    print("Average time for each sentence: %f" % (argmax_time_total / debug.debug.run_first_num))
                    logging.debug("Average time for each sentence: %f" % (argmax_time_total / debug.debug.run_first_num))
                    data_pool.reset_index()
                    sentence_count = 1
                    argmax_time_total = 0.0

            # End while(data_pool.has_next_data())

            # Reset index, while keeping the content intact
            data_pool.reset_index()

            if d_filename is not None:
                if t % dump_freq == 0 or t == max_iter - 1:
                    p_fork = multiprocessing.Process(
                        target=self.dump_vector,
                        args=(d_filename, t))

                    p_fork.start()
                    #self.w_vector.dump(d_filename + "_Iter_%d.db"%t)

        self.w_vector.clear()

        self.avg_weight(self.w_vector, self.c - 1)

        return

    def avg_weight(self, w_vector, count):
        if count > 0:
            w_vector.iaddc(self.weight_sum_dict, 1 / count)

    def dump_vector(self, d_filename, i):
        d_vector = WeightVector()
        self.avg_weight(d_vector, self.c-1)
        d_vector.dump(d_filename + "_Iter_%d.db"%i)
        d_vector.clear()

    def parallel_learn(self, dp, fv, parser):
        w_vec = WeightVector()
        weight_sum_dict = WeightVector()
        print "parallel_learn keys: %d"%len(fv.keys())
        for key in fv.keys():
            w_vec[key]=fv[key][0]
            weight_sum_dict[key]=fv[key][1]

        while dp.has_next_data():
            data_instance = dp.get_next_data()
            gold_global_vector = data_instance.convert_list_vector_to_dict(data_instance.gold_global_vector)
            current_edge_set = parser.parse(data_instance, w_vec.get_vector_score)
            current_global_vector = data_instance.set_current_global_vector(current_edge_set)

            delta_global_vector = gold_global_vector - current_global_vector
            weight_sum_dict.iadd(w_vec)
            if not current_global_vector == gold_global_vector:
                w_vec.iadd(delta_global_vector.feature_dict)
                weight_sum_dict.iadd(delta_global_vector.feature_dict)
        dp.reset_index()

        vector_list = {}
        for key in weight_sum_dict.keys():
            vector_list[str(key)] = (w_vec[key],weight_sum_dict[key])
        return vector_list.items()
