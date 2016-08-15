# DataPool

###### API Version: 1.0.0
###### Edit: 2016-08-01 10:46, Jetic Gu

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
format_list.	| `str` or `list`		|  					| Specify the format file or format list. If the given object is of `str` type it will be treated as a file URI. For specifications of a format file, refer to Format Specs. | "format/conllu.format"; "format/conllx.format"; "format/penn2malt.format"; ["ID", "FORM", "LEMMA"]
prep_path		| `str`					| "data/prep/"		| Specify the path which the temp files will be created. The default URI prefix is "hdfs://" | "/tmp/nlp-toolkit"
shards			| `int`					| 1					| Specify the number of shards. This option is often used when you want to use the data in parallel training or evaluation. | 8
sparkContext	| `pyspark.context.SparkContext` | None		| Specify the SparkContext object. If data pool somehow acquire access to HDFS, this option will be mandatory.	| sc
hadoop			| `bool`				| `False`			| If the value is `True`, the temp data will be created in HDFS, if not it will be created in local directory.	| `True`; `False`
comment_sign	| `str`					| None				| Sign of comment in the text. If the comment_sign matches the first word of the line, the line will be ignored. If the comment sign is specified in the format file the comment sign here will be ignored.	| "##"; ""
textString		| `unicode`				| None				| The text which contains the data. For format refer to Format Specs.	| sc.textFile("example.txt").first()

##### 2.2 Declaration

There are two ways of declaring a `DataPool` object, you can either create from specific file or from text.

#### 2.2.1 Create from file

You can create a `DataPool` which reads all its data from files. The file could be located in HDFS(Hadoop File System) or a local directory.

	dp = DataPool(fgen        = 'english_1st_fgen',
                  format_list = 'format/conllx.format',
                  data_regex  = 'dataFile[0-9].conll|dataFile1[0-9].conll',
                  data_path   = 'file:///natlang-data/')

#### 2.2.2 Create from text:

You can create a `DataPool` from existing text.

	dp = DataPool(fgen         = 'english_1st_fgen',
                  format_list  = format_list,
                  textString   = text,
                  comment_sign = comment_sign)

### 3. Package Attributes

##### data\_pool.\_\_version\_\_
The version of DataPool API

### 4. Instance Attributes

##### dataPool.format\_list

> Type: `list`

> Description: A list of all the column names read from format file. For more information, refer to Format Specs

##### dataPool.fgen

> Type: `classobj`

> Description: The feature generator class of this instance

##### dataPool.comment\_sign

> Type: `str`

> Description: The comment sign of the data of this instance. Lines started with comment sign will be ignored.

### 5. Methods

##### dataPool.loadedPath()

> Return type: `str`

> Description: This method returns the location of the loaded data in temp folder.

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
                  format_list = 'format/conllx.format',
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
                  format_list  = 'format/conllx.format',
                  data_regex   = 'example.txt',
                  data_path    = 'hdfs://master:2333/data/natlang-data/', # Notice in HDFS, DataPool only scans
                                                                           # subdirectories
                  shardNum     = 8,
                  sparkContext = sc,
                  hadoop       = True)

    def create_dp(textString, fgen, format, comment_sign):
        return DataPool(fgen         = fgen,
                        format_list  = format,
                        textString   = textString[1],
                        comment_sign = comment_sign)

    spark_dp = sc.wholeTextFiles(dp.loadedPath(), minPartitions=dp.shardNum).cache()

    spark_dp = spark_dp.map(lambda t: create_dp(textString   = t,
                                                fgen         = dp.fgen,
                                                format       = dp.format_list,
                                                comment_sign = dp.comment_sign)).cache()

    # do_your_mapreduce_stuff_here
