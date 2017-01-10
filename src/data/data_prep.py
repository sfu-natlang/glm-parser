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
import sys
import os
import re
import os.path
import hashlib
import logging

__version__ = '1.0.0'
logger = logging.getLogger('DATAPREP')


class DataPrep():
    def __init__(self,
                 dataURI,
                 dataRegex,
                 shardNum,
                 targetPath,
                 sparkContext=None):

        self.dataURI    = dataURI + "/" if dataURI[len(dataURI) - 1] != "/" else dataURI
        self.dataRegex  = dataRegex
        self.shardNum   = shardNum
        # Avoid error. We do not know whether the user has got a / at the end of the string or not,
        # which could be problematic in the future
        self.targetPath = targetPath + "/" if targetPath[len(targetPath) - 1] != "/" else targetPath
        self.sc         = sparkContext

        logger.debug("Preparing data for " + dataRegex)

        # Check param validity
        if (not isinstance(shardNum, int)) or int(shardNum) <= 0:
            raise ValueError("DATAPREP [ERROR]: shard number needs to be a positive integer")
        if dataRegex == "":
            raise ValueError("DATAPREP [ERROR]: dataRegex not specified")
        if targetPath == "":
            raise ValueError("DATAPREP [ERROR]: targetPath not specified")
        logger.debug("Using data from path: " + self.dataURI)
        return

    def localPath(self):
        '''
        Return the local path of the present data.
        '''
        if self.path:
            return self.path
        logger.warn("data not locally loaded yet, will not be loaded this time.")
        aFileList = []

        for dirName, subdirList, fileList in os.walk(self.dataURI[7:]):
            for fileName in fileList:
                if aFilePattern.match(str(fileName)) is not None:
                    filePath = "%s/%s" % (str(dirName), str(fileName))
                    aFileList.append(filePath)
        hashCode = hashlib.md5(''.join(aFileList) + str(self.shardNum)).hexdigest()[:7]
        # Adding a / at the end of the string to prevent confusion. It is in fact a directory,
        # not a file.
        self.path = self.targetPath + hashCode + '/'
        return self.path

    def hadoopPath(self):
        '''
        Return the path on HDFS of the present data.
        '''
        if self.hdfsPath:
            return self.hdfsPath
        raise RuntimeError("DATAPREP [ERROR]: data not uploaded to HDFS yet")
        return

    def loadLocal(self):
        '''
        Load the data and create tmp files in local directory
        '''
        def sentCount(dataURI, dataRegex):
            '''
            :dataURI: the dir storing the training data
            :format: the format of the training data
            :return: the totalnumber of sentences
            '''
            count = 0
            sectionPattern = re.compile(dataRegex)

            for dirName, subdirList, fileList in os.walk(dataURI):
                for fileName in fileList:
                    if sectionPattern.match(str(fileName)) is not None:
                        filePath = "%s/%s" % (str(dirName), str(fileName))
                        with open(filePath, "r") as theFile:
                            for line in theFile:
                                if line == '\n':
                                    count += 1
            return count

        # Process params
        if (not self.dataURI.startswith("file://")):
            raise ValueError("DATAPREP [ERROR]: Shouldn't use none local path for loading data locally: " + self.dataURI)
        if not os.path.isdir(self.dataURI[7:]):
            raise ValueError("DATAPREP [ERROR]: source directory do not exist")
        logger.debug("Partitioning Data locally")
        if not os.path.exists(self.targetPath):
            os.makedirs(self.targetPath)

        sectionPattern = re.compile(self.dataRegex)
        aFileList = []

        for dirName, subdirList, fileList in os.walk(self.dataURI[7:]):
            for fileName in fileList:
                if sectionPattern.match(str(fileName)) is not None:
                    filePath = "%s/%s" % (str(dirName), str(fileName))
                    aFileList.append(filePath)

        input_string = ''.join(aFileList) + str(self.shardNum)
        hashCode = hashlib.md5(input_string).hexdigest()[:7]

        self.path = self.targetPath + hashCode + '/'

        if not os.path.exists(self.path):
            logger.debug("Copying data to local directory: " + self.path)
            os.makedirs(self.path)

            fid = self.shardNum - 1

            output_file = self.path + str(fid)
            fout = open(output_file, "w")

            count = 0

            n = sentCount(self.dataURI[7:], self.dataRegex) / self.shardNum  # number of sentences per shard

            for filePath in aFileList:
                fin = open(filePath, "r")

                for line in fin:
                    if count == n and fid is not 0:
                        fid -= 1
                        fout.close()
                        output_file = self.path + str(fid)
                        fout = open(output_file, "w")
                        count = 0

                    fout.write(line)

                    if line == '\n':
                        count += 1

            fout.close()
        else:
            logger.debug("local directory: " + self.path + " already exists, will not proceed to copy")
        logger.debug("Partition complete")
        return self.path

    def loadHadoop(self):
        '''
        This function uploads the data to targetPath on hadoop.
        '''
        if self.sc is None:
            raise RuntimeError('DATAPREP [ERROR]: SparkContext not initialised')
        dataList = re.split("\||,|\s+", self.dataRegex)
        for i in range(len(dataList)):
            dataList[i] = self.dataURI + "*/" + dataList[i]
        logger.debug("Using regular expression for files: " + str(dataList))
        aRdd = self.sc.textFile(','.join(dataList)).cache()

        hashCode = hashlib.md5(self.dataURI + self.dataRegex + str(self.shardNum)).hexdigest()[:7]
        self.hdfsPath = self.targetPath + str(self.sc._jsc.sc().applicationId()) + '/' + hashCode + '/'
        logger.debug("Uploading data to HDFS")
        logger.debug("Uploading to target directory " + self.hdfsPath)

        aRdd.coalesce(self.shardNum, True).cache()
        aRdd.saveAsTextFile(self.hdfsPath)
        aRdd.unpersist()
        aRdd = None
        logger.debug("Upload complete")
        return self.hdfsPath

# Uncomment the following code for tests
'''
if __name__ == "__main__":
    import ConfigParser
    from ConfigParser import SafeConfigParser
    configFile = sys.argv[1]
    print("Reading configurations from file: %s" % (configFile))
    cf = SafeConfigParser(os.environ)
    cf.read(configFile)

    dataRegex    =    cf.get("data",   "train")
    dataURI     =    cf.get("data",   "data_path")
    targetPath   =    cf.get("data",   "prep_path")
    shardNum     = cf.getint("option", "shards")
    dataPrep = DataPrep(dataURI, dataRegex, shardNum, targetPath)
    #dataPrep.loadLocal()
    dataPrep.loadHadoop()
    print("Test Complete")
'''
