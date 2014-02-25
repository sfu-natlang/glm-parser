# -*- coding: utf-8 -*-

import os

class DataSet():
    """
    Read the test data files and generate the trees for parser testing
    The class is specifically for penn-wsj-deps data
    
    the section set can be defined as either tuple or list
    but cannot be both at the same time
    """
    def __init__(self,  
                 section_set=[(2,21)], 
                 data_path=".\\penn-wsj-deps\\"):
        
        self.data_path = data_path
            
        self.section_set = section_set
        self.section_set.sort()
        
        # track current unused test data
        self.current_data_set = []
        self.current_section = None      
        self.left_file_list  = [] 
        
        return            
    
    def add_file_list(self):
        next_section = self.get_next_section()
        self.current_section = next_section
        if next_section == None or self.data_path == None:
            return False
        else:
            for file in os.listdir(self.data_path + "%02d" % next_section):
                self.left_file_list.append("%02d\\" % next_section + file)
        return True
                      
    def get_next_data(self):
        data_set = self.current_data_set
        if data_set == []:
            data_set = self.add_data()
        return data_set.pop(0)
        
    def add_data(self):
        data_set = self.current_data_set
        
        if self.left_file_list == []:
            if self.add_file_list() == False:
                return None
            
        file_path = self.data_path + self.left_file_list.pop(0)
        f = open(file_path)
        
        word_list = []
        edge_set = []
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
                    edge_set.append((entry[2], str(current_index)))
            else:
                if word_list != []:
                    data_set.append((word_list, set(edge_set)))
                word_list = []
                edge_set = []
                current_index = 0
        return data_set

    def get_next_section(self):
        if self.section_set == []:
            return None
        
        if self.current_section == None:
            next_section = 0
        else:
            next_section = self.current_section + 1
        if isinstance(self.section_set[0], tuple):
            for sec_range in self.section_set:
                if  next_section < sec_range[0]:
                    return sec_range[0]
                elif next_section <= sec_range[1]:
                    return next_section
            return None
        else:
            while next_section not in self.section_set \
            and next_section <= max(self.section_set):
                next_section = next_section + 1
            if next_section in self.section_set:
                return next_section
            else:
                return None
            
       
    def set_data_path(self, data_path):
        """
        the data_path is the path to the 'penn-wsj-deps' folder
        (include "penn-wsj-deps")
        """
        self.data_path = data_path
        return