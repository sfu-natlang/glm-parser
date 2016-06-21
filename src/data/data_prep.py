# -*- coding: utf-8 -*-

#
# Global Linear Model Parser
# Simon Fraser University
# NLP Lab
#
# Author: Vivian Kou, Sean La, Jetic Gu
# (Please add on your name if you have authored this file)
#
# Origin: src/learn/partition.py
#

#
# The DataPrep class aims to partition the data and also
# to upload the data to hdfs when running the glm_parser
# on spark yarn cluster mode.
#
import logging
import sys, os
import re
import os.path
import hashlib
import ConfigParser
from ConfigParser import SafeConfigParser

class DataPrep():
    def __init__(self, dataPath=None, dataRegex=None, shardNum=None, targetPath=None, configFile=None, debug=False):
        self.dataPath=""
        self.dataRegex=""
        self.shardNum=0
        self.targetPath=""
        self.debug=debug
        if self.debug: print "DATAPREP [DEBUG]: Preparing data for hdfs"

        # Load config file
        if configFile:
            self.loadFromConfig(configFile)

        # Load params
        if dataPath:
            if not os.path.isdir(dataPath):
                raise ValueError("DATAPREP [ERROR]: source directory do not exist")
            self.dataPath = dataPath
        if shardNum:
            if (not isinstance(shardNum, int)) and int(shardNum)<=0 :
                raise ValueError("DATAPREP [ERROR]: shard number needs to be a positive integer")
            self.shardNum = shardNum
        if dataRegex:
		    self.dataRegex = dataRegex
        if targetPath:
		    self.targetPath = targetPath

        # Check param validity
        if self.dataPath=="":
            raise ValueError("DATAPREP [ERROR]: dataPath not specified")
        if self.dataRegex=="":
            raise ValueError("DATAPREP [ERROR]: dataRegex not specified")
        if self.shardNum==0:
            raise ValueError("DATAPREP [ERROR]: shardNumber not specified")
        if self.targetPath=="":
            raise ValueError("DATAPREP [ERROR]: targetPath not specified")

        print "DATAPREP [INFO]: Using data from path:" + self.dataPath

        return

    def loadFromConfig(self, configFile):
        if not os.path.exists(configFile):
            raise ValueError("DATAPREP [ERROR]: config file does not exist")
        if os.path.isdir(configFile):
            raise ValueError("DATAPREP [ERROR]: config file leads to directory instead of file")

        print("DARAPREP [INFO]: Reading configurations from file: %s" % (configFile))
        cf = SafeConfigParser(os.environ)
        cf.read(configFile)

        self.dataRegex    =    cf.get("data",   "train")
        self.dataPath     =    cf.get("data",   "data_path")
        self.targetPath   =    cf.get("data",   "prep_path")
        self.shardNum     = cf.getint("option", "shards")
        return

    def sentCount(self, dataPath, dataRegex):
        '''
        :dataPath: the dir storing the training data
        :format: the format of the training data
        :return: the totalnumber of sentences
        '''
        count = 0
        sectionPattern = re.compile(dataRegex)

        for dirName, subdirList, fileList in os.walk(dataPath):
            for fileName in fileList:
                if sectionPattern.match(str(fileName)) != None:
                    filePath = "%s/%s" % ( str(dirName), str(fileName) )
                    with open(filePath,"r") as theFile:
                        for line in theFile:
                            if line == '\n':
                                count += 1
        return count

    def dataPartition(self, dataPath=None, dataRegex=None, shardNum=None, targetPath=None):
        '''
        :param dataPath: the input directory storing training data_pool
        :param shardNum: the number of partisions of data_pool
        :param targetPath: the output directory storing the sharded data_pool
        '''
        # Process params
        if dataPath   == None: dataPath   = self.dataPath
        if dataRegex  == None: dataRegex  = self.dataRegex
        if shardNum   == None: shardNum   = self.shardNum
        if targetPath == None: targetPath = "data/prep/"


        if self.debug: print "DATAPREP [DEBUG]: Partitioning Data locally"
        if not os.path.exists(targetPath):
            os.makedirs(targetPath)

        sectionPattern = re.compile(dataRegex)
        aFileList = []

        for dirName, subdirList, fileList in os.walk(dataPath):
            for fileName in fileList:
                if sectionPattern.match(str(fileName)) != None:
                    filePath = "%s/%s" % ( str(dirName), str(fileName) )
                    if self.debug: print "DATAPREP [DEBUG]: Pendng file " + filePath
                    aFileList.append(filePath)

        input_string = ''.join(aFileList) + str(shardNum)
        folder = hashlib.md5(input_string).hexdigest()[:7]
        output_path = targetPath + folder + '/'

        if not os.path.exists(output_path):
            os.makedirs(output_path)

            fid = shardNum-1

            output_file = output_path + str(fid)
            fout = open(output_file,"w")

            count = 0

            n = self.sentCount(dataPath,dataRegex)/shardNum # number of sentences per shard

            for filePath in aFileList:
                if self.debug: print "DATAPREP [DEBUG]: Opening file "+ filePath
                fin = open(filePath, "r")

                for line in fin:
                    if count == n and fid is not 0:
                        fid -= 1
                        fout.close()
                        output_file = output_path + str(fid)
                        fout = open(output_file,"w")
                        count = 0

                    fout.write(line)

                    if line == '\n':
                        count += 1

            fout.close()
            if self.debug: print "DATAPREP [DEBUG]: Partition complete"
        return output_path

    def dataUpload(self, sourcePath, targetPath=None):
        '''
        This function uploads the folder sourcePath to targetPath on hadoop.
        '''
        if targetPath == None: targetPath = self.targetPath

        if self.debug: print "DATAPREP [DEBUG]: Uploading data to HDFS"
        if self.debug: print "DATAPREP [DEBUG]: Creating target directory " + targetPath
        os.system("hdfs dfs -mkdir -p " + targetPath)
        os.system("hdfs dfs -put -f %s %s"%(sourcePath,targetPath))
        if self.debug: print "DATAPREP [DEBUG]: Upload complete"
        return

# Uncomment the following code for tests

if __name__ == "__main__":
    #dataPath   = sys.argv[1]
    #dataRegex  = sys.argv[2]
    #shardNum   = int(sys.argv[3])
    dataPrep = DataPrep(targetPath="data/meow/", shardNum=8, configFile=sys.argv[1])
    sourcePath = dataPrep.dataPartition()
    dataPrep.dataUpload(sourcePath)
