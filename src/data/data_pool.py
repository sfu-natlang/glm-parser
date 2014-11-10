# -*- coding: utf-8 -*-
from __future__ import division
import os, re
from sentence import *
import logging, settings

logging.basicConfig(filename='glm_parser.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


class DataPool():
    def __init__(self, section_set=[], data_path="./penn-wsj-deps/"):
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
        self.data_path = data_path
        #self.set_section_list(section_set)

        #self.reset_whole()
        #self.load()

    def reset_whole(self):
        """
        Reset the index variables and the data list
        data list is the list of data in the feature form
        """
        self.reset()
        self.data_list = []

    def reset(self):
        """
        Reset only the index variables
        """
        self.current_index = -1

    def has_next_data(self):
        i = self.current_index + 1
        if i >= 0 and i < len(self.data_list):
            return True
        else:
            return False

    def get_next_data(self):
        """
            make sure to use function has_next_data function before calling this function
        """
        self.current_index += 1
        if self.current_index % 1000 == 0:
            logging.debug("Data finishing %.2f%% ..." % (100 * self.current_index / len(self.data_list)))
        return self.data_list[self.current_index]

    def load(self):
        """
        Load the trainning data
        """
        logging.debug("Loading data...")
        for section in self.section_list:
            logging.debug("Loading section %02d " % section)
            for file_name in os.listdir(self.data_path + "%02d" % section):
                file_path = self.data_path + "%02d/" % section + file_name
                self.data_list = self.data_list + self.get_data_list(file_path)

    def get_data_list(self, file_path, flag=1):
        """
        Form the DependencyTree list from the specified file, using spinal feature

        :param file_path: the path to the data file
        :type: str

        :return: a list of DependencyTree in the specified file
        :rtype: list(DependencyTree)
        """
        if flag == 1:
            """
                Gives the <E, D> pair; E is a tuple <word_index, spine> comprised of a word
                in the sentence and the spine associated with it; D is a tuple <head_index,
                modifier_index, <position, r_or_s, spine_head, spine_modifier, is_prev>>

                r_or_s is a binary flag, 1 for regular, 0 for sister adjoin, -1 for root
            """

            file_path = "./test"
            f = open(file_path)
            word_list = []
            pos_list = []
            edge_set = {}

            E = []
            D = []

            line_list = []
            spine_list = []
            data_list = []
            for line in f:
                if line != '':
                    spine = spine = line.split("\"")[1]
                    line = line.rstrip('\n')
                    line_list.append(line)
                    spine_list.append(spine)

            for line in line_list:
                elem = line.split()
                word_list.append(elem[1])
                pos_list.append(elem[3])
                # Form E
                E.append((elem[0], spine_list[int(elem[0]) - 1]))

                # Form D
                is_prev = 0
                if elem[-2] == 's':
                    r_or_s = -1
                elif elem[-2] == 'r':
                    r_or_s = 0
                    if elem[-1] == 1:
                    # If there is a previous modifier
                        is_prev = 1
                else:
                    # Skip the root
                    continue

                head_index = int(elem[6])
                modifier_index = int(elem[0])
                position = elem[-3]

                spine_head = spine_list[head_index - 1]
                spine_modifier = spine_list[modifier_index - 1]

                label = (position, r_or_s, spine_head, spine_modifier, is_prev)
            print E
            print D
        else:
            f = open(file_path)
            data_list = []
            word_list = []
            pos_list = []
            edge_set = {}
            current_index = 0

            for line in f:
                line = line[:-1]
                if line != '':
                    current_index = current_index + 1
                    entity = line.split()
                    if len(entity) != 4:
                        logging.error("invalid data!!")
                    else:
                        word_list.append(entity[0])
                        pos_list.append(entity[1])
                        edge_set[(int(entity[2]), current_index)] = entity[3]
                else:
                    if word_list != []:
                        sent = Sentence(word_list, pos_list, edge_set)
                        data_list.append(sent)
                # print d_tree.get_word_list()
                        word_list = []
                        pos_list = []
                        edge_set = {}
                        current_index = 0
        return data_list


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
        self.section_list = [section for section in section_set if isinstance(section, int)]

        section_sets = \
            map(lambda section_tuple: range(section_tuple[0], section_tuple[1] + 1),
                [st for st in section_set if isinstance(st, tuple)])
        for s_set in section_sets:
            self.section_list = self.section_list + s_set

        self.section_list.sort()
        return  # #############################################################################################################
        # Scripts for testing data_pool

if __name__ == "__main__":
    #dp = DataPool([2], settings.WSJ_CONLL_LOSSY_PATH)
    #dp.load()
    dp = DataPool([2], "./test")  
    dp.get_data_list("./test")
    #print dp.get_next_data()
    # dp.get_data_list("settings",1)
    # while dp.has_next_data():
    #    dp.get_next_data()

