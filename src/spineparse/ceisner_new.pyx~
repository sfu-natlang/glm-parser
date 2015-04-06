# distutils: language = c++
from libcpp.utility cimport pair
from libcpp.queue cimport queue
from libcpp.list cimport list
from libcpp cimport bool
from libc.stdlib cimport malloc, calloc, free

cdef struct EisnerNode:
    float score
    int mid_index
    char r_or_s
    int position
    
#TODO try size_t
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
                self.e[i][j] = <P_EisnerNode**>calloc(2,sizeof(P_EisnerNode*))
                for k in range(2):
                    self.e[i][j][k] = <P_EisnerNode*>calloc(2,sizeof(P_EisnerNode))
                    for l in range(2):
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

    
    def combine_triangle(self, head, modifier, arc_weight, sent):
        # s < t strictly
        if head == modifier:
            print "invalid head and modifier for combine triangle!!!"
            
        cdef int s, t, q
        if head < modifier:
            s = head
            t = modifier
        else:
            s = modifier
            t = head


        cdef int join_pos, join_number, r_or_s, max_index
        cdef float edge_score, max_score
        
        h_spine = self.psent.spine_list[head]
        join_number = h_spine.count('(')
        escore_list = []

        # can score be negative? yes
        # use the first value 
        cdef float max_escore = arc_weight(self.psent.get_local_vector(head, modifier, 0, 0))


        cdef int max_join_pos = 0
        cdef int max_rors = 0

        for join_pos from 0 <= join_pos < join_number by 1:
            for r_or_s from in [0, 1]:
                edge_score = arc_weight(self.psent.get_local_vector(head, modifier, join_pos, r_or_s))
                escore_list.append(edge_score);
                if edge_score > max_escore:
                    max_escore = edge_score
                    max_join_pos = join_pos
                    max_rors = r_or_s

        cdef int max_index = s
        cdef float max_score = \
            self.e[s][s][1][0].score + self.e[s+1][t][0][0].score + max_escore

        cdef float cur_score
        for q from s < q < t by 1:
            cur_score = self.e[s][q][1][0].score + self.e[q+1][t][0][0].score + max_escore
            if max_score < cur_score:
                max_score = cur_score
                max_index = q


        return max_score, max_index, max_rors, max_join_pos

