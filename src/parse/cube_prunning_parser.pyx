# distutils: language = c++
from libcpp.utility cimport pair
from libcpp.queue cimport queue
from libcpp.vector cimport vector
from libcpp.algorithm cimport sort as stdsort
from libcpp.algorithm cimport push_heap, pop_heap
from libcpp.list cimport list
from libcpp cimport bool
from libc.stdlib cimport malloc, calloc, free
from collections import defaultdict

cdef struct EisnerNode:
    float score
    int mid_index
    EisnerNode *left;
    EisnerNode *right;
    
#TODO try size_t
cdef struct EdgeRecoverNode:
    int s
    int t
    int orientation
    int shape
    int mid_index
    EisnerNode *left
    EisnerNode *right

cdef bool max_heap_comp(EisnerNode a, EisnerNode b):
    return a.score < b.score
    
cdef bool sort_comp(EisnerNode a, EisnerNode b):
    return a.score > b.score

cdef cppclass EisnerHeap:
    vector[EisnerNode] data
    int maxSize
    EisnerHeap(int size):
        this.maxSize = size

    void push_back(EisnerNode node):
        
        data.push_back(node)
        push_heap(data.begin(), data.end(), &max_heap_comp)

    void pop_front():
        pop_heap(data.begin(), data.end(), &max_heap_comp)
        data.pop_back()

    void push(EisnerNode node):
        push_back(node)
        if data.size() > maxSize:
            data.pop_back()

    void sort():
        stdsort(data.begin(), data.end(), &sort_comp)
    
    int size():
        return data.size()

    EisnerNode front():
        return data.front()

ctypedef EisnerHeap* P_EisnerHeap
ctypedef EisnerHeap** PP_EisnerHeap   

