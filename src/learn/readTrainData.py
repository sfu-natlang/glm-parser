# -*- coding: utf-8 -*-
from __future__ import division
import os,sys,inspect
from os import listdir
from os.path import isfile, join, isdir
from data import data_pool
from pyspark import SparkContext
from hvector._mycollections import mydefaultdict
from hvector.mydouble import mydouble
from weight.weight_vector import *
from operator import add
N = 2 # number of shards

class Learner():

	def __init__(self, fgen, parser):
		self.fgen = fgen
		self.parser = parser()
		return

	def spark_train(self, output_dir, max_iter):
		w_vector = WeightVector()

		sc = SparkContext(appName="sampleApp",master="local[4]")
		train_files= sc.wholeTextFiles(output_dir)
		fv = {}
		for round in range(2):
			weight_vector = sc.broadcast(fv)
			feat_vec_list = train_files.flatMap(lambda t: self.avg_perc_train(t,self.parser,fv,self.fgen))
			feat_vec_list = feat_vec_list.combineByKey(lambda value: (value, 1),
                             lambda x, value: (x[0] + value, x[1] + 1),
                             lambda x, y: (x[0] + y[0], x[1] + y[1])).collect()
		
			for (feat, (a,b)) in feat_vec_list:
				fv[feat] = float(a)/float(b)
		w_vector.data_dict.clear()
		w_vector.data_dict.iadd(fv)
		sc.stop()

	def avg_perc_train(self,textString,parser,fv,fgen):
		dp = data_pool.DataPool(textString=textString[1],fgen=fgen)
		w_vector = WeightVector()
		for key in fv.keys():
			w_vector.data_dict[key]=fv[key]
		#print data_pool.get_sent_num
		while dp.has_next_data():
			sentence = dp.get_next_data()
			gold_global_vector = sentence.gold_global_vector
			current_edge_set = parser.parse(sentence, w_vector.get_vector_score)
			sentence.set_current_global_vector(current_edge_set)
			current_global_vector = sentence.current_global_vector
			#current_global_vector = f_argmax(data_instance)
			w_vector.data_dict.iadd(gold_global_vector.feature_dict)
			w_vector.data_dict.iaddc(current_global_vector.feature_dict, -1)

		vector_list = {}
		num = 0
		for key in w_vector.data_dict.keys():
			vector_list[str(key)] = w_vector.data_dict[key]
	
		return vector_list.items()

		



	


