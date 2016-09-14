# DataPrep

###### API Version: 1.0.0
###### Edit: 2016-08-16 19:24, Jetic Gu

### 1. Description

`DataPrep` is the data loading device used in SFU Natural Language Toolkit.
Normally, `DataPool` sends `DataPrep` the information of the data to be loaded,
and `DataPrep` reads all the data and create temporary files for `DataPool` to
use.

#### 1.1 Import

	from data.data_prep import DataPrep

### 2. Parameters and Declaration

##### 2.1 Parameters

Parameter		|	Type							|	Default Value	|	Description	|	Examples
----------------|-----------------------------------|-------------------|---------------|------------
dataURI			| `str`								| 					| Specify the location of the data file you wish to load. If the data path refers to a local directory, the directory and its subdirectories will be searched from the data file, in Hadoop only the subdirectories will be scanned. The default URI prefix is "hdfs://" 	| "file:///natlang-data/"; "hdfs://data/natlang-data/"
dataRegex		| `str`								|					| Specify the name of the data file you wish to load from	| "wsj_0[0-2][0-9][0-9].mrg.3.pa.gs.tab"
shardNum		| `int`								|  					| Specify Number of shards. Value has to be greater than 0	| "english\_1st\_fgen"; "pos\_fgen"; feature.pos\_fgen.FeatureGenerator
targetPath		| `str`								|  					| Specify the location of the tmp files. | "./data/prep"
sparkContext	| `pyspark.context.SparkContext`	| None				| Specify the SparkContext object. If data pool somehow acquire access to HDFS, this option will be mandatory.	| sc

##### 2.2 Declaration

	dataPrep = DataPrep(dataURI      = "file:///natlang-data/",
                        dataRegex    = "dataFile[0-9].conll|dataFile1[0-9].conll",
                        shardNum     = 1,
                        targetPath   = "./data/prep",
                        sparkContext = sc)

### 3. Package Attributes

##### data\_prep.\_\_version\_\_
The version of DataPrep API

### 4. Instance Attributes

No instance attributes for this class.

### 5. Methods

##### dataPrep.loadLocal()

> Return type: `str`

> Description: This method loads the data to `targetPath` in local hard drive and returns location.

##### dataPrep.loadHadoop()

> Return type: `str`

> Description: This method loads the data to `targetPath` in HDFS and returns the location.

##### dataPrep.localPath()

> Return type: `str`

> Description: This method returns the location of the loaded data on local hard drive. If the data is not loaded,
it will return the location the data will be loaded.

##### dataPrep.hadoopPath()

> Return type: `instance` of `Sentence`

> Description: This method returns the location of the loaded data on HDFS. If the data is not loaded,
an error will be raised.
