# How To Write An Evaluator

###### Evaluator Base API Version: 1.0.0
###### Edit: 2016-08-16 21:13, Jetic Gu

### 1. Description

`Evaluators` are located under `src/evaluate`, they are used to evaluate a specific weight vector on specific tasks. The reason why we want a unified evaluator API is simple, the evaluators functions similarly, each time it retrieves a `sentence` from the `dataPool`, use the weight vector to generate the result, and we compare the result with the gold result stored in the `sentence` object, so that we know how well the weight vector does.

### 2 EvaluatorBase Class

The `EvaluatorBase` class in located under `src/evaluate/__init__.py`, it contains everything an evaluator needs, except for the sentence evaluation part, which lies under your responsibility.

#### 2.1 Instance Attributes

An instance of `EvaluatorBase` has two instance attributes:

Name						|	Type		|	Initial Value	|	Description
----------------------------|---------------|-------------------|-------------------
evaluator.correct\_num		|	`int`		|	0				|	The number of correct results
evaluator.gold\_set\_size	|	`int`		|	0				|	The total number of entries

All of the methods, including evaluation and printing out results involves these two.

#### 2.2 Methods

##### sequentialEvaluate()

This method is used to perform sequential evaluation. The following are its parameters:

Parameters					|	Type												|	Default Value	|	Description		
----------------------------|-------------------------------------------------------|-------------------|-------------------
data_pool					|	`instance` of `data.data_pool.DataPool`				|					|	the data pool used for evaluation
w_vector					|	`instance` of `weight.weight_vector.WeightVector`	|					|	the weight vector to be evaluated
sentence_evaluator			|	`instancemethod`									|					|	the method used to evaluate a sentence. This is to be written by the user
sparkContext				|	`pyspark.context.SparkContext`						|	None			|	SparkContext
hadoop						|	`bool`												|	None			|	Running in yarn mode or not

##### parallelEvaluate()

This method is used to perform evaluation in parallel. The following are its parameters:

Parameters					|	Type												|	Default Value	|	Description		
----------------------------|-------------------------------------------------------|-------------------|-------------------
data_pool					|	`instance` of `data.data_pool.DataPool`				|					|	the data pool used for evaluation
w_vector					|	`instance` of `weight.weight_vector.WeightVector`	|					|	the weight vector to be evaluated
sentence_evaluator			|	`instancemethod`									|					|	the method used to evaluate a sentence. This is to be written by the user
sparkContext				|	`pyspark.context.SparkContext`						|	None			|	SparkContext
hadoop						|	`bool`												|	None			|	Running in yarn mode or not

#### 2.3 What is yet to be done?

Everything except for one part is already done for you, that is the `sentence_evaluator` method. You need to implement this in your own evaluator.

### 3 Your Evaluator

It is highly recommended that you put your own evaluator under `src/evaluate/` for convenience.

#### 3.1 What to import?

Every evaluator class needs to be the subclass of `EvaluatorBase`, therefore one must import `EvaluatorBase`:

	from evaluate import EvaluatorBase

In advance(this is optional but recommended), the evaluators in SFU Natlang Toolkit all uses loggers to handle the logs. One can simply import the logger for evaluators by:

	from evaluate import logger
	
#### 3.2 Required Methods

The most important method is the `sentence_evaluator`. Its interface is fixed as follow:

	name_of_the_evaluator(self, sent, w_vector)
	
The expected return value of the method is defined as follow:

	return correct_num, gold_set_size
	
where `correct_num` is the number of entries that the weight vector was able to produce correctly, while `gold_set_size` is the total number of entries.

Once the method has been implemented, add the following methods into your evaluator class:

	def sequentialEvaluate(self,
                           data_pool,
                           w_vector,
                           sparkContext=None,
                           hadoop=None):

        return EvaluatorBase.sequentialEvaluate(self,
                                                data_pool,
                                                w_vector,
                                                self.name_of_the_evaluator,
                                                sparkContext,
                                                hadoop)

    def parallelEvaluate(self,
                         data_pool,
                         w_vector,
                         sparkContext,
                         hadoop):

        return EvaluatorBase.parallelEvaluate(self,
                                              data_pool,
                                              w_vector,
                                              self.name_of_the_evaluator,
                                              sparkContext,
                                              hadoop)
                                              
#### 3.3 Usage

##### 3.3.1 Sequential Evaluation

Sequential evaluator simply goes through the `dataPool` and evaluate the `w_vector` with each `sentence`. Example code:

	evaluator = my_evaluator()
	evaluator.sequentialEvaluate(dataPool,
	                             w_vector)
	                             
##### 3.3.2 Parallel Evaluation

Evaluation in parallel is relatively similar, it divides the `dataPool` to several shards and goes through each one in parallel, and combine the results in the end. The number of shards is defined in `dataPool`.

	evaluator = my_evaluator()
	evaluator.sequentialEvaluate(dataPool,
	                             w_vector,
	                             sc)

### 4 Output

The evaluator will print out the evaluation results through logger. It looks something like this:

	20XX-XX-XX XX:XX:XX,XXX EVALUATOR [INFO]: Feature count: 668751
	20XX-XX-XX XX:XX:XX,XXX EVALUATOR [INFO]: Unlabelled accuracy: 0.811463184488 (26659, 32853)
	20XX-XX-XX XX:XX:XX,XXX EVALUATOR [INFO]: Unlabelled attachment accuracy: 0.818883593088 (28005, 34199)
	
Feature count is the size of the weight vector(number of entries).

Unlabelled accuracy = `correct_num` / `gold_set_size`

Unlabelled attachment accuracy = (`correct_num` + `number_of_sentences`) / (`gold_set_size` + `number_of_sentences`)