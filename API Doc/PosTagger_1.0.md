# PosTagger

###### API Version: 1.0
###### Edit: 2016-08-19 18:39, Jetic Gu

### 1. Description

`PosTagger` stands for Part of Speech Tagger, it is one of the major components
of SFU Natlang Toolkit. The `PosTagger` class provides the ability to tag a
sentence with given weight vector, or perform training and evaluation.

#### 1.1 Import

	from pos_tagger import PosTagger

### 2. Methods

#### 2.1 \_\_init\_\_

Parameter				|	Type							|	Default Value		|	Description	|	Examples
------------------------|-----------------------------------|-----------------------|---------------|------------
weightVectorLoadPath	| `str`								| None					| Specify the location of the weight vector you wish to load. The default URI prefix is `"hdfs://"` 	| `"file://fv_Iter_5.db"`; `"hdfs://data/fv_Iter_5.db"`
tagger					| `str`								| "viterbi"				| Specify the name of the tagger you wish to use. | "viterbi"; "viterbi_pruning"
tagFile					| `int`								| "file://tagset.txt" 	| Specify the file containing all the tags you wish to use	|
sparkContext			| `pyspark.context.SparkContext`	| None					| Specify the SparkContext object. | sc

A sample tag file is provided in `src/tagset.txt`.

#### 2.2 train

The purpose of this method is to train the weight vector. Every time, it loads
up a learner and perform machine learning. For specification of a learner,
please refer to the `Learner` documentation.

Sample code:

	posTagger.train(dataPool     = dataPool,
		 	 		maxIteration = 5,
		 	 		learner      = 'average_perceptron')

In this case, `dataPool` is the `DataPool` instance that contains all the
training data. For specifications for `DataPool` class, please refer to the
`DataPool` documentation.

Should you wish to export the trained weight vector, one can use the following
parameters:

	posTagger.train(dataPool             = dataPool,
		 	 		maxIteration         = 5,
		 	 		learner              = 'average_perceptron',
		 	 		weightVectorDumpPath = './MY_W_VECTOR')

At the end of the each iteration, the trained weight_vector will be dumped
with `weightVectorDumpPath` as location and prefix. If one doesn't want it
dumped every iteration, one can also use the `dumpFrequency` parameter. See
full parameter list for more detail on the matter.

Should one wish to do the training in parallel, here's an example:

	posTagger.train(dataPool     = dataPool,
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

	posTagger.evaluate(dataPool)

For parallel evaluation:

	posTagger.evaluate(dataPool,
			 		   parallel=True,
			 	   	   sparkContext=sc)

Note that the number of shards is set in `dataPool`. Should one wish to perform
the evaluation in yarn mode, one needs to use `hadoop=True` parameter.

Parameter				|	Type							|	Default Value		|	Description
------------------------|-----------------------------------|-----------------------|---------------
dataPool				| `instance` of `DataPool`			|						| `DataPool` object that contains all the evaluation data.
parallel				| `bool`							| False				 	| Perform evaluation in parallel or not.
sparkContext			| `pyspark.context.SparkContext`	| None					| Specify the SparkContext object.
hadoop					| `bool`							| False					| Perform evaluation in yarn mode or not.

#### 2.4 getTags

The purpose of this method is to tag a single sentence.

Sample code:

	tags = posTagger.getTags(sentence)

`sentence` is an instance of `Sentence` class. The return value is a list of
tags.

### 3. Package Attributes

##### pos\_tagger.\_\_version\_\_
The version of POS Tagger API

### 4. Instance Attributes

##### posTagger.w_vector

`WeightVector` instance. The weight vector.

##### posTagger.tagger

`Tagger` class used for tagging.

##### posTagger.tagset

`list` of all the tags we are using, loaded from `tagFile`

##### posTagger.default_tag

Default tag for unknown word. Default value is `"NN"`
