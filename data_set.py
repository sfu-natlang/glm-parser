# -*- coding: utf-8 -*-

import os, dependency_tree

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
        
        self._section_list = [section for section in section_set if isinstance(section, int)]
        section_sets = \
            map(lambda section_tuple: range(section_tuple[0], section_tuple[1]+1),
                [st for st in section_set if isinstance(st, tuple)])
        for s_set in section_sets:
            self._section_list = self._section_list + s_set
        self._section_list.sort()
        
        # track current unused test data
        
        # the data set which contains the current unused data
        # it is a list of feature_set
        self._current_data_set = []

        # the current_section is the section
        # in which the newest data in the current data set locates
        self._current_section = -1

        # the left file list is the path of the files in the current section
        # that has not been added to the current data set
        self._left_file_list  = [] 
        
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
        
    def add_data(self):
        """
        add data from the next file in the left_file_list
        that has not been added to the data set

        return: if no data has been added:  None 
                otherwise:  the udated dataset
        """
        data_set = self._current_data_set
        
        if self._left_file_list == []:
            if self.add_file_list() == False:
                return data_set
            
        file_path = self._data_path + self._left_file_list.pop(0)
        f = open(file_path)
        
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
       
