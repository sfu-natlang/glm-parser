from __future__ import division
import os, re
import logging

fgen_name = 'english_2nd_fgen'
parser_name = 'ceisner3'
sentence_number = 20

class TestCeisner3():
    def __init__(self):
        return

    def run_test(self, fgen, parser, learner, data_pool):
        print "Testing ceisner3 parser"
        print "Test sentence #: %d" % sentence_number
        self.fgen = fgen
        self.parser = parser()
        self.dp = data_pool
        # print self.dp.section_list

        count = sentence_number
        i = count
        # while self.dp.has_next_data():
        while i > 0:
            i = i - 1
            sent = self.dp.get_next_data()
            # sent = A(sent0, sent0_edges)

            sent3 = sent.word_list
            sent3_edges = sent.edge_list_index_only

            sentence = SampleSentence(sent3, sent3_edges)
      
            res_edge_list = self.parser.parse(sentence, sentence.get_score)

            if set(res_edge_list) == set (sentence.edge_list_index_only):
                count = count - 1

        test_res = count == i
        return test_res
    
#############################################################################
#                              testing data
#############################################################################
sent0 = ["ROOT","A","B","C"]
sent0_edges = [(0,1), (1,2), (1,3)]
sent0_grand_dep = [
    [1,2,0], [1,3,0]
]
sent0_sibling_dep = [
    [2,3,1], [3,2,1]
]
sent1 = ["ROOT","A","hearing","is","scheduled","on","the","issue","today","."]
sent1_edges = [(0,3), (3,2), (2,1), (3,9), (3,8), (3,5), (3,4), (5,7), (7,6)]
sent1_grand_dep = [
    [3,9,0], [3,8,0], [3,5,0], [3,4,0], [3,2,0],
    [5,7,3], [2,1,3], [7,6,5]
]

sent1_sibling_dep = [
    [4,5,3], [2,4,3], [2,5,3], [2,8,3], [2,9,3],
    [4,2,3], [4,5,3], [4,8,3], [4,9,3], [5,2,3],
    [5,4,3], [5,8,3], [5,9,3], [8,2,3], [8,4,3],
    [8,5,3], [8,9,3], [9,2,3], [9,4,3], [9,5,3],
    [9,8,3]
]

class SampleSentence():
    def __init__(self, word_list, edge_list):
        self.word_list = word_list
        self.edge_list_index_only = edge_list
        self.grand_child_list = self.get_grand_child_list(edge_list, len(word_list))
        self.sibling_list = self.get_sibling_list(edge_list, len(word_list))

    def get_second_order_local_vector(self,h,m,g,type):
        if type == 2:
            if [h,m,g] in self.grand_child_list:
                return 1

        if type == 1:
            if [h,m,g] in self.sibling_list: #s, t, h
                return 1

        return 0

    def get_grand_child_list(self, edge_list, n):
        grand_child_list = []
        for h, m in edge_list:
            for g in range(0, n):
                if (g, h) in edge_list:
                    grand_child_list.append([h,m,g])
        return grand_child_list

    def get_sibling_list(self, edge_list, n):
        sibling_list = []
        for h, m in edge_list:
            for s in range(0, n):
                if s == m:
                    continue
                elif (h, s) in edge_list:
                    sibling_list.append([m,s,h])
        return sibling_list

    def get_score(self, a):
        return a


