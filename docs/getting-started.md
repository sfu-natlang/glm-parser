Getting Started
===============

Currently training the model is done using the averaged perceptron algorithm. This is an online algorithm, which means that it updates the weight vector one example at a time. It does iterate through the entire data multiple times. Each pass through the data is called an epoch.

The parser uses training, dev and test data in the CoNLL format for training and evaluation.

Searching for the argmax tree when given a fixed weight vector is done using the Eisner dependency parsing algorithm. 


Tree-adjoining grammar features
-------------------------------

The dependencies between words are created using tree-adjoining grammar derivations where each word lexicalizes an elementary tree and a full sentence parse is the combination of these elementary trees.

* Xavier Carreras, Michael Collins, and Terry Koo. TAG, Dynamic Programming and the Perceptron for Efficient, Feature-rich Parsing. In Proceedings of CoNLL 2008. 
    * http://www.cs.columbia.edu/~mcollins/papers/conll.final.pdf

