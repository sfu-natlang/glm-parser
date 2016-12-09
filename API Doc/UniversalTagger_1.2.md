# UniversalTagger

###### API Version: 1.2
###### Edit: 2016-12-09 12:20, Jetic Gu

### 0. New Features (comparing with 1.1)

This version of UniversalTagger API is based on version 1.1. It contains a few
minor bug fixes, support for the new DataPool interface(1.1), and also the
following new features:

* Added the ability to tag an entire DataPool and save it to a file.

#### 0.1 Import

### 1. Description

The universal tagger was renamed from the `PosTagger` version `1.0`, starting
from version `1.1` it will be able to handle more than just POS (Part of
Speech) tags. Note that the class `PosTagger` is now deprecated.

The universal tagger class `Tagger`, is one of the major components of SFU
Natlang Toolkit. The `PosTagger` class provides the ability to tag a sentence
with given weight vector, or perform training and evaluation.

#### 1.1 Import

	from universal_tagger import Tagger

#### 1.2 Compatible feature generators

The compatible feature generators provided in this toolkit are:

* `pos_fgen` for Part of Speech tagging.
* `ner_fgen` for Name Entity Recogniser tagging.

### 2. Methods

#### 2.1 \_\_init\_\_

Parameter				|	Type							|	Default Value		|	Description	|	Examples
------------------------|-----------------------------------|-----------------------|---------------|------------
weightVectorLoadPath	| `str`								| None					| Specify the location of the weight vector you wish to load. The default URI prefix is `"hdfs://"` 	| `"file://fv_Iter_5.db"`; `"hdfs://data/fv_Iter_5.db"`
tagger					| `str`								| "viterbi"				| Specify the name of the tagger you wish to use. | "viterbi"; "viterbi_pruning"
tagFile					| `int`								| "file://tagset.txt" 	| Specify the file containing all the tags you wish to use	|
sparkContext			| `pyspark.context.SparkContext`	| None					| Specify the SparkContext object. | sc

A sample tag file is provided in `src/tagset.txt`. Note that the default tag
will be the first item in the tag file.

#### 2.2 train

The purpose of this method is to train the weight vector. Every time, it loads
up a learner and perform machine learning. For specification of a learner,
please refer to the `Learner` documentation.

Sample code:

	tagger.train(dataPool     = dataPool,
		 	 	 maxIteration = 5,
		 	 	 learner      = 'average_perceptron')

In this case, `dataPool` is the `DataPool` instance that contains all the
training data. For specifications for `DataPool` class, please refer to the
`DataPool` documentation.

Should you wish to export the trained weight vector, one can use the following
parameters:

	tagger.train(dataPool             = dataPool,
		 	 	 maxIteration         = 5,
		 	 	 learner              = 'average_perceptron',
		 	 	 weightVectorDumpPath = './MY_W_VECTOR')

At the end of the each iteration, the trained weight_vector will be dumped
with `weightVectorDumpPath` as location and prefix. If one doesn't want it
dumped every iteration, one can also use the `dumpFrequency` parameter. See
full parameter list for more detail on the matter.

Should one wish to do the training in parallel, here's an example:

	tagger.train(dataPool     = dataPool,
				 maxIteration = 5,
				 learner      = 'average_perceptron',
                 parallel     = True,
                 sparkContext = sc)

Note that the number of shards is set in `dataPool`. Should one wish to perform
the training in yarn mode, one needs to use `hadoop=True` parameter.

Parameter				|	Type							|	Default Value		|	Description
------------------------|-----------------------------------|-----------------------|---------------
dataPool				| `instance` of `DataPool`			|						| `DataPool` object that contains all the training data.
maxIteration			| `int`								| 1						| Number of iterations of training.
learner					| `str`								| "average_perceptron"	| Specify the learner. For specifications of learners, refer to `Learner` documentation.
weightVectorDumpPath	| `str` or None						| None					| Specify the location and prefix of the weight vector you wish to dump.
dumpFrequency			| `int`								| 1						| Frequency of dumping weight vector. Default: dumping at the end of every iteration.
parallel				| `bool`							| False				 	| Perform training in parallel or not.
sparkContext			| `pyspark.context.SparkContext`	| None					| Specify the SparkContext object.
hadoop					| `bool`							| False					| Perform training in yarn mode or not.

#### 2.3 evaluate

The purpose of this method is to evaluate the weight vector.

Sample code:

	tagger.evaluate(dataPool)

For parallel evaluation:

	tagger.evaluate(dataPool,
			 		parallel=True,
			 	   	sparkContext=sc)

Note that the number of shards is set in `dataPool`. Should one wish to perform
the evaluation in yarn mode, one needs to use `hadoop=True` parameter.

Parameter				|	Type							|	Default Value		|	Description
------------------------|-----------------------------------|-----------------------|---------------
dataPool				| `instance` of `DataPool`			|						| `DataPool` object that contains all the evaluation data.
exportFileURI			| `str` or None						| None					| This option will disable parallel evaluation and export the tagged DataPool to a file
parallel				| `bool`							| False				 	| Perform evaluation in parallel or not.
sparkContext			| `pyspark.context.SparkContext`	| None					| Specify the SparkContext object.
hadoop					| `bool`							| False					| Perform evaluation in yarn mode or not.

#### 2.4 getTags

The purpose of this method is to tag a single sentence.

Sample code:

	tags = tagger.getTags(sentence)

`sentence` is an instance of `Sentence` class. The return value is a list of
tags.

### 3. Package Attributes

##### universal\_tagger.\_\_version\_\_
The version of Universal Tagger API

### 4. Instance Attributes

##### tagger.w_vector

`WeightVector` instance. The weight vector.

##### tagger.tagger

`Tagger` class used for tagging.

##### tagger.tagset

`list` of all the tags we are using, loaded from `tagFile`

##### tagger.default_tag

Default tag for unknown word. Default value is the first item in the tag file.