cdef class EisnerParser:
    cdef PP_EisnerHeap ***e
    cdef list[pair[int, int]] edge_list
    cdef int n
    cdef int tt
    def __cinit__(self):
        pass
    
    def init_eisner_matrix(self, max_size = 6):
        self.e = <PP_EisnerHeap***>malloc(self.n*sizeof(PP_EisnerHeap**))
        cdef int i, j, k, l
        for i in range(self.n):
            self.e[i] = <P_EisnerHeap***>calloc(self.n,sizeof(P_EisnerHeap**))
            for j in range(self.n):
                self.e[i][j] = <P_EisnerHeap**>calloc(2,sizeof(P_EisnerHeap*))
                for k in range(2):
                    self.e[i][j][k] = <P_EisnerHeap*>calloc(2,sizeof(P_EisnerHeap))
                    for l in range(2):
                        self.e[i][j][k][l] = new EisnerHeap(max_size)
                    if i == j:
                        self.e[i][j][k][0].push(EisnerNode(0,i, NULL, NULL))
                        
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

    
    def combine_triangle(self, head, modifier, arc_weight, sent, cube_prunning):
        # s < t strictly
        if head == modifier:
            print "invalid head and modifier for combine triangle!!!"
            
        cdef int s, t, q, r
        cdef int direction
        if head < modifier:
            s = head
            t = modifier
            direction = 1
        else:
            s = modifier
            t = head
            direction = 0
            
        cdef float edge_score
        cdef EisnerNode node

        if cube_prunning == 0:
            edge_score = arc_weight(sent.get_local_vector(head, modifier))
        for q from s <= q < t by 1:
            if cube_prunning == 0:
                node.score = \
                    self.e[s][q][1][0].front().score + self.e[q+1][t][0][0].front().score + edge_score
                node.mid_index = q
                node.left = &self.e[s][q][1][0].data[0]
                node.right = &self.e[q+1][t][0][0].data[0]
                self.e[s][t][direction][1].push(node)
            else:
                for r from 0 <= r < self.e[s][q][1][0].size():
                    for u from 0 <= u < self.e[q+1][t][0][0].size():
                        node.score = self.e[s][q][1][0].data[r].score + self.e[q+1][t][0][0].data[u].score\
                        + arc_weight(sent.get_local_vector(head,
                                                           modifier,
                                                           [self. e[s][q][1][0].data[r].mid_index],
                                                           2**(1-direction)))
                        + arc_weight(sent.get_local_vector(head, 
                                                           modifier,
                                                           [self.e[q+1][t][0][0].data[u].mid_index],
                                                           2**(direction)))
                                                                
                        node.mid_index = q
                        node.left = &self.e[s][q][1][0].data[r]
                        node.right = &self.e[q+1][t][0][0].data[0]
                        self.e[s][t][direction][1].push(node)

        self.e[s][t][direction][1].sort()
    
    def combine_left(self, s, t, arc_weight, sent, cube_prunning):        
        # s < t strictly
        if s >= t:
            print "invalid head and modifier for combine left!!!"
        
        cdef EisnerNode node

        cdef int q, r
        for q from s <= q < t by 1:
            if cube_prunning == 0:
                node.score = self.e[s][q][0][0].front().score + self.e[q][t][0][1].front().score
                node.mid_index = q
                node.left = &self.e[s][q][0][0].data[0]
                node.right = &self.e[q][t][0][1].data[0]
                self.e[s][t][0][0].push(node)
            else:
               for 0 <= r < self.e[s][q][0][0].size():
                    node.score = self.e[s][q][0][0].data[r].score + self.e[q][t][0][1].front().score\
                        + arc_weight(sent.get_local_vector(t, q, [self.e[s][q][0][0].data[r].mid_index], 2))
                    node.mid_index = q
                    node.left = &self.e[s][q][0][0].data[r]
                    node.right = &self.e[q][t][0][1].data[0]
                    self.e[s][t][0][0].push(node)
        
        self.e[s][t][0][0].sort()
       
    def combine_right(self, s, t, arc_weight, sent, cube_prunning):
        # s < t strictly
        if s >= t:
            print "invalid head and modifier for combine right!!!"
        
        cdef EisnerNode node
        cdef int q, r
        for q from s < q <= t by 1:
            if cube_prunning == 0:
                node.score = self.e[s][q][1][1].front().score + self.e[q][t][1][0].front().score
                node.mid_index = q
                node.left = &self.e[s][q][1][1].data[0]
                node.right = &self.e[q][t][1][0].data[0]
                self.e[s][t][1][0].push(node)
            else:
                for 0 <= r < self.e[q][t][1][0].size():
                    node.score = self.e[s][q][1][1].front().score + self.e[q][t][1][0].data[r].score\
                        + arc_weight(sent.get_local_vector(s, q, [self.e[q][t][1][0].data[r].mid_index], 2))    
                    node.mid_index = q
                    node.left = &self.e[s][q][1][1].data[0]
                    node.right = &self.e[q][t][1][0].data[r]
                    self.e[s][t][1][0].push(node)
    
        self.e[s][t][1][0].sort()

    cdef EdgeRecoverNode new_edge_recover_node(self, int s, int t, int orien, int shape):
        cdef EdgeRecoverNode new_node
        new_node.s = s
        new_node.t = t
        new_node.orientation = orien
        new_node.shape = shape

        return new_node
    
    cdef get_edge_list(self):
        
        cdef EdgeRecoverNode node, node_left, node_right
        cdef queue[EdgeRecoverNode] node_queue
        cdef EisnerNode e_node
        cdef int q
        cdef pair[int,int] edge

        if not self.edge_list.empty():
            self.edge_list.clear()

        e_node = self.e[0][self.n-1][1][0].front()
        node = EdgeRecoverNode(0, self.n-1, 1, 0, e_node.mid_index, e_node.left, e_node.right)
        node_queue.push(node)
        while not node_queue.empty():
            push = False
            node = node_queue.front()
            node_queue.pop()
            
            if node.orientation == 1 and node.shape == 0:
                q = node.mid_index
                node_left = EdgeRecoverNode(node.s, q, 1, 1, node.left.mid_index, node.left.left, node.left.right)
                node_right = EdgeRecoverNode(q, node.t, 1, 0, node.right.mid_index, node.right.left, node.right.right)

                push = True
            if node.orientation == 0 and node.shape == 0:
                q = node.mid_index
                node_left = EdgeRecoverNode(node.s, q, 0, 0, node.left.mid_index, node.left.left, node.left.right)
                node_right = EdgeRecoverNode(q, node.t, 0, 1, node.right.mid_index, node.right.left, node.right.right)

                push = True
            if node.orientation == 1 and node.shape == 1:
                edge.first = node.s
                edge.second = node.t
                self.edge_list.push_back(edge) 
                q = node.mid_index
                node_left = EdgeRecoverNode(node.s, q, 1, 0, node.left.mid_index, node.left.left, node.left.right)
                node_right = EdgeRecoverNode(q+1, node.t, 0, 0, node.right.mid_index, node.right.left, node.right.right)

                push = True
            if node.orientation == 0 and node.shape == 1:
                edge.first = node.t
                edge.second = node.s
                self.edge_list.push_back(edge)
                q = node.mid_index
                node_left = EdgeRecoverNode(node.s, q, 1, 0, node.left.mid_index, node.left.left, node.left.right)
                node_right = EdgeRecoverNode(q+1, node.t, 0, 0, node.right.mid_index, node.right.left, node.right.right)

                push = True

            if push:
                if node_left.s != node_left.t:
                    node_queue.push(node_left)
                if node_right.s != node_right.t:
                    node_queue.push(node_right)
        return
    
    def compute_eisner_matrix(self, sent, arc_weight, cube_prunning):
        cdef int m, s, t
        for m from 1 <= m < self.n by 1: 
            for s from 0 <= s < self.n by 1:
                t = s + m
                if t >= self.n:
                    break
                self.combine_triangle(t, s, arc_weight, sent, cube_prunning)
                self.combine_triangle(s, t, arc_weight, sent, cube_prunning)
                self.combine_left(s, t, arc_weight, sent, cube_prunning)
                self.combine_right(s, t, arc_weight, sent, cube_prunning)


    def parse(self, sent, arc_weight):	
        self.n = len(sent.word_list)
        self.init_eisner_matrix(3)

        #self.compute_eisner_matrix(sent, arc_weight, 0)
        self.compute_eisner_matrix(sent, arc_weight, 1)

        self.get_edge_list()       
        self.delete_eisner_matrix()

        return self.edge_list
        
