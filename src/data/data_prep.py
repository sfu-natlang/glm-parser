import logging
import sys
import re
import os
import os.path
import hashlib
import ConfigParser
from ConfigParser import SafeConfigParser

class DataPrep():
    def __init__(self, dataPath="", dataRegex="", shardNum=0, targetPath="", configFile=""):
        print "DATAPREP [DEBUG]: Preparing data for hdfs"
        if not os.path.isdir(dataPath):
            raise ValueError("DATAPREP [ERROR]: source directory do not exist")
        if (not isinstance(shardNum, int)) and int(shardNum)<=0 :
            raise ValueError("DATAPREP [ERROR]: shard number needs to be a positive integer")
        self.dataPath = dataPath
        self.dataRegex = dataRegex
        self.shardNum = shardNum
        self.targetPath = targetPath

        if configFile!="":
            loadFromConfig(configFile)
        print "DATAPREP [INFO]: Using data from path:" + self.dataPath

        sourcePath = dataPrep(self.dataPath, self.dataRegex, self.shardNum, self.targetPath)
        self.dataUpload(sourcePath, self.targetPath)

    def loadFromConfig(self, configFile):
        if not os.path.exists(configFile):
            raise ValueError("DATAPREP [ERROR]: config file does not exist")
        if os.path.isdir(configFile):
            raise ValueError("DATAPREP [ERROR]: config file leads to directory instead of file")

        print("DARAPREP [INFO]: Reading configurations from file: %s" % (configFile))
        cf = SafeConfigParser(os.environ)
        cf.read(configFile)

        if self.dataRegex != "":
            self.dataRegex    =    cf.get("data",   "train")
        if self.dataPath != "":
            self.dataPath     =    cf.get("data",   "data_path")
        if self.targetPath != "":
            self.targetPath   =    cf.get("data",   "prep_path")
        if self.shardNum != "":
            self.shardNum     = cf.getint("option", "shards")

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

    def dataPrep(self, dataPath, dataRegex, shardNum, targetPath="../data/prep/"):
        '''
        :param dataPath: the input directory storing training data_pool
        :param shardNum: the number of partisions of data_pool
        :param targetPath: the output directory storing the sharded data_pool
        '''
        print "DATAPREP [DEBUG]: Partitioning Data locally"
        if not os.path.exists(targetPath):
            os.makedirs(targetPath)

        sectionPattern = re.compile(dataRegex)
        fileList = []

        for dirName, subdirList, fileList in os.walk(dataPath):
            for fileName in fileList:
                if sectionPattern.match(str(fileName)) != None:
                    filePath = "%s/%s" % ( str(dirName), str(fileName) )
                    fileList.append(filePath)

        input_string = ''.join(fileList) + str(shardNum)
        folder = hashlib.md5(input_string).hexdigest()[:7]
        output_path = targetPath + folder + '/'

        if not os.path.exists(output_path):
            os.makedirs(output_path)

            fid = shardNum-1

            output_file = output_path + str(fid)
            fout = open(output_file,"w")

            count = 0

            n = sentCount(dataPath,dataRegex)/shardNum # number of sentences per shard

            for filePath in fileList:
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
            print "DATAPREP [DEBUG]: Partition complete"
        return output_path

    def dataUpload(self, sourcePath, targetPath="./data/prep/"):
        print "DATAPREP [DEBUG]: Uploading data to HDFS"
        print "DATAPREP [DEBUG]: Creating target directory" + targetPath
        os.system("hdfs dfs -mkdir -p" + targetPath)
        os.system("hdfs dfs -put %s %s"%(sourcePath,targetPath)
        print "DATAPREP [DEBUG]: Upload complete"



if __name__ == "__main__":
    dataPath   = sys.argv[1]
    dataRegex  = sys.argv[2]
    shardNum   = int(sys.argv[3])
    targetPath = "../data/prep/"
    configFile = sys.argv[4]
    data = DataPrep(dataPath, dataRegex, shardNum, targetPath, configFile)
