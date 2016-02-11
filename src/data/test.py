from sentence import Sentence

def get_data_list(file_path, config_path):
	fconfig = open(config_path)
	field_name_list = []

	for line in fconfig:
		field_name_list.append(line.strip())

	fconfig.close()

	f= open(file_path)

	data_list = []
	
	column_list = {}

	for field in field_name_list:
		column_list[field] = []

	length = len(field_name_list)

	for line in f:
		line = line[:-1]
		if line != '':
			entity = line.split()
			
			for i in range(length):
				column_list[field_name_list[i]].append(entity[i])
		else:
			if column_list[field_name_list[0]] != []:
				sent = Sentence(column_list, field_name_list)
				data_list.append(sent)
	
			column_list = {}

			for field in field_name_list:
				column_list[field] = []
	f.close()

	return data_list

config_path1 = "config/penn2malt.txt"
config_path2 = "config/conllx.txt"

file_path1 = "wsj_0001.mrg.3.pa.gs.tab"
file_path2 = "danish_ddt_train.conll"

data_list1 = get_data_list(file_path1, config_path1)
data_list2 = get_data_list(file_path2, config_path2)

print data_list1[0].return_column_list()
print data_list2[0].return_column_list()

print data_list1[0].return_field_name_list()
print data_list2[0].return_field_name_list()
