# -*- coding: utf-8 -*-
from __future__ import division
import os, re
from sentence import Sentence
import logging
import re

logging.basicConfig(filename='glm_parser.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

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
    def __init__(self, section_regex='', data_path="./penn-wsj-deps/",
                 fgen=None, config_path=None, textString=None, config_list=None):
        """
        Initialize the Data set

        :param section_regex: the sections to be used. 
        A regular expression that indicates which sections to be used e.g.
        (0[0-9])|(1[0-9])|(2[0-1])/.*tab
        :type section_regex: str 

        :param data_path: the relative or absolute path to the 'penn-wsj-deps' folder
        (including "penn-wsj-deps")
        :type data_path: str

        :param config_path: the config file that describes the file format for the type of data
        :type config_path: str        
        """  
        self.fgen = fgen
        self.reset_all()
        if textString is None:
            self.data_path = data_path
            self.section_regex = section_regex
            self.config_path = config_path
            self.load()
        else:
            self.load_stringtext(textString,config_list)


        return

    def load_stringtext(self,textString,config_list):
        lines = textString.splitlines()
        column_list = {}
        for field in config_list:
            if not(field.isdigit()):
                column_list[field] = []
                
        length = len(config_list) - 2

        for line in lines:
            if line != '':
                entity = line.split()
                for i in range(length):
                    if not(config_list[i].isdigit()):
                        column_list[config_list[i]].append(entity[i])
            else:
                if not(config_list[0].isdigit()) and column_list[config_list[0]] != []:
                    sent = Sentence(column_list, config_list, self.fgen)
                    self.data_list.append(sent)

                column_list = {}

                for field in config_list:
                    if not (field.isdigit()):
                        column_list[field] = []

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
                logging.debug("Data finishing %.2f%% ..." %
                             (100 * self.current_index/len(self.data_list), ))

            return self.data_list[self.current_index]
        raise IndexError("Run out of data while calling get_next_data()")

    def load(self):
        """
        For each section in the initializer, iterate through all files
        under that section directory, and load the content of each
        individual file into the class instance.

        This method should be called after section regex has been initalized
        and before any get_data method is called.
        """
        logging.debug("Loading data...")

        section_pattern = re.compile(self.section_regex)

        rootDir = self.data_path 

        for dirName, subdirList, fileList in os.walk(rootDir):
            logging.debug("Found directory: %s" % str(dirName))
            for file_name in fileList:
                if section_pattern.match(str(file_name)) != None:
                    file_path = "%s/%s" % ( str(dirName), str(file_name) ) 
                    self.data_list += self.get_data_list(file_path)

        return


    def get_data_list(self, file_path):
        """
        Form the DependencyTree list from the specified file.

        :param file_path: the path to the data file
        :type file_path: str

        :return: a list of DependencyTree in the specified file
        :rtype: list(Sentence)
        """

        fconfig = open(self.config_path)
        field_name_list = []
    
        for line in fconfig:
            field_name_list.append(line.strip())

        fconfig.close() 

        f = open(file_path)
        data_list = []

        column_list = {}

        for field in field_name_list:
            if not(field.isdigit()):
                column_list[field] = []

        length = len(field_name_list) - 2

        for line in f:
            line = line[:-1]
            if line != '':
                entity = line.split()
                for i in range(length):
                    if not(field_name_list[i].isdigit()):
                        column_list[field_name_list[i]].append(entity[i])
            
            else:
                # Prevent any non-mature (i.e. trivial) sentence structure
                if not(field_name_list[0].isdigit()) and column_list[field_name_list[0]] != []:
            
                    # Add "ROOT" for word and pos here
                    sent = Sentence(column_list, field_name_list, self.fgen)
                    data_list.append(sent)

                column_list = {}

                for field in field_name_list:
                    if not (field.isdigit()):
                        column_list[field] = []

        f.close()

        return data_list
    
    def get_sent_num(self):
        return len(self.data_list)

