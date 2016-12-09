# GlmParser

###### API Version: 1.1
###### Edit: 2016-12-09 12:20, Jetic Gu

### 0. New Features (comparing with 1.0)

This version of GlmParser API is based on version 1.1. It contains a few
minor bug fixes, support for the new DataPool interface(1.1), and also the
following new features:

* Added the ability to parse an entire DataPool and save it to a file.

### 1. Description

`GlmParser` stands for Global Linear Model Parser, it is one of the major
components of SFU Natlang Toolkit. The `GlmParser` class provides the ability
to parse a sentence with given weight vector, or perform training and
evaluation.

#### 1.1 Import

	from glm_parser import GlmParser

### 2. Methods

#### 2.1 \_\_init\_\_

Parameter				|	Type							|	Default Value		|	Description	|	Examples
------------------------|-----------------------------------|-----------------------|---------------|------------
weightVectorLoadPath	| `str`								| None					| Specify the location of the weight vector you wish to load. The default URI prefix is `"hdfs://"` 	| `"file://fv_Iter_5.db"`; `"hdfs://data/fv_Iter_5.db"`
parser					| `str`								| "ceisner"				| Specify the name of the parser you wish to use. | "ceisner"; "eisner"
sparkContext			| `pyspark.context.SparkContext`	| None					| Specify the SparkContext object. | sc


#### 2.2 train

The purpose of this method is to train the weight vector. Every time, it loads
up a learner and perform machine learning. For specification of a learner,
please refer to the `Learner` documentation.

Sample code:

	glmParser.train(dataPool     = dataPool,
		 	 		maxIteration = 5,
		 	 		learner      = 'average_perceptron')

In this case, `dataPool` is the `DataPool` instance that contains all the
training data. For specifications for `DataPool` class, please refer to the
`DataPool` documentation.

Should you wish to export the trained weight vector, one can use the following
parameters:

	glmParser.train(dataPool             = dataPool,
		 	 		maxIteration         = 5,
		 	 		learner              = 'average_perceptron',
		 	 		weightVectorDumpPath = './MY_W_VECTOR')

At the end of the each iteration, the trained weight_vector will be dumped
with `weightVectorDumpPath` as location and prefix. If one doesn't want it
dumped every iteration, one can also use the `dumpFrequency` parameter. See
full parameter list for more detail on the matter.

Should one wish to do the training in parallel, here's an example:

	glmParser.train(dataPool     = dataPool,
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

	glmParser.evaluate(dataPool)

For parallel evaluation:

	glmParser.evaluate(dataPool,
			 		   parallel=True,
			 	   	   sparkContext=sc)

In the event one wishes to use a trained tagger to do the tagging, one can use
the following code:

	glmParser.evaluate(dataPool,
				   	   tagger=posTagger)

Note that the tagger must be loaded with a trained tagger weight vector. For
details on the matter, refer to the documentation on `PosTagger`

Parameter				|	Type							|	Default Value		|	Description
------------------------|-----------------------------------|-----------------------|---------------
dataPool				| `instance` of `DataPool`			|						| `DataPool` object that contains all the evaluation data.
tagger					| `instance` of `PosTagger`			| None					| `PosTagger` object that contains a trained tagger weight vector.
exportFileURI			| `str` or None						| None					| This option will disable parallel evaluation and export the parsed DataPool to a file
parallel				| `bool`							| False				 	| Perform evaluation in parallel or not.
sparkContext			| `pyspark.context.SparkContext`	| None					| Specify the SparkContext object.
hadoop					| `bool`							| False					| Perform evaluation in yarn mode or not.

#### 2.4 getEdgeSet

The purpose of this method is to parse a single sentence.

Sample code:

	edge_set = glmParser.getEdgeSet(sentence)

`sentence` is an instance of `Sentence` class. The return value is the edge
set.

### 3. Package Attributes

##### glm\_parser.\_\_version\_\_
The version of GLM Parser API

### 4. Instance Attributes

##### glmParser.w_vector

`WeightVector` instance. The weight vector.

##### glmParser.parser

`Tagger` class used for tagging.

##### glmParser.tagger

`PosTagger` instance for tagger during evaluation.
