# Getting Started

Currently training the model is done using the averaged perceptron algorithm. This is an online algorithm, which means that it updates the weight vector one example at a time. It does iterate through the entire data multiple times. Each pass through the data is called an epoch.

The parser uses training, dev and test data in the CoNLL format for training and evaluation.

Searching for the argmax tree when given a fixed weight vector is done using the Eisner dependency parsing algorithm. 

## Learn the basics

First teach yourself the basics of parsing and machine learning for NLP.

### Step 1: learn about dependency parsing

Read the slides from the following tutorial to learn about dependency parsing and in particular read the explanation of the Eisner algorithm in the [graph-based parsing slides](http://stp.lingfil.uu.se/~nivre/docs/eacl2.pdf).

* [Recent Advanced in Dependency Parsing](http://stp.lingfil.uu.se/~nivre/eacl14.html). Ryan McDonald and Joakim Nivre. Tutorial at EACL 2014.

Then read upto the chapter on Graph-based parsing in the following book:

* [Dependency Parsing](https://books.google.ca/books?id=BYFgAQAAQBAJ). Sandra Kubler, Ryan McDonald and Joakim Nivre. Morgan & Claypool Publishers, 2009. [SFU Library link](http://www.morganclaypool.com.proxy.lib.sfu.ca/doi/abs/10.2200/S00169ED1V01Y200901HLT002)

A lot of useful information about first-order projective parsing is in Ryan McDonald's PhD thesis:

* [Discriminative Training and Spanning Tree Algorithms for Dependency Parsing](http://www.ryanmcd.com/papers/thesis.pdf). Ryan McDonald PhD thesis. 2006.

## Step 2: learn about structured prediction

The best way is to do the following homework. At the end of solving this homework you will know about structured prediction using the perceptron, the averaged perceptron. We apply similar algorithms to the task of parsing, part-of-speech tagging, etc.

* [Phrasal Chunking homework](http://anoopsarkar.github.io/nlp-class/hw2.html). from Anoop Sarkar's NLP course.

## Step 3: read the source

Ask Anoop for the latest development branch and start reading the source code. Especially the code in the `parse` and `learn` directories.

* [Github repository for this project](https://github.com/sfu-natlang/glm-parser/tree/merged_datapool_spark).

## More advanced material

### Higher order features

### Cube pruning

* Hao Zhang and Ryan McDonald. Generalized higher-order dependency parsing with cube pruning. EMNLP 2012.

More references in the [EACL 2014 tutorial slides](http://stp.lingfil.uu.se/~nivre/docs/eacl2.pdf) by McDonald and Nivre.

### Tree-adjoining grammar features

The dependencies between words are created using tree-adjoining grammar derivations where each word lexicalizes an elementary tree and a full sentence parse is the combination of these elementary trees.

* [TAG, Dynamic Programming and the Perceptron for Efficient, Feature-rich Parsing](http://www.cs.columbia.edu/~mcollins/papers/conll.final.pdf). Xavier Carreras, Michael Collins, and Terry Koo.  In Proceedings of CoNLL 2008. 

## Further reading

* Sabine Buchholz and Erwin Marsi. CoNLL-X shared task on multilingual dependency parsing. CoNLL 2006. 
* Wenliang Chen, Min Zhang, and Haizhou Li. Utilizing dependency language models for graph-based dependency parsing models. RANLP 2012. Workshop at ACL 2012.
* Keith Hall, Ryan McDonald, Jason Katz-Brown, and Michael Ringgaard.  Training dependency parsers by jointly optimizing multiple objectives. EMNLP 2011.
* Liang Huang, Suphan Fayong, and Yang Guo. Structured perceptron with inexact search. NAACL 2012.
* Terry Koo, Xavier Carreras, and Michael Collins. Simple semi-supervised dependency parsing. ACL 2008.
* Ryan McDonald and Joakim Nivre. Characterizing the errors of data-driven dependency parsing models. EMNLP-CoNLL 2007.
* Ryan McDonald and Fernando Pereira. Online learning of approximate dependency parsing algorithms. EACL 2006.
* J Nivre, J Hall, S Kubler, R McDonald, J Nilsson, S Riedel, and D Yuret. The CoNLL 2007 shared task on dependency parsing. CoNLL 2007.
* Liang Zhang, Huang, Kai Zhao, and Ryan McDonald. Online learning for inexact hypergraph search. EMNLP 2013.
* Alexander M Rush and Slav Petrov. Vine pruning for efficient multi-pass dependency parsing. NAACL-HLT 2012.
