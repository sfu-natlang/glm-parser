# -*- coding: utf-8 -*-
from __future__ import division
import os
import re
import importlib
import logging
from copy import deepcopy
from sentence import Sentence
from data_prep import DataPrep
from file_io import fileRead, fileWrite

__version__ = '1.1'
logger = logging.getLogger('DATAPOOL')


class DataPool():
    """
    Data object that holds all sentences (dependency trees) and provides
    interface for loading data from the disk and retrieving them using an
    index.

    Data are classified into sections when stored in the disk, but we
    do not preserve such structural information, and all sentences
    will be loaded and "flattened" to be held in a single list.

    The instance maintains a current_index variable, which is used to
    locate the last sentence object we have read. Calling get_next()
    method will increase this by 1, and calling has_next() will test
    this index against the total number. The value of the index is
    persistent during get_next() and has_next() calls, and will only
    be reset to initial value -1 when reset() is called (manually or
    during init).
    """
    def __init__(self,
                 fgen,
                 data_format,
                 data_regex   = None,
                 data_path    = None,
                 textString   = None,
                 prep_path    = 'data/prep/',
                 shards       = 1,
                 sparkContext = None,
                 hadoop       = False):

        """
        Initialize the Data set

        :param data_regex: the sections to be used.
        A regular expression that indicates which sections to be used e.g.
        (0[0-9])|(1[0-9])|(2[0-1])/.*tab
        :type data_regex: str

        :param data_path: the relative or absolute path to the 'penn-wsj-deps' folder
        (including "penn-wsj-deps")
        :type data_path: str

        :param format_path: the file that describes the file format for the type of data
        :type format_path: str
        """
        if isinstance(fgen, basestring):
            self.fgen = importlib.import_module('feature.' + fgen).FeatureGenerator
        else:
            self.fgen = fgen

        if isinstance(data_format, basestring):
            self.data_format = importlib.import_module('data.data_format.' + data_format).DataFormat(self.fgen)
        else:
            self.data_format = data_format

        self.hadoop   = hadoop
        self.reset_all()

        if textString is not None:
            self.load_stringtext(textString)

        if data_regex is not None:
            self.load(data_path    = data_path,
                      data_regex   = data_regex,
                      shards       = shards,
                      prep_path    = prep_path,
                      sparkContext = sparkContext)
        return

    def load(self,
             data_path,
             data_regex,
             shards,
             prep_path,
             sparkContext):
        """
        For each section in the initializer, iterate through all files
        under that section directory, and load the content of each
        individual file into the class instance.

        This method should be called after section regex has been initalized
        and before any get_data method is called.
        """
        logger.info("Loading data...")
        self.dataPrep = DataPrep(dataURI      = data_path,
                                 dataRegex    = data_regex,
                                 shardNum     = shards,
                                 targetPath   = prep_path,
                                 sparkContext = sparkContext)

        # Load data
        if self.hadoop is True:
            self.dataPrep.loadHadoop()
        else:
            self.dataPrep.loadLocal()

        # Add data to data_list
        # If using yarn mode, local data will not be loaded
        if self.hadoop is False:
            for dirName, subdirList, fileList in os.walk(self.dataPrep.localPath()):
                for file_name in fileList:
                    file_path = "%s/%s" % (str(dirName), str(file_name))
                    self.data_list += self.data_format.get_data_from_file(file_path)
        else:
            aRdd = sparkContext.textFile(self.dataPrep.hadoopPath()).cache()
            tmp  = aRdd.collect()
            tmpStr = ''.join(str(e) + "\n" for e in tmp)
            self.load_stringtext(textString = tmpStr)

        logger.info("Data loaded")
        return

    def load_stringtext(self, textString):
        self.data_list += self.data_format.load_stringtext(textString)
        return

    def loadedPath(self):
        if self.dataPrep:
            if self.hadoop is True:
                return self.dataPrep.hadoopPath()
            else:
                return self.dataPrep.localPath()
        else:
            raise RuntimeError("DATAPOOL [ERROR]: Data has not been loaded by DataPrep, cannot retrieve data path.")
        return

    def __add__(self, another_data_pool):
        if another_data_pool is None:
            return deepcopy(self)
        # if self.fgen != another_data_pool.fgen:
        #     raise RuntimeError("DATAPOOL [ERROR]: Merging dataPools do not have the same fgen")
        # if self.data_format != another_data_pool.data_format:
        #     raise RuntimeError("DATAPOOL [ERROR]: Merging dataPools do not have the same format")
        newDataPool = deepcopy(self)
        newDataPool.data_list = newDataPool.data_list + another_data_pool.data_list
        newDataPool.reset_index()
        return newDataPool

    def export(self, fileURI, sparkContext=None):
        self.data_format.export_to_file(self, fileURI, sparkContext)
        return

    def reset_all(self):
        """
        Reset the index variables and the data list.

        Restores the instance to a state when no sentence has been read
        """
        self.reset_index()
        self.data_list = []

        return

    def reset_index(self):
        """
        Reset the index variable to the very beginning of
        sentence list
        """
        self.current_index = -1

    def has_next_data(self):
        """
        Returns True if there is still sentence not read. This call
        does not advence data pointer. Call to get_next_data() will
        do the job.

        :return: False if we have reaches the end of data_list
                 True otherwise
        """
        i = self.current_index + 1
        if i >= 0 and i < len(self.data_list):
            return True
        else:
            return False

    def get_next_data(self):
        """
        Return the next sentence object, which is previously read
        from disk files.

        This method does not perform index checking, so please make sure
        the internal index is valid by calling has_next_data(), or an exception
        will be raise (which would be definitely not what you want)
        """
        if(self.has_next_data()):
            self.current_index += 1
            # Logging how many entries we have supplied
            if self.current_index % 1000 == 0:
                logger.debug("Data finishing %.2f%% ..." %
                             (100 * self.current_index / len(self.data_list), ))

            return self.data_list[self.current_index]
        raise IndexError("Run out of data while calling get_next_data()")

    def get_sent_num(self):
        return len(self.data_list)
