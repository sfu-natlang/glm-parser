# File IO

###### API Version: 1.0.0
###### Edit: 2016-08-01 14:31, Jetic Gu

### 1. Description

`file_io` provides the ability to read and write data to local hard drive and
HDFS.
It is encouraged that one uses the functions provided in `file_io` instead of
using standard python file reading and writing methods.

Supported URI prefixes are: "hdfs://" and "file://"

#### 1.1 Import

	from data.file_io import fileRead, fileWrite

### 2. fileRead

#### 2.1 Parameters

Parameter		|	Type				|	Default Value	|	Description	|	Examples
----------------|-----------------------|-------------------|---------------|------------
fileURI			| `str`					|					| `fileURI` should always start with URI prefix to avoid confusion. The default URI is "hdfs://" if one isn't provided.	| "file://example.txt"; "hdfs://example.txt"
SparkContext	| `pyspark.context.SparkContext` | None		| SparkContext	|	sc

#### 2.2 Return

If fileRead encountered no error, it should return a `list`, each element in
the list would be a string with no tailing `\n`, representing a single line of
the original file.

#### 2.3 Example

Contents of a text file(example.txt):

	Good things of day begin to droop and drowse;\n
	Whiles night's black agents to their preys do rouse.\n

Code:

	fileRead("file://example.txt", None)

Return:

	[
	'Good things of day begin to droop and drowse;',
	'Whiles night's black agents to their preys do rouse.'
	]


### 3. fileWrite

#### 3.1 Parameters

Parameter		|	Type				|	Default Value	|	Description	|	Examples
----------------|-----------------------|-------------------|---------------|------------
fileURI			| `str`					|					| `fileURI` should always start with URI prefix to avoid confusion. The default URI is "hdfs://" if one isn't provided.	| "file://example.txt"; "hdfs://example.txt"
contents		| `list` of `str`		|					| the format of this file should be exactly the same as the example above: a `list` of `str`, each representing a single line without tailing `\n`. | ['Good things of day begin to droop and drowse;',	'Whiles night's black agents to their preys do rouse.']
SparkContext	| `pyspark.context.SparkContext` | None		| SparkContext	|	sc

#### 3.2 Return

This method if encountered no error would return the fileURI of the file that it has written in. Note that when writing to hadoop, overwriting existing file would result in error. Also, writing to Hadoop would mean that a folder located and named after `fileURI` would be created and the actual `fileURI` will be returned.

#### 3.3 Example

Code:

	contents = [
		'Good things of day begin to droop and drowse;',
		'Whiles night's black agents to their preys do rouse.']

	print "Writing to local:"
	print fileWrite("file://example.txt", contents, None)
	
	print "Writing to HDFS:"
	print fileWrite("hdfs://example.txt", contents, sc)

Output:

	Writing to local:
	file://example.txt
	Writing to HDFS:
	hdfs://example.txt/part-00000