'''
        cdef float edge_score = arc_weight(sent.get_local_vector(head, modifier))
        cdef int max_index = s
        cdef float max_score = \
            self.e[s][s][1][0].score + self.e[s+1][t][0][0].score + edge_score

        cdef float cur_score
        for q from s < q < t by 1:
            cur_score = self.e[s][q][1][0].score + self.e[q+1][t][0][0].score + edge_score
            if max_score < cur_score:
                max_score = cur_score
                max_index = q
        return max_score, max_index 
'''
    
    cdef combine_left(self, int s, int t):        
        # s < t strictly
        if s >= t:
            print "invalid head and modifier for combine left!!!"
        
        cdef int max_index = s
        cdef float max_score = self.e[s][s][0][0].score + self.e[s][t][0][1].score

        cdef float cur_score
        cdef int q
        for q from s < q < t by 1:
            cur_score = self.e[s][q][0][0].score + self.e[q][t][0][1].score
            if max_score < cur_score:
                max_score = cur_score
                max_index = q

        return max_score, max_index 
       
    cdef combine_right(self, int s, int t):
        # s < t strictly
        if s >= t:
            print "invalid head and modifier for combine right!!!"
        
        cdef int max_index = s+1
        cdef float max_score = self.e[s][s+1][1][1].score + self.e[s+1][t][1][0].score

        cdef float cur_score
        cdef int q
        for q from s+1 < q <= t by 1:
            cur_score = self.e[s][q][1][1].score + self.e[q][t][1][0].score
            if max_score < cur_score:
                max_score = cur_score
                max_index = q
                
        return max_score, max_index     

    cdef EdgeRecoverNode new_edge_recover_node(self, int s, int t, int orien, int shape):
        cdef EdgeRecoverNode new_node
        new_node.s = s
        new_node.t = t
        new_node.orientation = orien
        new_node.shape = shape

        return new_node
    
    cdef split_right_triangle(self, EdgeRecoverNode node):
        """
        right triangle: e[s][t][1][0]
        """
        cdef EdgeRecoverNode node_left, node_right
        
        cdef int q = self.e[node.s][node.t][1][0].mid_index
        
        node_left = self.new_edge_recover_node(node.s, q, 1, 1)
        node_right = self.new_edge_recover_node(q, node.t, 1, 0)

        return node_left, node_right
        
    cdef split_left_triangle(self, EdgeRecoverNode node):
        """
        left triangle: e[s][t][0][0]
        """
        cdef EdgeRecoverNode node_left, node_right
        
        cdef int q = self.e[node.s][node.t][0][0].mid_index
        
        node_left = self.new_edge_recover_node(node.s, q, 0, 0)
        node_right = self.new_edge_recover_node(q, node.t, 0, 1)

        return node_left, node_right

    cdef split_right_trapezoid(self, EdgeRecoverNode node):
        """
        right trapezoid: e[s][t][1][1]
        """
        cdef pair[int, int] edge
        edge.first = node.s
        edge.second = node.t
        self.edge_list.push_back(edge)
        
        cdef EdgeRecoverNode node_left, node_right

        cdef int q = self.e[node.s][node.t][1][1].mid_index
        node_left = self.new_edge_recover_node(node.s, q, 1, 0)
        node_right = self.new_edge_recover_node(q+1, node.t, 0, 0)
        
        return node_left, node_right

    cdef split_left_trapezoid(self, EdgeRecoverNode node):
        """
        left trapezoid: e[s][t][0][1]
        """
        cdef pair[int, int] edge
        edge.first = node.t
        edge.second = node.s
        self.edge_list.push_back(edge)
        
        cdef EdgeRecoverNode node_left, node_right

        cdef int q = self.e[node.s][node.t][0][1].mid_index
        node_left = self.new_edge_recover_node(node.s, q, 1, 0)
        node_right = self.new_edge_recover_node(q+1, node.t, 0, 0)

        return node_left, node_right

    
    cdef get_edge_list(self):
        
        cdef EdgeRecoverNode node, node_left, node_right
        cdef queue[EdgeRecoverNode] node_queue

        if not self.edge_list.empty():
            self.edge_list.clear()
        
        node_queue.push(self.new_edge_recover_node(0, self.n-1, 1, 0))
        while not node_queue.empty():
            push = False
            node = node_queue.front()
            node_queue.pop()
            
            if node.orientation == 1 and node.shape == 0:
                node_left, node_right = self.split_right_triangle(node)
                push = True
            if node.orientation == 0 and node.shape == 0:
                node_left, node_right = self.split_left_triangle(node)
                push = True
            if node.orientation == 1 and node.shape == 1:
                node_left, node_right = self.split_right_trapezoid(node)
                push = True
            if node.orientation == 0 and node.shape == 1:
                node_left, node_right = self.split_left_trapezoid(node)
                push = True
                
            if push:
                if node_left.s != node_left.t:
                    node_queue.push(node_left)
                if node_right.s != node_right.t:
                    node_queue.push(node_right)
        return
    
    def parse(self, sent, arc_weight):	
        
        self.n = len(sent.word_list)
        self.init_eisner_matrix()

        cdef int m, s, t, q
        self.psent = ParserFeatureGenerator(sent);

        #TODO: try for m in range(1,self.n)
        for m from 1 <= m < self.n by 1: 
            for s from 0 <= s < self.n by 1:
                t = s + m
                if t >= self.n:
                    break


                self.e[s][t][0][1].score, self.e[s][t][0][1].mid_index, self.e[s][t][0][1].r_or_s, self.e[s][t][0][1].position =\
                    self.combine_triangle(t, s, arc_weight, sent)
                self.e[s][t][1][1].score, self.e[s][t][1][1].mid_index, self.e[s][t][1][1].r_or_s, self.e[s][t][1][1].position =\
                    self.combine_triangle(s, t, arc_weight, sent)
                self.e[s][t][0][0].score, self.e[s][t][0][0].mid_index =\
                    self.combine_left(s, t)
                self.e[s][t][1][0].score, self.e[s][t][1][0].mid_index =\
                    self.combine_right(s, t)
'''
                self.e[s][t][0][1].score, self.e[s][t][0][1].mid_index =\
                    self.combine_triangle(t, s, arc_weight, sent)
                self.e[s][t][1][1].score, self.e[s][t][1][1].mid_index =\
                    self.combine_triangle(s, t, arc_weight, sent)
                self.e[s][t][0][0].score, self.e[s][t][0][0].mid_index =\
                    self.combine_left(s, t)
                self.e[s][t][1][0].score, self.e[s][t][1][0].mid_index =\
                    self.combine_right(s, t)
'''
       
        self.get_edge_list()       
        self.delete_eisner_matrix()

        return self.edge_list
        
