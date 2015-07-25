# -*- coding: utf-8 -*-
from __future__ import division
import os, re
from sentence import Sentence
import logging

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
    def __init__(self, section_set=[], data_path="./penn-wsj-deps/",
                 fgen=None):
        """
        Initialize the Data set
        
        :param section_set: the sections to be used. 
        It can be specifiled by a list of either integer or tuple.
        for tuple (a,b), the section would be from a to b including a and b
        :type section_set: list(int/tuple)
        
        :param data_path: the relative or absolute path to the 'penn-wsj-deps' folder
        (including "penn-wsj-deps")
        :type data_path: str
        
        """  
        self.data_path = data_path
        self.set_section_list(section_set)
        
        self.reset_all()
        self.load(fgen)

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
                logging.debug("Data finishing %.2f%% ..." %
                             (100 * self.current_index/len(self.data_list), ))

            return self.data_list[self.current_index]
        raise IndexError("Run out of data while calling get_next_data()")

    def get_sent_num(self):
        return len(self.data_list)

    def load(self, fgen):
        """
        For each section in the initializer, iterate through all files
        under that section directory, and load the content of each
        individual file into the class instance.

        This method should be called after section list has been initalized
        and before any get_data method is called.
        """
        logging.debug("Loading data...")
        for section in self.section_list:
            logging.debug("Loading section %02d " % section)
            # There is a slash at the end in order to append file name
            data_path_with_section = self.data_path + ("%02d/" % (section, ))
            for file_name in os.listdir(data_path_with_section):
                file_path = data_path_with_section + file_name
                # Append newly read section data to data_list
                self.data_list = self.data_list + self.get_data_list(file_path, fgen)

        return


    def get_data_list(self, file_path, fgen):
        """
        Form the DependencyTree list from the specified file. The file format
        is defined below:

        ----------------------------------------------
        [previous sentence]
        [empty line]
        {word} {pos} {parent index} {edge_property}
        ...
        ...
        [empty line]
        [next sentence]
        ----------------------------------------------

        * Sentences are separated by an empty line
        * Each entry in the sentence has an implicit index

        :param file_path: the path to the data file
        :type file_path: str
        
        :return: a list of DependencyTree in the specified file
        :rtype: list(Sentence)
        """
        f = open(file_path)

        data_list = []
        word_list = []
        pos_list = []
        edge_set = {}
        current_index = 0

        for line in f:
            line = line[:-1]
            if line != '':
                current_index += 1
                entity = line.split()
                if len(entity) != 4:
                    logging.error("Invalid data format - Length not equal to 4")
                else:
                    # We do not add the 'ROOT' for word and pos
                    # They are added in class Sentence
                    word_list.append(entity[0])
                    pos_list.append(entity[1])
                    edge_set[(int(entity[2]), current_index)] = entity[3]
            else:
                # Prevent any non-mature (i.e. trivial) sentence structure
                if word_list != []:
                    # Add "ROOT" for word and pos here
                    sent = Sentence(word_list, pos_list, edge_set, fgen)
                    data_list.append(sent)

                word_list = []
                pos_list = []
                edge_set = {}
                current_index = 0

        # DO NOT FORGET THIS!!!!!!!!!!!!
        f.close()

        return data_list

    
    def set_section_list(self, section_set):
        """
        Initialize self.section_list as a list containing section
        numbers that we are going to use for training

        Argument section_set is a list of tuples or intrgers:

        +------------------------------------------------------+
        |   tuples    representing the range of the section,   |
        |             i.e. (1,3) means range 1,2,3             |
        |------------------------------------------------------|
        |   int       single section number                    |
        +------------------------------------------------------+

        :param section_set: the sections to be used
        :type section_set: list(tuple/int)
        """
        # First get all sections that are specified using integers
        self.section_list = [section for section in section_set if isinstance(section, int)]

        # Then, make all tuple (x, y) a list [x, x + 1, .. , y]
        section_sets = \
            map(lambda section_tuple: range(section_tuple[0], section_tuple[1]+1),
                [st for st in section_set if isinstance(st, tuple)])

        for s_set in section_sets:
            self.section_list = self.section_list + s_set
        
        # We always train using increasing order
        self.section_list.sort()

        return


##############################################################################################################
# Scripts for testing data_pool

if __name__ == "__main__":
    dp = DataPool([2], "../../penn-wsj-deps/")
    i = 0
    while dp.has_next_data():
        data = dp.get_next_data()
        print data.word_list
        print data.pos_list
        print data.edge_set



