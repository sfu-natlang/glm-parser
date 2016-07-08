
# Cube Pruning Eisner Parser Design Doc                                                                                     

The cube pruning approach is similar to the methods described in the following paper:                                                    
* Hao Zhang; Ryan McDonald. [Enforcing Structural Diversity in Cube-pruned Dependency Parsing](http://www.aclweb.org/anthology/P/P14/P14-2107.pdf). EMNLP 2014. 
* Hao Zhang; Ryan McDonald. [Generalized Higher-Order Dependency Parsing with Cube Pruning](http://www.aclweb.org/anthology/D/D12/D12-1030.pdf)                                                                                     
* Hao Zhang; Liang Huang; Kai Zhao; Ryan McDonald. [Online Learning for Inexact Hypergraph Search](http://www.aclweb.org/anthology/D/D13/D13-1093.pdf). [attachment](http://www.aclweb.org/anthology/attachments/D/D13/D13-1093.Attachment.pdf)                                                                                                       

## Design                                                                                                         

Each parsing state will have a parsing history(possible parsing sub trees). We combine two parsing state using cube-pruning to prune out the subtrees that are not likely to appear in the optimal result. In other words, each spam will generate a best-of-k subtrees of that spam. After filling out the whole eisner matrix, 
a forest of possible parsing trees will be generated.          

### Data Structure
The basic chart element is `EisnerHeap`, which stores the state information of one specific chart location. The Eisner matrix is a n by n two-dimentional array of `EisnerHeap`

#### `EisnerHeap` member  

* `bestK`: Specify the number of parsing histories(sub trees), the size of `buf`  
* `cube`: Three dimensional array [n][k][k], used in cube-pruning stage to color the search history of cube pruning  
* `buf`: Array of `bestK` number of possible sub trees in descending order in terms of root score 
* `heap`: heap structure used in cube pruning stage
* `state`: a tuple containing state information, (head, depend, direction, shape)
 

### Pseudocode
``` 
Parse(sentence, arc_weight):
	for m in (1, n):
		for s in (0, n):
			t = s + m
            for q in (s, t):
                score = calculate the score of merging C[s][q][1][0].buf[0] and C[q][t][0][0].buf[0]
                push (score, 0, 0) into heap
                top_score = Explore(heap, s, q, t, 0, 1)
                if top_score > C[s][q][0][1].buf[0].score:
                    c[s][q][0][1].buf[0] = {'score':top_score, 'feature_signature':t}

                score = calculate the score of merging C[s][q][1][0].buf[0] and C[q][t][0][0].buf[0]
                push (score, 0, 0) into heap
                top_score = Explore(heap, s, q, t, 1, 1)
                if top_score > C[s][q][1][1].buf[0].score:
                    c[s][q][1][1].buf[0] = {'score':top_score, 'feature_signature':t}

                score = calculate the score of merging C[s][q][0][0].buf[0] and C[q][t][0][1].buf[0]
                push (score, 0, 0) into heap
                top_score = Explore(heap, s, q, t, 0, 0)
                C[s][t][0][0].buf.append({'score':top_score, 'feature_signature':q})

                score = calculate the score of merging C[s][q][1][1].buf[0] and C[q][t][1][0].buf[0]
                push (score, 0, 0) into heap
                top_score = Explore(heap, s, q, t, 1, 0)
                C[s][t][1][0].buf.append({'score':top_score, 'feature_signature':q})

            sort C[s][t][0][0].buf, keep the k node with the highest score
            sort C[s][t][1][0].buf, keep the k node with the highest score

Explore(heap, s, q, t, dir, shape):
    top_score = -Inf

    for i in range (0, k):
        if heap is empty:
            break

        cell = heap.pop()   # cell: [score, left_index, right_index]
        if cell[0] > top_score:
            top_score = cell[0]

        # neighbors
        for (i, j) in [(cell[1]-1, cell[2]), (cell[1], cell[2]-1), (cell[1]+1, cell[2]), (cell[1], cell[2]+1)]:
            if (i, j) is in range:
                find node N1 as C[s][q][dir|shape][!dir & !shape].buf[i], node N2 as C[q][t][!shape & dir][!shape & dir].buf[j]
        calculate the score of neighboring cells
        push neighboring cells into heap

    heap.empty()
    return top_score
```

![cube_pruning](cube_pruning.png) 
