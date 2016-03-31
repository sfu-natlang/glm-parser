class Learner():

	def __init__(self, fgen, parser):
		self.fgen = fgen
		self.parser = parser()
		return

	def count_sent(self, input_dir, format):
		#counter for counting the number of sentences
		count = 0
		if format is "sec":
			for s in listdir(input_dir):
				input_sec = join(input_dir,s)
				if isdir(input_sec):
					for f in listdir(input_sec):
						file_path = join(input_sec,f)
						if isfile(file_path):
							#print file_path
							with open(file_path,"r") as in_file:
								for line in in_file:
									if line == '\n':
										count += 1
		else:
			for f in listdir(input_dir):
				file_path = join(input_dir,f)
				if isfile(file_path):
					with open(file_path,"r") as in_file:
						for line in in_file:
							if line == '\n':
								count += 1
		return count

	def spark_train(self, output_dir, max_iter):
		sc = SparkContext(appName="sampleApp",master="local[4]")
		train_files= sc.wholeTextFiles(output_dir)
		fv = {}
		for round in range(max_iter):
			weight_vector = sc.broadcast(fv)

			feat_vec_list = train_files.map(lambda t: self.avg_perc_train(t,self.parser,fv,self.fgen))
			feat_vec_list = feat_vec_list.reduceByKey(add)
			print feat_vec_list.collect()
		sc.stop()

	'''
		feat_vec_list = train_files.map(lambda t: self.avg_perc_train(t,self.parser,fv,self.fgen))
		
		feat_vec_list = feat_vec_list.combineByKey(lambda value: (value, 1),
                             lambda x, value: (x[0] + value, x[1] + 1),
                             lambda x, y: (x[0] + y[0], x[1] + y[1])).collect()
		
		for (feat, (a,b)) in feat_vec_list:
		        fv[feat] = float(a)/float(b)
		w_vector.data_dict.clear()
		w_vector.data_dict.iadd(fv)
	'''
		def avg_perc_train(self,textString,parser,fv,fgen):
			dp = data_pool.DataPool(textString=textString[1],fgen=fgen)
			w_vector = weight_vector.WeightVector()
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
			vector_list = []
			vector_list.append({'a':1})
			for key in w_vector.data_dict.keys():
				#vector_list.append((str(key),w_vector.data_dict[key]))
				vector_list.append({'a':1})
			return vector_list

'''
	def partition_data(self, input_dir, sent_num, output_dir):

		n = sent_num/N
		count = 0
		fid = N-1
		output_file = output_dir+"training_data_%d"%fid
		fout = open(output_file,"w")
		file_close = True
		for s in listdir(input_dir):
			input_sec = join(input_dir,s)
			if isdir(input_sec):
				for f in listdir(input_sec):
					file_path = join(input_sec,f)
					if isfile(file_path):
						with open(file_path,"r") as in_file:
							for line in in_file:
								if count == n:
									fid -=1
									fout.close
									output_file = output_dir+"training_data_%d"%fid
									fout = open(output_file,"w")
									count = 0
								fout.write(line)
								if line == '\n':
									count += 1
		fout.close
'''