##############################################################################################################
#    Old DataSet Class --- Not used any more
##############################################################################################################
class DataSet():
    """
    Read the test data files and generate the trees for parser testing
    The class is specifically for penn-wsj-deps data
    """
    def __init__(self,  
                 section_set=None, 
                 data_path=None):
        """
        Initialize the Data set
        
        :param section_set: the sections to be used. 
        It can be specifiled by a list of either integer or tuple.
        for tuple (a,b), the section would be from a to b including a and b
        :type section_set: list(int/tuple)
        
        :param data_path: the relative or absolute path to the 'penn-wsj-deps' folder
        (include "penn-wsj-deps")
        :type data_path: str
        
        """  
        if section_set == None:
            section_set = [(2,21)]
        if data_path == None:
            data_path="./penn-wsj-deps/"
            
        self._data_path = data_path
        self.set_section_list(section_set)        
        self.init_current_tracker()
        
        return            
    
    def reset(self):
        """
        reset the tracking parameter, to start over from the first sentence
        """
        self.init_current_tracker()
        return        
        
    def init_current_tracker(self):
        """
        Initialize the parameter for tracking the current unused data:
        
        """
        # track current unused test data       
        # the data set which contains the current unused data
        # it is a list of DependencyTree
        self._current_data_set = []

        # the current_section is the section
        # in which the newest data in the current data set locates
        self._current_section = -1

        # the left file list is the path of the files in the current section
        # that has not been added to the current data set
        self._left_file_list  = [] 
        return
    
    def set_section_list(self, section_set):
        """
        Set the section list from section set
        the section set is a list contains:
            tuples --   representing the range of the section,
                        i.e. (1,3) means range 1,2,3
            int    --   single section number
        
        :param section_set: the sections to be used
        :type section_set: list(tuple/int) 
        """
        self._section_list = [section for section in section_set if isinstance(section, int)]
        
        section_sets = \
            map(lambda section_tuple: range(section_tuple[0], section_tuple[1]+1),
                [st for st in section_set if isinstance(st, tuple)])
        for s_set in section_sets:
            self._section_list = self._section_list + s_set
        
        self._section_list.sort()        
        return               
    
    def add_file_list(self):
        """
        add all the file path in the next section to the left_file_list

        :return: the result if the addition succeed
        :rtype: True, if there is file path added, otherwise, False
        """
        next_section = self.get_next_section()
        self._current_section = next_section
        if next_section == None or self._data_path == None:
            return False
        else:
            print next_section
            for file in os.listdir(self._data_path + "%02d" % next_section):
                self._left_file_list.append("%02d/" % next_section + file)
        return True
        
    def has_next_data(self):
        """
        :return:    True, if there exists unused data entry
                    False, otherwise
        :rtype: boolean
        """            
        data_set = self._current_data_set
        if data_set == []:
            data_set = self.add_data()
        return data_set != []
        
    def get_next_data(self):
        """
        Return the next unused data entry

        :return: An entry in the data set
        :rtype: DependencyTree
        """
        if self.has_next_data():
            return self._current_data_set.pop(0)
        else:
            return None

    def get_data(self, file_name, index=0):
        """
        Get data entity from specified file name and index
        
        :param file_name: the name of the data file
        :type file_name: str
        
        :param index: the index of the data entity in the file, 0 by default,
                      which is the 1st entity in the file
        :type index: int
        
        :return: the expected data entity
        :rtype: DependencyTree
        """
        sections = re.findall( r'wsj_(\d\d)\d\d\.mrg\.3\.pa\.gs\.tab', file_name)
        if sections == None or len(sections) != 1:
            print "Invalid file name!!"
            return None   
            
        section = sections[0]
        
        file_path = self._data_path + section + '/' + file_name
        data_list = self.get_data_list(file_path)
        
        if index >= len(data_list) or index < -len(data_list):
            print "Invalid index!!"
            return None
        return data_list[index]
    
    def get_data_list(self, file_path):
        """
        Form the DependencyTree list from the specified file
        
        :param file_path: the path to the data file
        :type: str
        
        :return: a list of DependencyTree in the specified file
        :rtype: list(DependencyTree)
        """
        f = open(file_path)
        #print file_path
        data_set = []
        word_list = ['__ROOT__']
        pos_list = ['ROOT']
        edge_set = {}
        current_index = 0

        for line in f:
            line = line[:-1]
            if line != '':
                current_index = current_index + 1
                entry = line.split()
                if len(entry) != 4:
                    print "invalid data!!"
                else:
                    word_list.append(entry[0])
                    pos_list.append(entry[1])
                    edge_set[(int(entry[2]), current_index)] = entry[3]
            else:
                if word_list != []:
                    d_tree = dependency_tree.DependencyTree()
                    d_tree.set_word_list(word_list)
                    d_tree.set_pos_list(pos_list)
                    d_tree.set_edge_list(edge_set)
                    data_set.append(d_tree)
                word_list = ['__ROOT__']
                pos_list = ['ROOT']
                edge_set = {}
                current_index = 0
        return data_set
    
    def add_data(self):
        """
        add data from the next file in the left_file_list
        that has not been added to the data set

        return: if no data has been added:  None 
                otherwise:  the udated dataset
        """      
        if self._left_file_list == []:
            if self.add_file_list() == False:
                return self._current_data_set
            
        file_path = self._data_path + self._left_file_list.pop(0)
        self._current_data_set += self.get_data_list(file_path)
        return self._current_data_set

    def get_next_section(self):
        """
        find the next section in the section_set,
        according to the current section

        :return: the next section
        :rtype: int
        """
        if self._current_section == None:
            return None
            
        left_list = filter(lambda n: n>self._current_section, self._section_list)
        if left_list == []:
            return None
        else:
            return left_list[0]
