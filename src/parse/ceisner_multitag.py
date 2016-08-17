# -*- coding: utf-8 -*-

from numpy import inf
import copy, time
from pos_tagger import PosTagger
from eisner_state import EisnerState
import logging

logger = logging.getLogger('PARSER')


class EisnerParser:
    """
    An Eisner parsing algorithm implementation
    """

    def __init__(self):
        return

    def init_eisner_matrix(self, pos_list):
        """
        Initialize a dynamic programming table, i.e. e[0..n][0..n][0..1][0..1]

        orientation: 
        <-:0
        ->:1
        shape:
        trapezoid:1
        triangle:0

        :param n: The length of the sentence including the artificial ROOT
        :type n: integer
        """
        # CAUTION: Must use deepcopy() here, since Python uses the object
        # reference model, which will cause trouble if we use shared object
        # in the chart
        # The last dimenison of the table. It uses a tuple to store score
        # and edges of current stage
        e1 = [copy.deepcopy(EisnerState()) for i in range(2)]
        # The dimension that specifies the direction of the edge
        e2 = [copy.deepcopy(e1) for i in range(2)]
        # The end of the span
        e3 = [copy.deepcopy(e2) for i in range(self.n)]
        # The start of the span
        e4 = [copy.deepcopy(e3) for i in range(self.n)]
        self.e = e4

        for i in range(0, self.n):
            self.e[i][i][0][1].pos_init((i, i, 0, 1), pos_list)
            self.e[i][i][1][1].pos_init((i, i, 1, 1), pos_list)
            self.e[i][i][0][0].pos_init((i, i, 0, 0), pos_list)
            self.e[i][i][1][0].pos_init((i, i, 1, 0), pos_list)

        return

    def combine_left_trapezoid(self, s, t, q, arc_weight, sent):
        # print sent.gold_global_vector
        while self.e[s][q][1][0].pos_has_next_key():
            key0 = self.e[s][q][1][0].pos_get_next_key()
            while self.e[q+1][t][0][0].pos_has_next_key():
                key1 = self.e[q+1][t][0][0].pos_get_next_key()

                edge_score = arc_weight(
                    sent.get_local_vector(
                        t,
                        s,
                        self.e[q+1][t][0][0].pos_get_head_pos(),
                        self.e[s][q][1][0].pos_get_head_pos()
                    )
                )
                score = self.e[s][q][1][0].pos_get_score(key0) + \
                        self.e[q+1][t][0][0].pos_get_score(key1) + \
                        edge_score

                self.e[s][t][0][1].pos_update_score(1, key1, key0,
                                                    (score, q, key0, key1))
            self.e[q+1][t][0][0].pos_reset_iter()
        self.e[s][q][1][0].pos_reset_iter()

    def combine_right_trapezoid(self, s, t, q, arc_weight, sent):
        while self.e[s][q][1][0].pos_has_next_key():
            key0 = self.e[s][q][1][0].pos_get_next_key()
            while self.e[q+1][t][0][0].pos_has_next_key():
                key1 = self.e[q+1][t][0][0].pos_get_next_key()
                edge_score = arc_weight(
                    sent.get_local_vector(
                        s,
                        t,
                        self.e[q+1][t][0][0].pos_get_head_pos(),
                        self.e[s][q][1][0].pos_get_head_pos()
                    )
                )
                score = self.e[s][q][1][0].pos_get_score(key0) + \
                        self.e[q+1][t][0][0].pos_get_score(key1) + \
                        edge_score
                self.e[s][t][1][1].pos_update_score(1, key0, key1,
                                                    (score, q, key0, key1))
            self.e[q+1][t][0][0].pos_reset_iter()
        self.e[s][q][1][0].pos_reset_iter()

    def combine_left_triangle(self, s, t, q, arc_weight, sent):
        while self.e[s][q][0][0].pos_has_next_key():
            key0 = self.e[s][q][0][0].pos_get_next_key()
            while self.e[q][t][0][1].pos_has_next_key():
                key1 = self.e[q][t][0][1].pos_get_next_key()
                if not self.e[q][t][0][1].pos_is_combinable(key0):
                    continue
                score = self.e[s][q][0][0].pos_get_score(key0) + \
                        self.e[q][t][0][1].pos_get_score(key1)
                self.e[s][t][0][0].pos_update_score(0, key1, key0,
                                                    (score, q, key0, key1))
            self.e[q][t][0][1].pos_reset_iter()
        self.e[s][q][0][0].pos_reset_iter()

    def combine_right_triangle(self, s, t, q, arc_weight, sent):
        while self.e[s][q][1][1].pos_has_next_key():
            key0 = self.e[s][q][1][1].pos_get_next_key()
            while self.e[q][t][1][0].pos_has_next_key():
                key1 = self.e[q][t][1][0].pos_get_next_key()
                if not self.e[s][q][1][1].pos_is_combinable(key1):
                    continue
                score = self.e[s][q][1][1].pos_get_score(key0) + \
                        self.e[q][t][1][0].pos_get_score(key1)
                self.e[s][t][1][0].pos_update_score(0, key0, key1,
                                                    (score, q, key0, key1))
            self.e[q][t][1][0].pos_reset_iter()
        self.e[s][q][1][1].pos_reset_iter()

    def get_edge_list(self):
        """
        node: (s, t, d, c, key) where
        s is the start index
        t is the end index
        d is the direction
        c is the completeness
        key is defined in Eisner_state, here it's (pos, pos) pair

        :return:
        {
            edge_list: [...], a list of edges predicted by parser
            pos_list: [...], a list of pos tags predicted by parser
        }
        """
        """
        :return:
        """
        max_score = -inf
        max_key = None
        self.edge_list = []
        self.pos_list = ['ROOT']
        queue = []
        for i in range(1, self.n):
            self.pos_list.append('TBD')

        while self.e[0][self.n - 1][1][0].pos_has_next_key():
            key = self.e[0][self.n - 1][1][0].pos_get_next_key()
            if self.e[0][self.n - 1][1][0].pos_get_score(key) > max_score:
                max_score = self.e[0][self.n - 1][1][0].pos_get_score(key)
                max_key = key
        self.e[0][self.n - 1][1][0].pos_reset_iter()

        queue.append((0, self.n-1, 1, 0, max_key))
        while queue:
            node = queue.pop(0)

            if node[2] == 0:
                self.pos_list[node[0]] = self.e[node[0]][node[1]][node[2]][node[3]].pos_get_tail_pos(node[4])
            else:
                self.pos_list[node[1]] = self.e[node[0]][node[1]][node[2]][node[3]].pos_get_tail_pos(node[4])

            if node[3] == 1:
                if node[2] == 0:
                    self.edge_list.append((node[1], node[0]))
                else:
                    self.edge_list.append((node[0], node[1]))

            node_left, node_right = self.e[node[0]][node[1]][node[2]][node[3]].pos_split(node[4])

            if node_left[0] != node_left[1]:
                queue.append(node_left)
            if node_right[0] != node_right[1]:
                queue.append(node_right)

    def store_parsed_result(self,parsed_result):
        """
        Saves the parsed result into the instance

        :param parsed_result: The return value of parse()
        :type parsed_result: See parse()
        """
        self.max_score = parsed_result[0]
        self.edge_set = parsed_result[1]
        return


    def parse(self, sent, arc_weight):
        self.n = len(sent.get_word_list())
        self.init_eisner_matrix(sent.get_pos_list())

        #TODO: try for m in range(1,self.n)
        for m in range(1, self.n):
            for s in range(0, self.n-1):
                t = s + m
                if t >= self.n:
                    break

                self.e[s][t][0][1].pos_init((s, t, 0, 1), sent.get_pos_list())
                self.e[s][t][1][1].pos_init((s, t, 1, 1), sent.get_pos_list())
                self.e[s][t][0][0].pos_init((s, t, 0, 0), sent.get_pos_list())
                self.e[s][t][1][0].pos_init((s, t, 1, 0), sent.get_pos_list())

                for q in range(s, t):
                    self.combine_left_trapezoid(s, t, q, arc_weight, sent)
                    self.combine_right_trapezoid(s, t, q, arc_weight, sent)
                    self.combine_left_triangle(s, t, q, arc_weight, sent)
                    self.combine_right_triangle(s, t, q+1, arc_weight, sent)

        self.get_edge_list()

        print self.edge_list
        print ''
        print self.pos_list
        return self.edge_list, self.pos_list
