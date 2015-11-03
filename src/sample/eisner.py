# -*- coding: utf-8 -*-
import copy, time

class EisnerParser():
    """
    An Eisner parsing algorithm implementation
    """
    
    def __init__(self):
        return
        
    def init_eisner_matrix(self,n):
        """
        Initialize a dynamic programming table, i.e. e[0..n][0..n][0..1][0..1]

        :param n: The length of the sentence including the artificial ROOT
        :type n: integer

        :return: An initialized table with all chart entries being (0,[])
        :rtype: Multi-dimensional list
        """
        # CAUTION: Must use deepcopy() here, since Python uses the object
        # reference model, which will cause trouble if we use shared object
        # in the chart
        # The last dimenison of the table. It uses a tuple to store score
        # and edges of current stage
        e1 = [copy.deepcopy([0,[]]) for i in range(2)]
        # The dimension that specifies the direction of the edge
        e2 = [copy.deepcopy(e1) for i in range(2)]
        # The end of the span
        e3 = [copy.deepcopy(e2) for i in range(n)]
        # The start of the span
        e4 = [copy.deepcopy(e3) for i in range(n)]
        return e4

    def store_parsed_result(self,parsed_result):
        """
        Saves the parsed result into the instance

        :param parsed_result: The return value of parse()
        :type parsed_result: See parse()
        """
        self.max_score = parsed_result[0]
        self.edge_set = parsed_result[1]
        return
    

    def parse(self,n,arc_weight,sentence=None):
        """
        Implementation of Eisner Algorithm using dynamic programming table
        
        :param n: The number of input words that constitute a sentence.
        :type n: int
        :param arc_weight: A scoring function that gives scores to edges
        :type arc_weight: function(head_node,child_node)

        :return: The maximum score of the dependency structure as well as all edges
        :rtype: tuple(integer,list(tuple(integer,integer)))
        """
        #tt = 0;
        e = self.init_eisner_matrix(n)
        for m in range(1, n):
            for s in range(0, n):
                t = s + m
                if t >= n:
                    break
                #t1 = time.clock()
                weight = arc_weight(t,s)
                #tt += (time.clock() - t1)
                e[s][t][0][1][0], q_max = max(
                    [(e[s][q][1][0][0] + e[q+1][t][0][0][0] + weight, q)
                    for q in range(s, t)], 
                    key=lambda (a,c): a)
                e[s][t][0][1][1] =\
                    e[s][q_max][1][0][1] + e[q_max+1][t][0][0][1] + [(t,s)]
                
                
                #t1 = time.clock()
                weight = arc_weight(s,t)
                #tt += (time.clock() - t1)
                e[s][t][1][1][0], q_max = max(
                    [(e[s][q][1][0][0] + e[q+1][t][0][0][0] + weight, q)
                    for q in range(s, t)], 
                    key=lambda (a,c): a)
                e[s][t][1][1][1] =\
                    e[s][q_max][1][0][1] + e[q_max+1][t][0][0][1] + [(s,t)]
                
                
                e[s][t][0][0][0], q_max = max(
                    [(e[s][q][0][0][0] + e[q][t][0][1][0],q)
                    for q in range(s, t)], 
                    key=lambda (a,c): a)
                e[s][t][0][0][1] = e[s][q_max][0][0][1] + e[q_max][t][0][1][1]
                
                
                e[s][t][1][0][0], q_max = max(
                    [(e[s][q][1][1][0] + e[q][t][1][0][0], q)
                    for q in range(s+1, t+1)], 
                    key=lambda (a,c): a)
                e[s][t][1][0][1] = e[s][q_max][1][1][1] + e[q_max][t][1][0][1]
                #print s, t
                
        self.store_parsed_result(e[0][n - 1][1][0])
        #print "edge query time", tt    
        return set(e[0][n - 1][1][0][1])
    
