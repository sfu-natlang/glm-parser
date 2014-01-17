glm-parser
==========

This project implements a parser for natural language that uses a general linear model over higher-order dependencies between words. Training the model is done using a (margin-aware) Perceptron algorithm. The dependencies between words are created using tree-adjoining grammar derivations where each word lexicalizes an elementary tree and a full sentence parse is the combination of these elementary trees. Search is done using the Eisner dependency parsing algorithm augmented with search over higher-order dependencies. The parser uses Penn Treebank style trees for training data.

Part of the system replicates the following paper:

Xavier Carreras, Michael Collins, and Terry Koo. 
TAG, Dynamic Programming and the Perceptron for Efficient, Feature-rich Parsing. 
In Proceedings of CONLL 2008.
http://www.cs.columbia.edu/~mcollins/papers/conll.final.pdf
