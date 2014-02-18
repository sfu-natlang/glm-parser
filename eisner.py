# -*- coding: utf-8 -*-

def ini_eisner_matrix(n):
    e1 = [(0,set([])) for i in range(2)]
    e2 = [e1 for i in range(2)]
    e3 = [e2 for i in range(n)]
    e4 = [e3 for i in range(n)]
    return e4

def eisner(sent, arc_weight):
    """function to run eisner algorithm
    and return the maximum eisner score and the corresponding tree"""
    n = len(sent)+1
    e = ini_eisner_matrix(n)
    for m in range(1, n):
        for s in range(0, n):
            t = s + m
            if t >= n:
                break
            
            e[s][t][0][1] = max([
                (e[s][q][1][0][0] + e[q+1][t][0][0][0] + arc_weight(sent[t], sent[s]),
                 e[s][q][1][0][1].union(e[q+1][t][0][0][1]))
                for q in range(s, t)
                ])
            e[s][t][1][1] = max([
                (e[s][q][1][0][0] + e[q+1][t][0][0][0] + arc_weight(sent[s], sent[t]),
                 e[s][q][1][0][1].union(e[q+1][t][0][0][1]))
                for q in range(s, t)
                ])
            e[s][t][0][0] = max([
                (e[s][q][0][0][0] + e[q][t][0][1][0],
                 e[s][q][0][0][1].union(e[q][t][0][1][1]))
                for q in range(s, t)
                ])
            e[s][t][1][0] = max([
                (e[s][q][1][1][0] + e[q][t][1][0][0],
                 e[s][q][1][1][1].union(e[q][t][1][0][1))
                for q in range(s+1, t+1)
                ])
            
    return e[0][n][1][0]
    
