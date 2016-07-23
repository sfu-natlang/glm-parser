from hvector._mycollections import mydefaultdict
from hvector.mydouble import mydouble
from weight import weight_vector
from data import data_pool
import perceptron
import debug.debug
import sys
import os
import shutil
import re
import importlib
from os.path import isfile, join, isdir
from pyspark import SparkContext
from learn import logger


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
            dp = data_pool.DataPool(textString   = textString[1],
                                    fgen         = fgen,
                                    format_list  = format,
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

        if learner.name == "AveragePerceptronLearner":
            logger.info("Using Averaged Perceptron Learner")
            fv = {}
            total_sent = dp.map(get_sent_num).sum()
            c = total_sent * max_iter
            for iteration in range(max_iter):
                logger.info("Starting Iteration %d" % iteration)
                # mapper: computer the weight vector in each shard using parallel_learn
                feat_vec_list = dp.flatMap(lambda t: learner.parallel_learn(dp=t,
                                                                            fv=fv,
                                                                            f_argmax=f_argmax))
                # reducer: combine the weight vectors from each shard
                feat_vec_list = feat_vec_list.combineByKey(
                    lambda value: (value[0], value[1], 1),
                    lambda x, value: (x[0] + value[0], x[1] + value[1], x[2] + 1),
                    lambda x, y: (x[0] + y[0], x[1] + y[1], x[2] + y[2])).collect()

                fv = {}
                for (feat, (a, b, c)) in feat_vec_list:
                    fv[feat] = (float(a) / float(c), b)
                logger.info("Iteration complete, total number of keys: %d" % len(fv.keys()))

            self.w_vector.clear()
            for feat in fv.keys():
                self.w_vector[feat] = fv[feat][1] / c

        if learner.name == "PerceptronLearner":
            logger.info("Using Perceptron Learner")
            fv = {}
            for iteration in range(max_iter):
                logger.info("Starting Iteration %d" % iteration)
                logger.info("Initial Number of Keys: %d" % len(fv.keys()))
                # mapper: computer the weight vector in each shard using parallel_learn
                feat_vec_list = dp.flatMap(lambda t: learner.parallel_learn(dp=t,
                                                                            fv=fv,
                                                                            f_argmax=f_argmax))
                # reducer: combine the weight vectors from each shard
                feat_vec_list = feat_vec_list.combineByKey(
                    lambda value: (value, 1),
                    lambda x, value: (x[0] + value, x[1] + 1),
                    lambda x, y: (x[0] + y[0], x[1] + y[1])).collect()

                fv = {}
                for (feat, (a, b)) in feat_vec_list:
                    fv[feat] = float(a) / float(b)
                logger.info("Iteration complete")
            self.w_vector.clear()
            self.w_vector.iadd(fv)

        if d_filename is not None:
            if hadoop is False:
                logger.info("Dumping trained weight vector to local directory: " +
                       d_filename)
                self.w_vector.dump(d_filename + "_Iter_%d.db" % max_iter)
            else:
                logger.info("Dumping trained weight vector")
                contents = []
                for k, v in w_vector.iteritems():
                    contents.append(str(k) + "    " + str(v) + "\n")
                logger.info("Dumping to: " + fileWrite(d_filename + "_Iter_%d.db" % max_iter, contents, sc))
        return self.w_vector
