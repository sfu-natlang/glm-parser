# -*- coding: utf-8 -*-
from pos_tagger import PosTagger
import copy
import time
from numpy import inf
import logging
# from data.sentence import Sentence

logger = logging.getLogger('PARSER')


class EisnerState:
    """
    An Eisner parsing algorithm implementation
    """

    def __init__(self):
        self.pos_iter = -1
        self.pos_dict = {}
        self.pos_keys = []

    def init_id(self, state_id):
        self.id = state_id

    def pos_init(self, state_id, pos_list):
        if not hasattr(self, 'id'):
            self.init_id(state_id)

        if state_id[2] == 0:
            head, tail = 1, 0
        else:
            head, tail = 0, 1

        for pos_left in pos_list[state_id[0]]:
            for pos_right in pos_list[state_id[1]]:
                if state_id[0] == state_id[1] and pos_left != pos_right:
                    continue

                if state_id[2] == 0 and state_id[3] == 0:
                    self.pos_dict[(pos_right, pos_left)] = (0, state_id[0],
                                                            (pos_left, pos_left),
                                                            (pos_right, pos_left))
                    self.pos_keys.append((pos_right, pos_left))

                if state_id[2] == 1 and state_id[3] == 0:
                    self.pos_dict[(pos_left, pos_right)] = (0, state_id[1],
                                                            (pos_left, pos_right),
                                                            (pos_right, pos_right))
                    self.pos_keys.append((pos_left, pos_right))

                if state_id[0] == state_id[1]:
                    continue

                if state_id[2] == 0 and state_id[3] == 1:
                    self.pos_dict[(pos_right, pos_left)] = (0, state_id[0],
                                                            (pos_left, pos_left),
                                                            (pos_right, pos_list[state_id[0]+1][0]))
                    self.pos_keys.append((pos_right, pos_left))

                if state_id[2] == 1 and state_id[3] == 1:
                    self.pos_dict[(pos_left, pos_right)] = (0, state_id[0],
                                                            (pos_left, pos_left),
                                                            (pos_right, pos_list[state_id[0]+1][0]))
                    self.pos_keys.append((pos_left, pos_right))


    def pos_has_next_key(self):
        return self.pos_iter < len(self.pos_keys) - 1

    def pos_get_next_key(self):
        self.pos_iter += 1
        if self.pos_iter < len(self.pos_keys):
            return self.pos_keys[self.pos_iter]
        else:
            logger.error('No next key!')
            raise ValueError('No next key')

    def pos_get_head_pos(self, key=None):
        if (key == None):
            return self.pos_keys[self.pos_iter][0]
        else:
            return key[0]

    def pos_get_tail_pos(self, key=None):
        if (key == None):
            return self.pos_keys[self.pos_iter][1]
        else:
            return key[1]

    def pos_get_score(self, key):
        return self.pos_dict[key][0]

    def pos_update_score(self, shape, key_head, key_dep, val):
        if shape == 1:
            if self.pos_dict[(key_head[0], key_dep[0])][0] == 0 or self.pos_dict[(key_head[0], key_dep[0])][0] < val[0]:
                self.pos_set_score((key_head[0], key_dep[0]), val)
        else:
            if self.pos_dict[(key_head[0], key_dep[1])][0] == 0 or self.pos_dict[(key_head[0], key_dep[1])][0] < val[0]:
                self.pos_set_score((key_head[0], key_dep[1]), val)

    def pos_reset_iter(self):
        self.pos_iter = -1

    def pos_set_score(self, key, val):
        self.pos_dict[key] = val

    def pos_is_combinable(self, key):
        return self.pos_keys[self.pos_iter][1] == key[0]

    def pos_split(self, key):
        if self.id[2] == 0 and self.id[3] == 0:
            return (self.id[0], self.pos_dict[key][1], 0, 0, self.pos_dict[key][2]), \
                   (self.pos_dict[key][1], self.id[1], 0, 1, self.pos_dict[key][3])
        if self.id[2] == 1 and self.id[3] == 0:
            return (self.id[0], self.pos_dict[key][1], 1, 1, self.pos_dict[key][2]), \
                   (self.pos_dict[key][1], self.id[1], 1, 0, self.pos_dict[key][3])
        if self.id[3] == 1:
            return (self.id[0], self.pos_dict[key][1], 1, 0, self.pos_dict[key][2]), \
                   (self.pos_dict[key][1] + 1, self.id[1], 0, 0, self.pos_dict[key][3])


#    def init_eisner_matrix(self,n):
#        """
#        Initialize a dynamic programming table, i.e. e[0..n][0..n][0..1][0..1]
#
#        :param n: The length of the sentence including the artificial ROOT
#        :type n: integer
#
#        :return: An initialized table with all chart entries being (0,[])
#        :rtype: Multi-dimensional list
#        """
#        # CAUTION: Must use deepcopy() here, since Python uses the object
#        # reference model, which will cause trouble if we use shared object
#        # in the chart
#        # The last dimenison of the table. It uses a tuple to store score
#        # and edges of current stage
#        e1 = [copy.deepcopy([0,[]]) for i in range(2)]
#        # The dimension that specifies the direction of the edge
#        e2 = [copy.deepcopy(e1) for i in range(2)]
#        # The end of the span
#        e3 = [copy.deepcopy(e2) for i in range(n)]
#        # The start of the span
#        e4 = [copy.deepcopy(e3) for i in range(n)]
#        return e4
