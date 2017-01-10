# distutils: language = c++
from libcpp.utility cimport pair
from libcpp.queue cimport queue
from libcpp.list cimport list
from libcpp cimport bool
from libc.stdlib cimport malloc, calloc, free

cdef struct EisnerNode:
    float score
    int mid_index

cdef struct EdgeRecoverNode:
    int h
    int m
    int x
    int shape

ctypedef EisnerNode* P_EisnerNode
ctypedef EisnerNode** PP_EisnerNode

cdef class EisnerParser:
    cdef PP_EisnerNode ***e
    cdef list[pair[int, int]] edge_list
    cdef int n
    cdef queue[EdgeRecoverNode] recover_queue

    def __cinit__(self):
        pass

    def init_eisner_matrix(self):
        self.e = <PP_EisnerNode***>malloc(self.n*sizeof(PP_EisnerNode**))
        cdef int i, j, k, l
        for i in range(self.n):
            self.e[i] = <P_EisnerNode***>calloc(self.n,sizeof(P_EisnerNode**))
            for j in range(self.n):
                self.e[i][j] = <P_EisnerNode**>calloc(self.n,sizeof(P_EisnerNode*))
                for k in range(self.n):
                    self.e[i][j][k] = <P_EisnerNode*>calloc(3,sizeof(P_EisnerNode))
                    for l in range(3):
                        self.e[i][j][k][l] = <P_EisnerNode>calloc(1,sizeof(EisnerNode))
        return

    def delete_eisner_matrix(self):
        cdef int i, j, k
        for i in range(self.n):
            for j in range(self.n):
                for k in range(2):
                    for l in range(2):
                        free(self.e[i][j][k][l])
                    free(self.e[i][j][k])
                free(self.e[i][j])
            free(self.e[i])

    def new_IGSpan_right(self, h, m, g, sent, arc_weight):
        cdef int r
        # must satisfy h < m:
        if h >= m:
            print "invalid h < m condition in new_IGSpan_right"
            return

        cdef float edge_score = arc_weight(sent.get_second_order_local_vector(h, m, g, 2)) #g
        #print "new_IGSpan_right", edge_score
        cdef int max_index = h
        cdef float max_score = \
            self.e[h][h][g][0].score + self.e[m][h+1][h][0].score + edge_score

        cdef float cur_score
        for r from h < r < m by 1:
            cur_score = self.e[h][r][g][0].score + self.e[m][r+1][h][0].score + edge_score
            if max_score < cur_score:
                max_score = cur_score
                max_index = r

        self.e[h][m][g][1].score = max_score
        self.e[h][m][g][1].mid_index = max_index
        return

    def new_IGSpan_left(self, h, m, g, sent, arc_weight):
        cdef int r
        # must satisfy h > m:
        if h <= m:
            print "invalid h > m condition in new_IGSpan_left"
            return

        cdef float edge_score = arc_weight(sent.get_second_order_local_vector(h, m, g, 2)) #g
        #print "new_IGSpan_left", edge_score
        cdef int max_index = m
        cdef float max_score = \
            self.e[h][m+1][g][0].score + self.e[m][m][h][0].score + edge_score

        cdef float cur_score
        for r from m < r < h by 1:
            cur_score = self.e[h][r+1][g][0].score + self.e[m][r][h][0].score + edge_score
            if max_score < cur_score:
                max_score = cur_score
                max_index = r

        self.e[h][m][g][1].score = max_score
        self.e[h][m][g][1].mid_index = max_index
        return

    def new_SSpan(self, m, m1, h, sent, arc_weight):
        cdef int s, t, r
        if m < m1:
            s = m
            t = m1
        else:
            s = m1
            t = m

        cdef float edge_score = arc_weight(sent.get_second_order_local_vector(s, t, h, 1)) # s -- must ensure s < t
        #print "new_SSpan", edge_score
        cdef int max_index = s
        cdef float max_score = \
            self.e[s][s][h][0].score + self.e[t][s+1][h][0].score + edge_score

        cdef float cur_score
        for r from s < r < t by 1:
            cur_score = self.e[s][r][h][0].score + self.e[t][r+1][h][0].score + edge_score
            if max_score < cur_score:
                max_score = cur_score
                max_index = r

        self.e[m][m1][h][2].score = max_score
        self.e[m][m1][h][2].mid_index = max_index
        self.e[m1][m][h][2].score = max_score
        self.e[m1][m][h][2].mid_index = max_index
        return

    def update_IGSpan(self, h, m, g, sent, arc_weight):
        cdef int s, t, r
        if (h - m == 1) or (m - h == 1):
            return

        if h < m:
            s = h
            t = m
        else:
            s = m
            t = h

        cdef float edge_score = arc_weight(sent.get_second_order_local_vector(h, m, g, 2)) # g
        #print "update_IGSpan", edge_score
        cdef int max_index = s+1
        cdef float max_score = \
            self.e[h][s+1][g][1].score + self.e[m][s+1][h][2].score + edge_score

        cdef float cur_score
        for r from s+1 < r < t by 1:
            cur_score = self.e[h][r][g][1].score + self.e[m][r][h][2].score + edge_score
            if max_score < cur_score:
                max_score = cur_score
                max_index = r

        if self.e[h][m][g][1].score < max_score :
            self.e[h][m][g][1].score = max_score
            self.e[h][m][g][1].mid_index = -max_index #negative index to indicate a sibling

        return

    def new_CGSpan(self, h, m, g):
        cdef int s, t, r
        if h < m:
            s = h
            t = m
        else:
            s = m
            t = h

        cdef int max_index = m
        cdef float max_score = \
            self.e[h][m][g][1].score + self.e[m][m][h][0].score

        cdef float cur_score
        for r from s < r < t by 1:
            cur_score = self.e[h][r][g][1].score + self.e[r][m][h][0].score
            if max_score < cur_score:
                max_score = cur_score
                max_index = r

        self.e[h][m][g][0].score = max_score
        self.e[h][m][g][0].mid_index = max_index
        return

    def print_eisner_matrix(self):
        cdef int s, t, g

        for g from 0 <= g < self.n by 1:
            print "CGSpan, G:", g
            for s from 0 <= s < self.n by 1:
                for t from 0 <= t < self.n by 1:
                    print self.e[s][t][g][0].score, '\t',
                print

            print "IGSpan, G", g
            for s from 0 <= s < self.n by 1:
                for t from 0 <= t < self.n by 1:
                    print self.e[s][t][g][1].score, '\t',
                print

            print "SSpan, H:", g
            for s from 0 <= s < self.n by 1:
                for t from 0 <= t < self.n by 1:
                    print self.e[s][t][g][1].score,  '\t',
                print

    cdef add_edge(self, int h, int m):
        cdef pair[int, int] edge
        edge.first = h
        edge.second = m
        self.edge_list.push_back(edge)

        # print '(', h, ',', m, ')'

    cdef init_recover_queue(self):
        while not self.recover_queue.empty():
            self.recover_queue.pop()

    cdef push_recover_queue(self, h, m, x, shape):
        cdef EdgeRecoverNode new_node
        if h != m:
            new_node.h = h
            new_node.m = m
            new_node.x = x
            new_node.shape = shape
            self.recover_queue.push(new_node)

    cdef get_edge_list(self):
        cdef EdgeRecoverNode node
        self.init_recover_queue()

        if not self.edge_list.empty():
            self.edge_list.clear()

        cdef int s, mid_index
        cdef float max_score
        max_score = self.e[0][1][0][0].score + self.e[0][self.n-1][0][0].score
        mid_index = 1

        for s from 0 < s < self.n by 1:
            if max_score < (self.e[s][1][0][0].score + self.e[s][self.n-1][0][0].score):
                max_score = self.e[s][1][0][0].score + self.e[s][self.n-1][0][0].score
                mid_index = s

        self.add_edge(0, mid_index)
        self.push_recover_queue(mid_index, 1, 0, 0)
        self.push_recover_queue(mid_index, self.n-1, 0, 0)
        while not self.recover_queue.empty():
            node = self.recover_queue.front()
            self.recover_queue.pop()

            if node.shape == 0:
                self.split_triangle(node)
            if node.shape == 1:
                self.split_trapezoid(node)
            if node.shape == 2:
                self.split_rectangle(node)

        return

    cdef split_triangle(self, EdgeRecoverNode node):
        """
        triangle: e[h][m][g][0]
        """

        cdef int q = self.e[node.h][node.m][node.x][0].mid_index

        self.push_recover_queue(node.h, q, node.x, 1)
        self.push_recover_queue(q, node.m, node.h, 0)

        return

    cdef split_trapezoid(self, EdgeRecoverNode node):
        """
        trapezoid: e[h][m][g][1]
        """
        self.add_edge(node.h, node.m)

        cdef int q = self.e[node.h][node.m][node.x][1].mid_index

        if q > 0 and node.h < node.m: # grand-grand
            self.push_recover_queue(node.h, q, node.x, 0)
            self.push_recover_queue(node.m, q+1, node.h, 0)
        elif q > 0 and node.h > node.m:
            self.push_recover_queue(node.h, q+1, node.x, 0)
            self.push_recover_queue(node.m, q, node.h, 0)
        elif q < 0: # grand-sibling
            q = -q
            self.push_recover_queue(node.h, q, node.x, 1)
            self.push_recover_queue(node.m, q, node.h, 2)
        else:
            print "invalid mid_index or (h,m) relation for trapezoid split"
            print node.h, node.m, q

        return

    cdef split_rectangle(self, EdgeRecoverNode node):
        """
        rectangle: e[m][m1][h][2] (h is the common head)
        """

        cdef int q = self.e[node.h][node.m][node.x][2].mid_index
        cdef s,t
        if node.h < node.m:
            s = node.h
            t = node.m
        else:
            s = node.m
            t = node.h
        self.push_recover_queue(s, q, node.x, 0)
        self.push_recover_queue(t, q+1, node.x, 0)

        return

    def update_eisner_matrix(self, s, t, g, sent, arc_weight):
        self.new_IGSpan_right(s, t, g, sent, arc_weight)
        self.new_IGSpan_left(t, s, g, sent, arc_weight)
        self.new_SSpan(s, t, g, sent, arc_weight)
        self.update_IGSpan(s, t, g, sent, arc_weight)
        self.update_IGSpan(t, s, g, sent, arc_weight)
        self.new_CGSpan(s, t, g)
        self.new_CGSpan(t, s, g)

    def parse(self, sent, arc_weight, tagger=None):
        if tagger is not None:
            sent.set_pos_list(tagger.getTags(sent))

        self.n = len(sent.word_list)
        self.init_eisner_matrix()

        for m from 1 <= m < self.n by 1:
            for s from 0 <= s < self.n by 1:
                t = s + m
                if t >= self.n:
                    break

                for g from 0 <= g < s by 1:
                    self.update_eisner_matrix(s,t,g,sent,arc_weight)

                for g from t < g < self.n by 1:
                    self.update_eisner_matrix(s,t,g,sent,arc_weight)

        # self.print_eisner_matrix()
        self.get_edge_list()
        self.delete_eisner_matrix()

        return self.edge_list
