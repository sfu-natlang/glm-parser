import logging
from hvector._mycollections import mydefaultdict
from hvector.mydouble import mydouble
from weight import weight_vector 
from data import data_pool
import perceptron
import debug.debug
import sys,os,shutil,re
from os.path import isfile, join, isdir
from pyspark import SparkContext


logging.basicConfig(filename='glm_parser.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

class ParallelPerceptronLearner():

    def __init__(self, w_vector=None, max_iter=1):
        """
        :param w_vector: A global weight vector instance that stores
         the weight value (float)
        :param max_iter: Maximum iterations for training the weight vector
         Could be overridden by parameter max_iter in the method
        :return: None
        """
        logging.debug("Initialize ParallelPerceptronLearner ... ")
        self.w_vector = w_vector
        return

    def parallel_learn(self, max_iter=-1, dir_name=None, shards=1, fgen=None,parser=None,config_path=None,learner=None):
        '''
        This is the function which does distributed training using Spark
        TODO: rewrite weight_vector to cache the golden feature as a rdd
        
        :param max_iter: iterations for training the weight vector
        :param dir_name: the output directory storing the sharded data
        :param fgen: feature generator
        :param parser: parser for generating parse tree
        '''

        def create_dp(textString,fgen,config):
            dp = data_pool.DataPool(textString=textString[1],fgen=fgen,config_list=config)
            return dp

        fconfig = open(config_path)
        config_list = []
    
        for line in fconfig:
            config_list.append(line.strip())
        fconfig.close() 

        nodes_num = "local[%d]"%shards
        sc = SparkContext(master=nodes_num)
        train_files= sc.wholeTextFiles(dir_name).cache()

        fv = {}
        for key in self.w_vector.data_dict.keys():
            fv[str(key)]=w_vector.data_dict[key]

        dp = train_files.map(lambda t: create_dp(t,fgen=fgen,config=config_list)).cache()

        for round in range(max_iter):
            weight_vector = sc.broadcast(fv)
            #mapper: computer the weight vector in each shard using avg_perc_train
            feat_vec_list = dp.flatMap(lambda t: learner.parallel_learn(t,weight_vector.value,parser))
            #reducer: combine the weight vectors from each shard
            feat_vec_list = feat_vec_list.combineByKey(lambda value: (value, 1),
                             lambda x, value: (x[0] + value, x[1] + 1),
                             lambda x, y: (x[0] + y[0], x[1] + y[1])).collect()
            for (feat, (a,b)) in feat_vec_list:
                fv[feat] = float(a)/float(b)
        self.w_vector.data_dict.clear()
        self.w_vector.data_dict.iadd(fv)

        sc.stop()

        # delete the sharded files
        for the_file in os.listdir(dir_name):
            file_path = os.path.join(dir_name, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception, e:
                print e

        



    
