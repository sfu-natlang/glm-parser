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
    int s
    int t
    int orientation
    int shape

ctypedef EisnerNode* P_EisnerNode
ctypedef EisnerNode** PP_EisnerNode 

cdef class EisnerParser:
    cdef PP_EisnerNode ***e
    cdef list[pair[int, int]] edge_list
    cdef int n
    cdef int tt
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

    def new_IGSpan(self, h, m, g, arc_weight):
        cdef int s, t, r
        if h < m:
            s = h
            t = m
        else:
            s = m
            t = h

        cdef float edge_score = arc_weight(h, m, g, 'g')
        cdef int max_index = s
        cdef float max_score = \
            self.e[h][s][g][0].score + self.e[m][s+1][g][0].score + edge_score

        cdef float cur_score
        for r from s < r < t by 1:
            cur_score = self.e[h][r][g][0].score + self.e[m][r+1][g][0].score + edge_score
            if max_score < cur_score:
                max_score = cur_score
                max_index = r

        self.e[h][m][g][1].score = max_score
        self.e[h][m][g][1].mid_index = max_index
        return

    def new_SSpan(self, h, m, m1, arc_weight):
        cdef int s, t, r
        if m < m1:
            s = m
            t = m1
        else:
            s = m1
            t = m

        cdef float edge_score = arc_weight(h, s, t, 's') # must ensure s < t
        cdef int max_index = s
        cdef float max_score = \
            self.e[m][s][h][0].score + self.e[m1][s+1][h][0].score + edge_score

        cdef float cur_score
        for r from s < r < t by 1:
            cur_score = self.e[m][r][h][0].score + self.e[m1][r+1][h][0].score + edge_score
            if max_score < cur_score:
                max_score = cur_score
                max_index = r

        self.e[m][m1][h][2].score = max_score
        self.e[m][m1][h][2].mid_index = max_index
        self.e[m1][m][h][2].score = max_score
        self.e[m1][m][h][2].mid_index = max_index
        return
    
    def update_IGSpan(self, h, m, g, arc_weight):
        cdef int s, t, r
        if h < m:
            s = h
            t = m
        else:
            s = m
            t = h

        cdef float edge_score = arc_weight(h, m, g, 'g')
        cdef int max_index = s
        cdef float max_score = \
            self.e[h][s][g][1].score + self.e[h][s][m][2].score + edge_score

        cdef float cur_score
        for r from s < r < t by 1:
            cur_score = self.e[h][r][g][1].score + self.e[h][r][m][2].score + edge_score
            if max_score < cur_score:
                max_score = cur_score
                max_index = r

        if self.e[h][m][g][1].score < max_score :
            self.e[h][m][g][1].score = max_score
            self.e[h][m][g][1].mid_index = max_index

        return

    def new_CGSpan(self, h, m, g):
        cdef int s, t, r
        if h < m:
            s = h
            t = m
        else:
            s = m
            t = h

        cdef int max_index = s
        cdef float max_score = \
            self.e[h][s][g][1].score + self.e[s][m][h][0].score

        cdef float cur_score
        for r from s < r <= t by 1:
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


    def parse(self, sent, arc_weight):	

        self.n = len(sent.word_list)
        self.init_eisner_matrix()

        for m from 1 <= m < self.n by 1: 
            for s from 0 <= s < self.n by 1:
                t = s + m
                if t >= self.n:
                    break

                for g from 0 <= g < s by 1:
                    self.new_IGSpan(s, t, g, arc_weight)
                    self.new_IGSpan(t, s, g, arc_weight)
                    self.new_SSpan(g, s, t, arc_weight)
                    self.update_IGSpan(s, t, g, arc_weight)
                    self.update_IGSpan(t, s, g, arc_weight)
                    self.new_CGSpan(s, t, g)
                    self.new_CGSpan(t, s, g)
                
                for g from t < g < self.n by 1:
                    self.new_IGSpan(s, t, g, arc_weight)
                    self.new_IGSpan(t, s, g, arc_weight)
                    self.new_SSpan(g, s, t, arc_weight)
                    self.update_IGSpan(s, t, g, arc_weight)
                    self.update_IGSpan(t, s, g, arc_weight)
                    self.new_CGSpan(s, t, g)
                    self.new_CGSpan(t, s, g)
        
        self.print_eisner_matrix()
        
        gsore = 0
        gs = 0
        mid_1 = 0
        mid_2 = 0
        for s from 0 <= s < self.n by 1:   
            if gsore < (self.e[s][1][0][0].score + self.e[s][self.n-1][0][0].score):
                gsore = (self.e[s][1][0][0].score + self.e[s][self.n-1][0][0].score)
                gs = s
                mid_1 = self.e[s][1][0][0].mid_index
                mid_2 = self.e[s][self.n-1][0][0].mid_index

        print gsore, gs, mid_1, mid_2


        return self.edge_list
