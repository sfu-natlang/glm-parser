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
    def __init__(self, dataPath, dataRegex, shardNum, targetPath, sparkContext=None, debug=True):
        self.dataPath  = dataPath
        self.dataRegex = dataRegex
        self.shardNum  = shardNum
        # Avoid error. We do not know whether the user has got a / at the end of the string or not,
        # which could be problematic in the future
        self.targetPath= targetPath + "/" if targetPath[len(targetPath)-1] != "/" else targetPath
        self.debug     = debug
        self.sc = sparkContext
        if self.debug: print "DATAPREP [DEBUG]: Preparing data for " + dataRegex

        # Check param validity
        if not os.path.isdir(dataPath):
            raise ValueError("DATAPREP [ERROR]: source directory do not exist")
        if (not isinstance(shardNum, int)) or int(shardNum)<=0 :
            raise ValueError("DATAPREP [ERROR]: shard number needs to be a positive integer")
        if dataRegex=="":
            raise ValueError("DATAPREP [ERROR]: dataRegex not specified")
        if targetPath=="":
            raise ValueError("DATAPREP [ERROR]: targetPath not specified")
        if self.debug: print "DATAPREP [DEBUG]: Using data from path:" + self.dataPath
        return

    def localPath(self):
        '''
        Return the path of the present data.
        '''
        if self.path: return self.path
        print ("DATAPREP [WARN]: data not locally loaded yet, will not be loaded this time.")
        aFileList = []

        for dirName, subdirList, fileList in os.walk(self.dataPath):
            for fileName in fileList:
                if aFilePattern.match(str(fileName)) != None:
                    filePath = "%s/%s" % ( str(dirName), str(fileName) )
                    aFileList.append(filePath)
        hashCode = hashlib.md5(''.join(aFileList) + str(self.shardNum)).hexdigest()[:7]
        # Adding a / at the end of the string to prevent confusion. It is in fact a directory,
        # not a file.
        self.path = self.targetPath + hashCode + '/'
        return self.path

    def hadoopPath(self):
        '''
        Return the path of the present data.
        '''
        if self.hdfsPath: return self.hdfsPath
        raise RuntimeError("DATAPREP [ERROR]: data not uploaded to HDFS yet")
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

    def loadLocal(self):
        '''
        :param dataPath: the input directory storing training data_pool
        :param shardNum: the number of partisions of data_pool
        :param targetPath: the output directory storing the sharded data_pool
        '''
        # Process params
        if self.debug: print "DATAPREP [DEBUG]: Partitioning Data locally"
        if not os.path.exists(self.targetPath):
            os.makedirs(self.targetPath)

        sectionPattern = re.compile(self.dataRegex)
        aFileList = []

        for dirName, subdirList, fileList in os.walk(self.dataPath):
            for fileName in fileList:
                if sectionPattern.match(str(fileName)) != None:
                    filePath = "%s/%s" % ( str(dirName), str(fileName) )
                    #if self.debug: print "DATAPREP [DEBUG]: Pendng file " + filePath
                    aFileList.append(filePath)

        input_string = ''.join(aFileList) + str(self.shardNum)
        hashCode = hashlib.md5(input_string).hexdigest()[:7]

        self.path = self.targetPath + hashCode + '/'

        if not os.path.exists(self.path):
            if self.debug: print "DATAPREP [DEBUG]: Copying data to local directory: " + self.path
            os.makedirs(self.path)

            fid = self.shardNum-1

            output_file = self.path + str(fid)
            fout = open(output_file,"w")

            count = 0

            n = self.sentCount(self.dataPath, self.dataRegex)/self.shardNum # number of sentences per shard

            for filePath in aFileList:
                #if self.debug: print "DATAPREP [DEBUG]: Opening file "+ filePath
                fin = open(filePath, "r")

                for line in fin:
                    if count == n and fid is not 0:
                        fid -= 1
                        fout.close()
                        output_file = self.path + str(fid)
                        fout = open(output_file,"w")
                        count = 0

                    fout.write(line)

                    if line == '\n':
                        count += 1

            fout.close()
        else:
            if self.debug: print "DATAPREP [DEBUG]: local directory: " + self.path + " already exists, will not proceed to copy"
        if self.debug: print "DATAPREP [DEBUG]: Partition complete"
        return self.path

    def loadHadoop(self):
        '''
        This function uploads the data to targetPath on hadoop.
        '''
        from pyspark import SparkContext

        if self.sc == None: self.sc = SparkContext()

        aFilePattern = re.compile(self.dataRegex)
        aFileList = []

        for dirName, subdirList, fileList in os.walk(self.dataPath):
            for fileName in fileList:
                if aFilePattern.match(str(fileName)) != None:
                    filePath = "%s/%s" % ( str(dirName), str(fileName) )
                    aFileList.append("file://"+filePath)

        aRdd = self.sc.textFile(','.join(aFileList)).cache()

        hashCode = hashlib.md5(''.join(aFileList) + str(self.shardNum)).hexdigest()[:7]
        self.hdfsPath = self.targetPath + str(self.sc._jsc.sc().applicationId()) + '/' + hashCode + '/'
        if self.debug: print "DATAPREP [DEBUG]: Uploading data to HDFS"
        if self.debug: print "DATAPREP [DEBUG]: Creating target directory " + self.hdfsPath
        # Save as specific amount of files
        # aRdd.coalesce(self.shardNum,True).saveAsTextFile(self.path)
        # Save as default amount of files
        aRdd.saveAsTextFile(self.hdfsPath)
        if self.debug: print "DATAPREP [DEBUG]: Upload complete"
        return self.hdfsPath

# Uncomment the following code for tests
'''
if __name__ == "__main__":
    configFile = sys.argv[1]
    print("DATAPREP [DEBUG]: Reading configurations from file: %s" % (configFile))
    cf = SafeConfigParser(os.environ)
    cf.read(configFile)

    dataRegex    =    cf.get("data",   "train")
    dataPath     =    cf.get("data",   "data_path")
    targetPath   =    cf.get("data",   "prep_path")
    shardNum     = cf.getint("option", "shards")
    dataPrep = DataPrep(dataPath, dataRegex, shardNum, targetPath)
    #dataPrep.loadLocal()
    dataPrep.loadHadoop()
    print("DATAPREP [DEBUG]: Test Complete")
'''
