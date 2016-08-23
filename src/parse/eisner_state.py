# -*- coding: utf-8 -*-
import logging
from collections import namedtuple

logger = logging.getLogger('PARSER')

EisnerQueueNode = namedtuple("EisnerQueueNode", "s t d c key")

class EisnerState:
    """
    An Eisner State implementation, including multi keys:

    pos: POS pair (pos1, pos2), where pos1 is the POS tag of the head,
         and pos2 is the POS tag of the dependent

    pos_dict: a dictionary of key and its value {key: val, key val, ...}
              where key is a pos key (pos1, pos2) and val is a tuple:
              (score, q, key_s2q, key_q2t)
    """

    def __init__(self):
        self.pos_iter = -1
        self.pos_dict = {}
        self.pos_keys = []

    def init_id(self, state_id):
        """
        self.s: start index
        self.t: end index
        self.d: direction
                0: <--
                1: -->
        self.c: completeness (shape)
                0: triangle
                1: trapezoidal
        """
        self.s = state_id[0]
        self.t = state_id[1]
        self.d = state_id[2]
        self.c = state_id[3]

    def pos_init(self, state_id, pos_list):
        if not hasattr(self, 'id'):
            self.init_id(state_id)

        for pos_left in pos_list[self.s]:
            for pos_right in pos_list[self.t]:
                if self.s == self.t and pos_left != pos_right:
                    continue

                if self.d == 0 and self.c == 0:
                    self.pos_dict[(pos_right, pos_left)] = (0, self.s,
                                                            (pos_left, pos_left),
                                                            (pos_right, pos_left))
                    self.pos_keys.append((pos_right, pos_left))

                if self.d == 1 and self.c == 0:
                    self.pos_dict[(pos_left, pos_right)] = (0, self.t,
                                                            (pos_left, pos_right),
                                                            (pos_right, pos_right))
                    self.pos_keys.append((pos_left, pos_right))

                if self.s == self.t:
                    continue

                if self.d == 0 and self.c == 1:
                    self.pos_dict[(pos_right, pos_left)] = (0, self.s,
                                                            (pos_left, pos_left),
                                                            (pos_right, pos_list[self.s+1][0]))
                    self.pos_keys.append((pos_right, pos_left))

                if self.d == 1 and self.c == 1:
                    self.pos_dict[(pos_left, pos_right)] = (0, self.s,
                                                            (pos_left, pos_left),
                                                            (pos_right, pos_list[self.s+1][0]))
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

    def pos_update_score(self, shape, key_head, key_dep, val, init=False):
        if shape == 1:
            if (self.pos_dict[(key_head[0], key_dep[0])][0] == 0 and init) or self.pos_dict[(key_head[0], key_dep[0])][0] < val[0]:
                self.pos_set_score((key_head[0], key_dep[0]), val)
        else:
            if (self.pos_dict[(key_head[0], key_dep[1])][0] == 0 and init) or self.pos_dict[(key_head[0], key_dep[1])][0] < val[0]:
                self.pos_set_score((key_head[0], key_dep[1]), val)

    def pos_reset_iter(self):
        self.pos_iter = -1

    def pos_set_score(self, key, val):
        self.pos_dict[key] = val

    def pos_is_combinable(self, key):
        return self.pos_keys[self.pos_iter][1] == key[0]

    def pos_split(self, key):
        if self.d == 0 and self.c == 0:
            return EisnerQueueNode(self.s, self.pos_dict[key][1], 0, 0, self.pos_dict[key][2]), \
                   EisnerQueueNode(self.pos_dict[key][1], self.t, 0, 1, self.pos_dict[key][3])
        if self.d == 1 and self.c == 0:
            return EisnerQueueNode(self.s, self.pos_dict[key][1], 1, 1, self.pos_dict[key][2]), \
                   EisnerQueueNode(self.pos_dict[key][1], self.t, 1, 0, self.pos_dict[key][3])
        if self.c == 1:
            return EisnerQueueNode(self.s, self.pos_dict[key][1], 1, 0, self.pos_dict[key][2]), \
                   EisnerQueueNode(self.pos_dict[key][1] + 1, self.t, 0, 0, self.pos_dict[key][3])


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
