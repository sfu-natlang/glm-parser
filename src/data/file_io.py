import sys
import re
import os.path

__version__ = '1.0.0'


def __fileReadHDFS(fileURI, sparkContext=None):
    if fileURI is None:
        raise ValueError("FILEIO [ERROR]: Reading file not specified")

    # Initialising
    if sparkContext is None:
        raise RuntimeError('FILEIO [ERROR]: SparkContext not initialised')
    sc = sparkContext

    aRdd = sc.textFile(fileURI).cache()
    aRdd = aRdd.map(str).cache()
    fileContent = aRdd.collect()

    return fileContent


def __fileWriteHDFS(fileURI, contents, sparkContext=None):
    '''
    Acceptable contents:
        list(array) of data
    '''
    if fileURI is None:
        raise ValueError("FILEIO [ERROR]: Saving file not specified")
    if not isinstance(contents, list):
        raise ValueError("FILEIO [ERROR]: Contents to be saved should be a list(an array)")
    # Initialising
    if sparkContext is None:
        raise RuntimeError('FILEIO [ERROR]: SparkContext not initialised')
    sc = sparkContext

    try:
        aRdd = sc.parallelize(contents, 1).cache()
        aRdd.coalesce(1, True).cache()
        aRdd.saveAsTextFile(fileURI)
    except:
        raise RuntimeError('FILEIO [ERROR]: Unable to save file to HDFS: ' + fileURI)

    return fileURI + "/part-00000"


def fileRead(fileURI, sparkContext=None):
    if fileURI is None:
        raise ValueError("FILEIO [ERROR]: File not specified")
    if (fileURI.startswith("file://")):
        try:
            contents = []
            f = open(fileURI[7:])
            for line in f:
                contents.append(line.rstrip('\n'))
            return contents
        except:
            raise RuntimeError('FILEIO [ERROR]: Unable to read from local directory: ' + fileURI)
    return __fileReadHDFS(fileURI=fileURI, sparkContext=sparkContext)


def fileWrite(fileURI, contents, sparkContext=None):
    '''
    Acceptable contents:
        list(array) of data
    '''
    if fileURI is None:
        raise ValueError("FILEIO [ERROR]: saving path not specified")
    if not isinstance(contents, list):
        raise ValueError("FILEIO [ERROR]: Contents to be saved should be a list(an array)")
    if (fileURI.startswith("file://")):
        try:
            f = open(fileURI[7:], "w")
            for line in contents:
                f.write(line + "\n")
            return fileURI
        except:
            raise RuntimeError('FILEIO [ERROR]: Unable to save to local directory: ' + fileURI)
    return __fileWriteHDFS(fileURI=fileURI, contents=contents, sparkContext=sparkContext)
