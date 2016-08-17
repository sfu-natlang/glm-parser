import os
from weight.weight_vector import WeightVector
from data import data_pool
from learner import logger


class ParallelPerceptronLearner():

    def __init__(self, w_vector=None, max_iter=1):
        """
        :param w_vector: A global weight vector instance that stores
         the weight value (float)
        :param max_iter: Maximum iterations for training the weight vector
         Could be overridden by parameter max_iter in the method
        :return: None
        """
        logger.debug("Initialize ParallelPerceptronLearner ... ")
        self.w_vector = w_vector
        return

    def parallel_learn(self,
                       max_iter   = -1,
                       dataPool   = None,
                       shards     = 1,
                       f_argmax   = None,
                       learner    = None,
                       sc         = None,
                       d_filename = None,
                       hadoop     = False):
        '''
        This is the function which does distributed training using Spark


        :param max_iter: iterations for training the weight vector
        :param dir_name: the output directory storing the sharded data
        :param parser: parser for generating parse tree
        '''

        def create_dp(textString, fgen, format, comment_sign):
            dp = data_pool.DataPool(fgen         = fgen,
                                    format_list  = format,
                                    textString   = textString[1],
                                    comment_sign = comment_sign)
            return dp

        def get_sent_num(dp):
            return dp.get_sent_num()

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

        fv = {}
        total_sent = dp.map(get_sent_num).sum()
        logger.info("Totel number of sentences: %d" % total_sent)

        for iteration in range(max_iter):
            logger.info("Starting Iteration %d" % iteration)
            logger.info("Initial Number of Keys: %d" % len(fv.keys()))
            # mapper: computer the weight vector in each shard using parallel_learn
            w_vector_list = dp.flatMap(lambda t: learner.parallel_learn(data_pool=t,
                                                                        init_w_vector=fv,
                                                                        f_argmax=f_argmax))
            # reducer: combine the weight vectors from each shard
            # value is the tuple returned by parallel_learn
            # value[0] is w_vector[key]
            # value[1] is weight_sum_dict[key]
            w_vector_list = w_vector_list.combineByKey(
                lambda value: value,
                lambda x, value: tuple(map(sum, zip(x, value))),
                lambda x, y: tuple(map(sum, zip(x, y)))).collect()

            fv = learner.iteration_proc(w_vector_list)
            logger.info("Iteration complete, total number of keys: %d" % len(fv.keys()))

        self.w_vector = learner.export()

        if d_filename is not None:
            logger.info("Dumping trained weight vector")
            self.w_vector.dump(d_filename + "_Iter_%d.db" % max_iter, sc)
        return self.w_vector
