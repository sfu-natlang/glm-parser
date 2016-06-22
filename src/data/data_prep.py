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
    def __init__(self, dataPath, dataRegex, shardNum, targetPath, debug=False):
        self.dataPath  = dataPath
        self.dataRegex = dataRegex
        self.shardNum  = shardNum
        self.targetPath= targetPath + "/" # Avoid error
        self.debug     = debug
        if self.debug: print "DATAPREP [DEBUG]: Preparing data for hdfs"

        # Check param validity
        if not os.path.isdir(dataPath):
            raise ValueError("DATAPREP [ERROR]: source directory do not exist")
        if (not isinstance(shardNum, int)) or int(shardNum)<=0 :
            raise ValueError("DATAPREP [ERROR]: shard number needs to be a positive integer")
        if self.dataRegex=="":
            raise ValueError("DATAPREP [ERROR]: dataRegex not specified")
        if self.targetPath=="":
            raise ValueError("DATAPREP [ERROR]: targetPath not specified")
        print "DATAPREP [INFO]: Using data from path:" + self.dataPath
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

    def loadToPath(self):
        '''
        :param dataPath: the input directory storing training data_pool
        :param shardNum: the number of partisions of data_pool
        :param targetPath: the output directory storing the sharded data_pool
        '''
        # Process params
        dataPath   = self.dataPath
        dataRegex  = self.dataRegex
        shardNum   = self.shardNum
        targetPath = self.targetPath

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

    def dataUpload(self):
        '''
        This function uploads the folder sourcePath to targetPath on hadoop.
        '''
        from pyspark import SparkContext

        sc = SparkContext()

        aFilePattern = re.compile(self.dataRegex)
        aRdd = sc.emptyRDD()
        aFileList = []

        for dirName, subdirList, fileList in os.walk(self.dataPath):
            for fileName in fileList:
                if aFilePattern.match(str(fileName)) != None:
                    filePath = "%s/%s" % ( str(dirName), str(fileName) )
                    if self.debug: print "DATAPREP [DEBUG]: Adding file " + filePath
                    aRdd = aRdd + sc.textFile("file://"+filePath)
                    aFileList.append(filePath)

        aRdd.filter(lambda x: x!='').collect()

        hashCode = hashlib.md5(''.join(aFileList) + str(self.shardNum)).hexdigest()[:7]
        if self.debug: print "DATAPREP [DEBUG]: Uploading data to HDFS"
        if self.debug: print "DATAPREP [DEBUG]: Creating target directory " + self.targetPath + hashCode
        # Save as specific amount of files
        # aRdd.coalesce(self.shardNum,True).saveAsTextFile(self.targetPath + hashCode)
        # Save as default amount of files
        aRdd.saveAsTextFile(self.targetPath + hashCode)
        if self.debug: print "DATAPREP [DEBUG]: Upload complete"
        return

# Uncomment the following code for tests
'''
if __name__ == "__main__":
    configFile = sys.argv[1]
    print("DATAPREP [INFO]: Reading configurations from file: %s" % (configFile))
    cf = SafeConfigParser(os.environ)
    cf.read(configFile)

    dataRegex    =    cf.get("data",   "train")
    dataPath     =    cf.get("data",   "data_path")
    targetPath   =    cf.get("data",   "prep_path")
    shardNum     = cf.getint("option", "shards")
    dataPrep = DataPrep(dataPath, dataRegex, shardNum, targetPath)
    #dataPrep.loadToPath()
    dataPrep.dataUpload()
    print("DATAPREP [INFO]: Test Complete")
'''
