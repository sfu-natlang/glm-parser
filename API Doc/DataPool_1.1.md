# DataPool

###### API Version: 1.1
###### Edit: 2016-12-09 12:20, Jetic Gu

### 0. New Features (comparing with 1.0)

This version of DataPool API is based on version 1.1. It involves changes in
the way DataPool handles different formats and the following new features:

* Added the ability to export a DataPool to a file.
* Added the ability to merge two DataPools.

### 1. Description

`DataPool` is the data storage device used in SFU Natural Language Toolkit. All the data are stored in the `DataPool` object, and accessed through `DataPool`.

`DataPool` doesn't provide a random access method, instead it uses an index which goes though the entire `DataPool`.

#### 1.1 Import

	from data.data_pool import DataPool

### 2. Parameters and Declaration

##### 2.1 Parameters

Parameter		|	Type				|	Default Value	|	Description	|	Examples
----------------|-----------------------|-------------------|---------------|------------
data\_regex		| `str`					|	""				|	Specify the name of the data file you wish to load from	| "wsj_0[0-2][0-9][0-9].mrg.3.pa.gs.tab"
data\_path		| `str`					| "./penn-wsj-deps/"| Specify the location of the data file you wish to load. If the data path refers to a local directory, the directory and its subdirectories will be searched from the data file, in Hadoop only the subdirectories will be scanned. The default URI prefix is "hdfs://" 	| "file:///natlang-data/"; "hdfs://data/natlang-data/"
fgen			| `str` or `classobj`	|  					| Specify the feature generator for the `DataPool`. If the given object is an instance of `str`, `DataPool` will search `feature` folder for a file that matches, and use the `FeatureGenerator` class inside. If the given object is an instance of `classobj`, it will use that class as feature generator. To write a customised feature generator, refer to the feature generator API.	| "english\_1st\_fgen"; "pos\_fgen"; feature.pos\_fgen.FeatureGenerator
data_format.	| `str` or `DataFormat`	|  					| Specify the name of the format or an data_format instance. The source code of supported formats are under `src/data/data_format` | "conllu"; "conllx"; "penn2malt"
prep_path		| `str`					| "data/prep/"		| Specify the path which the temp files will be created. The default URI prefix is "hdfs://" | "/tmp/nlp-toolkit"
shards			| `int`					| 1					| Specify the number of shards. This option is often used when you want to use the data in parallel training or evaluation. | 8
sparkContext	| `pyspark.context.SparkContext` | None		| Specify the SparkContext object. If data pool somehow acquire access to HDFS, this option will be mandatory.	| sc
hadoop			| `bool`				| `False`			| If the value is `True`, the temp data will be created in HDFS, if not it will be created in local directory.	| `True`; `False`
textString		| `unicode`				| None				| The text which contains the data. For format refer to Format Specs.	| sc.textFile("example.txt").first()

##### 2.2 Declaration

There are two ways of declaring a `DataPool` object, you can either create from specific file or from text.

#### 2.2.1 Create from file

You can create a `DataPool` which reads all its data from files. The file could be located in HDFS(Hadoop File System) or a local directory.

	dp = DataPool(fgen        = 'english_1st_fgen',
                  data_format = 'conllx',
                  data_regex  = 'dataFile[0-9].conll|dataFile1[0-9].conll',
                  data_path   = 'file:///natlang-data/')

#### 2.2.2 Create from text:

You can create a `DataPool` from existing text.

	dp = DataPool(fgen         = 'english_1st_fgen',
                  data_format  = "conllx",
                  textString   = text)

### 3. Package Attributes

##### data\_pool.\_\_version\_\_
The version of DataPool API

### 4. Instance Attributes

##### dataPool.data_format

> Type: `DataFormat`

> Description: the `DataFormat` instance used in this `DataPool` instance

##### dataPool.fgen

> Type: `classobj`

> Description: The feature generator class of this instance

### 5. Methods

##### dataPool.loadedPath()

> Return type: `str`

> Description: This method returns the location of the loaded data in temp folder.

##### dataPool.export(fileURI, sparkContext=None)

> `fileURI` type: `str`

> `sparkContext` type: `pyspark.context.SparkContext`

> Description: This method exports the `DataPool` instance to the `fileURI`.

##### dataPool.__add__(another_data_pool)

> `another_data_pool` type: `DataPool`

> Return type: `DataPool`

> Description: This method merges the two `DataPool`s by attaching `another_data_pool`'s data to the end and return the result.

##### dataPool.reset\_index()

> Description: reset dataPool index to the very beginning.

##### dataPool.has\_next\_data()

> Return type: `bool`

> Description: If the index has reached the bottom, return `False`, which means there are no data left to retrieve. Else, return `True`. This method doesn't modify the index, nor retrieve the data. To retrieve the data, see method `dataPool.get_next_data()`

##### dataPool.get\_next\_data()

> Return type: `instance` of `Sentence`

> Description: This method returns the data instance of current index and increase index by 1.

##### dataPool.get\_sent\_num()

> Return type: `int`

> Description: Return the number of sentences in `dataPool`

### 6. Examples

#### Scenario 1: Processing sentences in a CoNLLX formatted text file on local hard drive

In this case, assume the actual file is `example.txt` located under `/data/natlang-data/example/`. We are going to use first order feature generator for English in this example (`feature/english_1st_fgen.py`)

	dp = DataPool(fgen        = 'english_1st_fgen',
                  data_format = 'conllx',
                  data_regex  = 'example.txt',
                  data_path   = 'file:///data/natlang-data/example/',)

    while dp.has_next_data():
        sentence = dp.get_next_data()

        # do_your_stuff_here

    dp.reset_index() # don't forget to reset the index

#### Scenario 2: Processing sentences in a CoNLLX formatted text file on HDFS and do something on each shard

Assume the actual file is `example.txt` located under `hdfs://master:2333/data/natlang-data/example/`. We are going to use first order feature generator for English in this example (`feature/english_1st_fgen.py`), and create the temp files in HDFS.

To support parallel operation, we are going to use more than 1 shard, say 8 shards. After creating the `DataPool` instance, it cannot be used in spark yet. We'll need to load it with RDD.

	dp = DataPool(fgen         = 'english_1st_fgen',
                  data_format  = 'conllx',
                  data_regex   = 'example.txt',
                  data_path    = 'hdfs://master:2333/data/natlang-data/', # Notice in HDFS, DataPool only scans
                                                                           # subdirectories
                  shardNum     = 8,
                  sparkContext = sc,
                  hadoop       = True)

    def create_dp(textString, fgen, data_format):
        return DataPool(fgen         = fgen,
                        data_format  = data_format,
                        textString   = textString[1])

    spark_dp = sc.wholeTextFiles(dp.loadedPath(), minPartitions=dp.shardNum).cache()

    spark_dp = spark_dp.map(lambda t: create_dp(textString   = t,
                                                fgen         = dp.fgen,
                                                data_format  = dp.data_format,
                                                comment_sign = dp.comment_sign)).cache()

    # do_your_mapreduce_stuff_here
