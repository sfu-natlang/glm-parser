# Learner

###### API Version: 1.0.0
###### Edit: 2016-08-18 20:20, Jetic Gu

### 1. Description

`Learner`s are the machine learning implementations for SFU Natlang Toolkit, we use them to perform trainings, they are one of the most important part of the project.
Currently, SFU Natlang Toolkit provides two learners: original `perceptron` and `averaged_perceptron`, each in two modes: `sequential_learn` and
`parallel_learn`.

#### 1.1 Import

	from learner.THE_LEARNER_YOU_WISH_TO_USE import Learner

Currently, there are three files under `src/learner`:

* averaged_perceptron.py
* perceptron.py
* perceptron_base.py

Note that only the first two can be used, while the third one is merely a base
class for the other two. If you wish to write your own perceptron learner,
please consider reading through `perceptron_base.py`.

### 2. Methods

##### 2.0 f_argmax

`f_argmax` is the function we use to generate our feature vector. It's
interface is fixed, and examples of `f_argmax` could be found in our
`src/glm_parser.py` and `src/pos_tagger.py`. The interface is fixed as follow:

 	f_argmax(w_vector, sentence)

What it means that one uses the current weight vector to process the sentence
to retrieve the result, and use the result to generate features. In the
original perceptron implementation, we call it the `local_feature_vector`, and
we update the weight vector each time by adding the difference between
`local_feature_vector` and `gold_feature_vector`.

##### 2.1 \_\_init\_\_

Parameter		|	Type						|	Default Value	|	Description
----------------|-------------------------------|-------------------|---------------
`w_vector`		| `instance` of `WeightVector`	|	None			|	The initial weight vector for training

##### 2.2 sequential_learn

This method is used to perform sequential learning. An example is provided as
follow:

	learner.sequential_learn(f_argmax,
		                     data_pool,
							 iterations=3)

For introduction to `f_argmax` see section 2.0 of the present document.
`data_pool` is the `DataPool` instance that contains the training data.

Should one wish to export the trained `WeightVector`, one can add the following
parameters to do just the thing:

	learner.sequential_learn(f_argmax,
							 data_pool,
							 iterations=3,
							 d_filename='./My_Weight_Vector')

Under this setting, the `learner` will dump the `WeightVector` at the end of
every iteration. Should one wish to change that, say once per two iterations,
one could use `dump_freq` parameter:

	learner.sequential_learn(f_argmax,
							 data_pool,
							 iterations=3,
							 d_filename='./My_Weight_Vector'
							 dump_freq=2)

Note that the `WeightVector` of the final iteration will be dumped no matter what values is given to `dump_freq`.

A complete list of parameters:

Parameter		|	Type					| Default Value |	Description
----------------|---------------------------|---------------|---------------
`f_argmax`		| `function`				|				| See section 2.0 for detail
`data_pool`		| `instance` of `DataPool`	|				| The `DataPool` instance that contains training data. See `DataPool` documentation for more information
`iterations`	| `int`						| 1				| Number of iterations
`d_filename`	| `str`						| None			| Location and prefix of the `WeightVector` to be dumped. For example, `"file://./MY_W_VECTOR"`
`dump_freq`		| `int`						| 1				| Frequency of dumping `WeightVector`. For example given value 3, it dumps every 3 iterations plus the final iteration.

This method returns the trained `WeightVector` object.


##### 2.3 parallel_learn

This method is used to perform parallel learning. An example is provided as
follow:

	learner.parallel_learn(f_argmax,
		                   data_pool,
						   iterations=3,
						   sparkContext=sc)

For introduction to `f_argmax` see section 2.0 of the present document.
`data_pool` is the `DataPool` instance that contains the training data.
`sparkContext` is the `instance` of `SparkContext` needed for using spark.

Should one wish to export the trained `WeightVector`, the additional
parameters are the same with those described in section 2.2 of the present
document.

A complete list of parameters:

Parameter		|	Type					| Default Value |	Description
----------------|---------------------------|---------------|---------------
`f_argmax`		| `function`				|				| See section 2.0 for detail
`data_pool`		| `instance` of `DataPool`	|				| The `DataPool` instance that contains training data. See `DataPool` documentation for more information
`iterations`	| `int`						| 1				| Number of iterations
`d_filename`	| `str`						| None			| Location and prefix of the `WeightVector` to be dumped. For example, `"file://./MY_W_VECTOR"`
`dump_freq`		| `int`						| 1				| Frequency of dumping `WeightVector`. For example given value 3, it dumps every 3 iterations plus the final iteration.
`sparkContext`	| `pyspark.context.SparkContext` | None				| Specify the SparkContext object. This is mandatory
`hadoop`		| `bool`					| False			| Running in yarn mode or not

This method returns the trained `WeightVector` object.

##### 2.3 export

Export the trained weight vector. This method has no additional attributes.

Usage:

		DESTINY = learner.export()

### 3. Package Attributes

##### learner.perceptron_base.\_\_version\_\_
The version of learner API
