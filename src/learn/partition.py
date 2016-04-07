import logging

import re
import os.path
import hashlib

def count_sent(input_dir, regex):
    '''
    :input_dir: the dir storing the training data
    :format: the format of the training data
    :return: the totalnumber of sentences
    '''
    count = 0
    section_pattern = re.compile(regex)
    rootDir = input_dir

    for dirName, subdirList, fileList in os.walk(rootDir):
        for file_name in fileList:
            if section_pattern.match(str(file_name)) != None:
                file_path = "%s/%s" % ( str(dirName), str(file_name) ) 
                with open(file_path,"r") as in_file:
                    for line in in_file:
                        if line == '\n':
                            count += 1
    return count

def partition_data(input_dir, regex, shard_num, output_dir="data/prep/"):
    '''
    :param input_dir: the input directory storing training data_pool
    :param shard_num: the number of partisions of data_pool
    :param output_dir: the output directory storing the sharded data_pool
    '''
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    section_pattern = re.compile(regex)
    file_list = []

    for dirName, subdirList, fileList in os.walk(input_dir):
        for file_name in fileList:
            if section_pattern.match(str(file_name)) != None:
                file_path = "%s/%s" % ( str(dirName), str(file_name) ) 
                file_list.append(file_path)

    input_string = ''.join(file_list) + str(shard_num)
    folder = hashlib.md5(input_string).hexdigest()[:7] 
    output_path = output_dir + folder + '/' 

    if not os.path.exists(output_path):
	os.makedirs(output_path) 

        fid = shard_num-1

        output_file = output_path + str(fid) 
        fout = open(output_file,"w")
        
        count = 0

        sent_num = count_sent(input_dir,regex) # count the total number of sentences
        n = sent_num/shard_num # number of sentences per shard

        for file_path in file_list:
            fin = open(file_path, "r")

            for line in fin:
                if count == n and fid is not 0:
                    fid -= 1
                    fout.close()
                    output_file = output_path + fid 
                    fout = open(output_file,"w")
                    count = 0

                fout.write(line)

                if line == '\n':
                    count += 1

        fout.close()

    return output_path 
