from weight.weight_vector import WeightVector
from data.data_pool import DataPool

import debug.debug
import time
from learner import logger

__version__ = '1.0.0'


class PerceptronLearnerBase:

    name = "PerceptronLearnerBase"

    def __init__(self, w_vector):
        self.w_vector = {}
        for key in w_vector.keys():
            self.w_vector[key] = w_vector[key]
        return

    def __iteration_learn(self,
                          data_pool,
                          init_w_vector,
                          f_argmax,
                          log=False,
                          info=""):
        raise NotImplemented

    def __iteration_proc(self):
        raise NotImplemented

    def export():
        raise NotImplemented

    def sequential_learn(self,
                         f_argmax,
                         data_pool,
                         iterations=1,
                         d_filename=None,
                         dump_freq=1):

        logger.info("Starting sequential train")
        logger.info("Using Learner: " + self.name)

        self.w_vector = {}

        # for t = 1 ... T
        for t in range(iterations):
            logger.info("Starting Iteration %d" % t)
            logger.info("Initial Number of Keys: %d" % len(self.w_vector.keys()))

            vector_list = self.__iteration_learn(data_pool=data_pool,
                                                 init_w_vector=self.w_vector,
                                                 f_argmax=f_argmax,
                                                 log=True,
                                                 info="Iteration %d, " % t)

            self.w_vector = self.__iteration_proc(vector_list)
            logger.info("Iteration complete, total number of keys: %d" % len(self.w_vector.keys()))

            if d_filename is not None:
                if t % dump_freq == 0 or t == iterations - 1:
                    tmp = self.export()
                    tmp.dump(d_filename + "_Iter_%d.db" % (t + 1))

        return self.export()

    def parallel_learn(self,
                       f_argmax,
                       data_pool,
                       iteration=1,
                       d_filename=None,
                       dump_freq=1,
                       sparkContext=None
                       hadoop=False):

        def create_dp(textString, fgen, format, comment_sign):
            dp = data_pool.DataPool(fgen         = fgen,
                                    format_list  = format,
                                    textString   = textString[1],
                                    comment_sign = comment_sign)
            return dp

        def get_sent_num(dp):
            return dp.get_sent_num()

        sc = sparkContext

        dir_name     = dataPool.loadedPath()
        format_list  = dataPool.format_list
        comment_sign = dataPool.comment_sign
        fgen         = dataPool.fgen

        # By default, when the hdfs is configured for spark, even in local mode it will
        # still try to load from hdfs. The following code is to resolve this confusion.
        if hadoop is True:
            train_files = sc.wholeTextFiles(dir_name, minPartitions=10).cache()
        else:
            dir_name = os.path.abspath(os.path.expanduser(dir_name))
            train_files = sc.wholeTextFiles("file://" + dir_name, minPartitions=10).cache()

        dp = train_files.map(lambda t: create_dp(textString   = t,
                                                 fgen         = fgen,
                                                 format       = format_list,
                                                 comment_sign = comment_sign)).cache()

        self.w_vector = {}
        logger.info("Totel number of sentences: %d" % dp.map(get_sent_num).sum())

        for t in range(iterations):
            logger.info("Starting Iteration %d" % iteration)
            logger.info("Initial Number of Keys: %d" % len(self.w_vector.keys()))

            w_vector_list = dp.flatMap(
                lambda t: self.__iteration_learn(data_pool=t,
                                                 init_w_vector=self.w_vector,
                                                 f_argmax=f_argmax))

            w_vector_list = w_vector_list.combineByKey(
                lambda value: value,
                lambda x, value: tuple(map(sum, zip(x, value))),
                lambda x, y: tuple(map(sum, zip(x, y)))).collect()

            self.w_vector = self.__iteration_proc(w_vector_list)
            logger.info("Iteration complete, total number of keys: %d" % len(self.w_vector.keys()))

            if d_filename is not None:
                if t % dump_freq == 0 or t == iterations - 1:
                    tmp = self.export()
                    tmp.dump(d_filename + "_Iter_%d.db" % (t + 1), sparkContext)

        return self.export()
