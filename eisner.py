# -*- coding: utf-8 -*-
import copy

class EisnerParser():
    """
    An Eisner parsing algorithm implementation
    """
    
    def __init__(self,sentence=""):
        # Default is empty string or a list
        if isinstance(sentence,str):
            self.sentence_list = sentence.split()
        else:
            self.sentence_list = sentence
        return

    def __add__(self,op2):
        return EsinerParser(self.sentence_list + op2.sentence_list)
        
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
        e1 = [copy.deepcopy((0,set([]))) for i in range(2)]
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
    

    def parse(self,arc_weight,sentence=None):
        """
        Implementation of Eisner Algorithm using dynamic programming table
        
        :param sent: The list of input words that constitute a sentence.
        :type sent: list
        :param arc_weight: A scoring function that gives scores to edges
        :type arc_weight: function(head_node,child_node)

        :return: The maximum score of the dependency structure as well as all edges
        :rtype: tuple(integer,list(tuple(integer,integer)))
        """

        if sentence == None:
            sent = self.sentence_list
        elif isinstance(sentence,list):
            sent = sentence
        elif isinstance(sentence,str):
            sent = sentence.split()
        else:
            raise TypeError("""parser() only supports string, list or a
                               default None argument.""")
        print sent
        # n is the length of the sentence including the artificial ROOT
        n = len(sent)
        e = self.init_eisner_matrix(n)
        for m in range(1, n):
            for s in range(0, n):
                t = s + m
                if t >= n:
                    break
            
                e[s][t][0][1] = max([
                    (e[s][q][1][0][0] + e[q+1][t][0][0][0] + arc_weight((t,s)),
                     e[s][q][1][0][1].union(e[q+1][t][0][0][1]).union(set([(t,s)])))
                    for q in range(s, t)
                    ])
            
                e[s][t][1][1] = max([
                    (e[s][q][1][0][0] + e[q+1][t][0][0][0] + arc_weight((s,t)),
                     e[s][q][1][0][1].union(e[q+1][t][0][0][1]).union(set([(s,t)])))
                    for q in range(s, t)
                    ])
            
                e[s][t][0][0] = max([
                    (e[s][q][0][0][0] + e[q][t][0][1][0],
                     e[s][q][0][0][1].union(e[q][t][0][1][1]))
                    for q in range(s, t)
                    ])
            
                e[s][t][1][0] = max([
                    (e[s][q][1][1][0] + e[q][t][1][0][0],
                     e[s][q][1][1][1].union(e[q][t][1][0][1]))
                    for q in range(s+1, t+1)
                    ])
                #print s, t
        self.store_parsed_result(e[0][n - 1][1][0])
            
        return e[0][n - 1][1][0]
    
