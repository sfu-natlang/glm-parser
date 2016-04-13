##Summery
This is the test on CoNLL-U dataset using the latest on branch on 30-03-2016:

	datapool_fgen_clean

The tests results are:

|	index	|	language					|	results		|
|-----------|-------------------------------|---------------|
|	1		|	`UD_Ancient_Greek`			|	Success		|
|	2		|	`UD_Ancient_Greek-PROIEL`	|	Success		|
|	3		|	`UD_Arabic`					|	Fail		|
|	4		|	`UD_Basque`					|	Success		|
|	5		|	`UD_Bulgarian`				|	Fail		|
|	6		|	`UD_Croatian`				|	Success		|
|	7		|	`UD_Czech`					|	Fail		|
|	8		|	`UD_Danish`					|	Success		|
|	9		|	`UD_Dutch`					|	Fail		|
|	10		|	`UD_English`				|	Success		|
|	11		|	`UD_Estonian`				|	Fail		|
|	12		|	`UD_Finnish`				|	Fail		|
|	13		|	`UD_Finnish-FTB`			|	Fail		|
|	14		|	`UD_French`					|	Fail		|
|	15		|	`UD_German`					|	Fail		|
|	16		|	`UD_Gothic`					|	Success		|
|	17		|	`UD_Greek`					|	Fail		|
|	18		|	`UD_Hebrew`					|	Fail		|
|	19		|	`UD_Hindi`					|	Fail		|
|	20		|	`UD_Hungarian`				|	Success		|
|	21		|	`UD_Indonesian`				|	Success		|
|	22		|	`UD_Irish`					|	Success		|
|	23		|	`UD_Italian`				|	Fail		|
|	24		|	`UD_Japanese-KTC`			|	Fail		|
|	25		|	`UD_Latin`					|	Success		|
|	26		|	`UD_Latin-ITT`				|	Fail		|
|	27		|	`UD_Latin-PROIEL`			|	Success		|
|	28		|	`UD_Norwegian`				|	Success		|
|	29		|	`UD_Old_Church_Slavonic`	|	Success		|
|	30		|	`UD_Persian`				|	Fail		|
|	31		|	`UD_Polish`					|	Fail		|
|	32		|	`UD_Portuguese`				|	Fail		|
|	33		|	`UD_Romanian`				|	Fail		|
|	34		|	`UD_Slovenian`				|	Fail		|
|	35		|	`UD_Spanish`				|	Fail		|
|	36		|	`UD_Swedish`				|	Success		|
|	37		|	`UD_Tamil`					|	Fail		|


#1
    python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="grc-ud-train.conllu" --test="grc-ud-test.conllu" -d 30-03-2016_Ancient_Greek -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

	30-03-2016_Ancient_Greek.log:
	03/31/2016 02:56:18 AM INFO: Training time usage(seconds): 8051.126227
	03/31/2016 03:00:30 AM INFO: Feature count: 5389024
	03/31/2016 03:00:30 AM INFO: Unlabeled accuracy: 0.573323828759 (14477, 25251)
	03/31/2016 03:00:30 AM INFO: Unlabeled attachment accuracy: 0.588841398260 (15430, 26204)

---

#2
    python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2--train="grc_proiel-ud-train.conllu" --test="grc_proiel-ud-test.conllu" -d 30-03-2016_Ancient_Greek -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

	30-03-2016_Ancient_Greek_proiel.log:
	03/31/2016 11:42:30 AM INFO: Training time usage(seconds): 4077.691314
	03/31/2016 11:42:30 AM INFO: Feature count: 3857054
	03/31/2016 11:42:30 AM INFO: Unlabeled accuracy: 0.702842935899 (13004, 18502)
	03/31/2016 11:42:30 AM INFO: Unlabeled attachment accuracy: 0.724838596667 (14483, 19981)

---

#3
    python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="ar-ud-train.conllu" --test="ar-ud-test.conllu" -d 30-03-2016_Arabic -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

stdout:

	Time accounting is ON
	Interface object AveragePerceptronLearner detected
		 with interface sequential_learn
	Using learner: AveragePerceptronLearner (average_perceptron)
	Interface object FirstOrderFeatureGenerator detected
		 with interface get_local_vector
	Using feature generator: FirstOrderFeatureGenerator (english_1st_fgen)
	Interface object EisnerParser detected
		 with interface parse
	Using parser: EisnerParser (ceisner)
	Traceback (most recent call last):
	  File "glm_parser.py", line 323, in <module>
	    config=config)
	  File "glm_parser.py", line 43, in __init__
	    self.train_data_pool = DataPool(train_regex, data_path, fgen=self.fgen, 	config_path=config)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-3/src/data/data_pool.py", line 54, in __init__
	    self.load()
	  File "/Users/jetic/Documents/Sink 2/glm-parser-3/src/data/data_pool.py", line 130, in load
	    self.data_list += self.get_data_list(file_path)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-3/src/data/data_pool.py", line 171, in get_data_list
	    column_list[field_name_list[i]].append(entity[i])
	IndexError: list index out of range

---

#4
    python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="eu-ud-train.conllu" --test="eu-ud-test.conllu" -d 30-03-2016_Basque -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

	30-03-2016_Basque.log:
	03/31/2016 12:43:25 AM INFO: Training time usage(seconds): 1742.623729
	03/31/2016 12:43:25 AM INFO: Feature count: 1943749
	03/31/2016 12:43:25 AM INFO: Unlabeled accuracy: 0.729876097481 (17790, 24374)
	03/31/2016 12:43:25 AM INFO: Unlabeled attachment accuracy: 0.748443052000 (19589, 26173)

---

#5
    python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="bg-ud-train.conllu" --test="bg-ud-test.conllu" -d 30-03-2016_Bulgarian -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

stdout:

	Time accounting is ON
	Interface object AveragePerceptronLearner detected
		 with interface sequential_learn
	Using learner: AveragePerceptronLearner (average_perceptron)
	Interface object FirstOrderFeatureGenerator detected
		 with interface get_local_vector
	Using feature generator: FirstOrderFeatureGenerator (english_1st_fgen)
	Interface object EisnerParser detected
	 with interface parse
	Using parser: EisnerParser (ceisner)
	Traceback (most recent call last):
	  File "glm_parser.py", line 323, in <module>
	    config=config)
	  File "glm_parser.py", line 43, in __init__
	    self.train_data_pool = DataPool(train_regex, data_path, fgen=self.fgen, config_path=config)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-5/src/data/data_pool.py", line 54, in __init__
	    self.load()
	  File "/Users/jetic/Documents/Sink 2/glm-parser-5/src/data/data_pool.py", line 130, in load
	    self.data_list += self.get_data_list(file_path)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-5/src/data/data_pool.py", line 171, in get_data_list
	    column_list[field_name_list[i]].append(entity[i])
	IndexError: list index out of range

---

#6
    python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="hr-ud-test.conllu" --test="hr-ud-train.conllu" -d 30-03-2016_Croatian -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

	30-03-2016_Croatian.log:
	03/31/2016 10:01:04 AM INFO: Training time usage(seconds): 137.004405
	03/31/2016 10:01:04 AM INFO: Feature count: 151740
	03/31/2016 10:01:04 AM INFO: Unlabeled accuracy: 0.736820736643 (58074, 78817)
	03/31/2016 10:01:04 AM INFO: Unlabeled attachment accuracy: 0.748185106951 (61631, 82374)

---

#7
    python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="cs-ud-train*.conllu" --test="cs-ud-test.conllu" -d 30-03-2016_Czech -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

stdout:

	Time accounting is ON
	Interface object AveragePerceptronLearner detected
		 with interface sequential_learn
	Using learner: AveragePerceptronLearner (average_perceptron)
	Interface object FirstOrderFeatureGenerator detected
		 with interface get_local_vector
	Using feature generator: FirstOrderFeatureGenerator (english_1st_fgen)
	Interface object EisnerParser detected
		 with interface parse
	Using parser: EisnerParser (ceisner)
	Traceback (most recent call last):
	  File "glm_parser.py", line 323, in <module>
	    config=config)
	  File "glm_parser.py", line 44, in __init__
	    self.test_data_pool = DataPool(test_regex, data_path, fgen=self.fgen, config_path=config)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-7/src/data/data_pool.py", line 54, in __init__
	    self.load()
	  File "/Users/jetic/Documents/Sink 2/glm-parser-7/src/data/data_pool.py", line 130, in load
	    self.data_list += self.get_data_list(file_path)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-7/src/data/data_pool.py", line 171, in get_data_list
	    column_list[field_name_list[i]].append(entity[i])
	IndexError: list index out of range

---

#8
    python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="da-ud-train.conllu" --test="da-ud-test.conllu" -d 30-03-2016_Danish -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

	30-03-2016_Danish.log:
	03/31/2016 10:30:46 AM INFO: Training time usage(seconds): 2114.097420
	03/31/2016 10:30:46 AM INFO: Feature count: 1878265
	03/31/2016 10:30:46 AM INFO: Unlabeled accuracy: 0.791978246091 (4660, 5884)
	03/31/2016 10:30:46 AM INFO: Unlabeled attachment accuracy: 0.802771511441 (4982, 6206)

---

#9
    python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="nl-ud-train.conllu" --test="nl-ud-test.conllu" -d 30-03-2016_Dutch -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

stdout:

	Time accounting is ON
	Interface object AveragePerceptronLearner detected
		 with interface sequential_learn
	Using learner: AveragePerceptronLearner (average_perceptron)
	Interface object FirstOrderFeatureGenerator detected
		 with interface get_local_vector
	Using feature generator: FirstOrderFeatureGenerator (english_1st_fgen)
	Interface object EisnerParser detected
		 with interface parse
	Using parser: EisnerParser (ceisner)
	Traceback (most recent call last):
	  File "glm_parser.py", line 323, in <module>
	    config=config)
	  File "glm_parser.py", line 43, in __init__
	    self.train_data_pool = DataPool(train_regex, data_path, fgen=self.fgen, config_path=config)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-9/src/data/data_pool.py", line 54, in __init__
	    self.load()
	  File "/Users/jetic/Documents/Sink 2/glm-parser-9/src/data/data_pool.py", line 130, in load
	    self.data_list += self.get_data_list(file_path)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-9/src/data/data_pool.py", line 171, in get_data_list
	    column_list[field_name_list[i]].append(entity[i])
	IndexError: list index out of range

---

#10
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="en-ud-train.conllu" --test="en-ud-test.conllu" -d 30-03-2016_English -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

	30-03-2016_English.log:
	03/31/2016 12:50:22 PM INFO: Training time usage(seconds): 3711.857173
	03/31/2016 12:50:22 PM INFO: Feature count: 2862292
	03/31/2016 12:50:22 PM INFO: Unlabeled accuracy: 0.834993624482 (20955, 25096)
	03/31/2016 12:50:22 PM INFO: Unlabeled attachment accuracy: 0.847606079564 (23032, 27173)

---

#11
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="et-ud-train.conllu" --test="et-ud-test.conllu" -d 30-03-2016_Estonian -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

stdout:

	Time accounting is ON
	Interface object AveragePerceptronLearner detected
		 with interface sequential_learn
	Using learner: AveragePerceptronLearner (average_perceptron)
	Interface object FirstOrderFeatureGenerator detected
		 with interface get_local_vector
	Using feature generator: FirstOrderFeatureGenerator (english_1st_fgen)
	Interface object EisnerParser detected
		 with interface parse
	Using parser: EisnerParser (ceisner)
	Traceback (most recent call last):
	  File "glm_parser.py", line 323, in <module>
	    config=config)
	  File "glm_parser.py", line 43, in __init__
	    self.train_data_pool = DataPool(train_regex, data_path, fgen=self.fgen, config_path=config)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-11/src/data/data_pool.py", line 54, in __init__
	    self.load()
	  File "/Users/jetic/Documents/Sink 2/glm-parser-11/src/data/data_pool.py", line 130, in load
	    self.data_list += self.get_data_list(file_path)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-11/src/data/data_pool.py", line 171, in get_data_list
	    column_list[field_name_list[i]].append(entity[i])
	IndexError: list index out of range

---

#12
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="fi-ud-train.conllu" --test="fi-ud-test.conllu" -d 30-03-2016_Finnish -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

stdout:

	Time accounting is ON
	Interface object AveragePerceptronLearner detected
		 with interface sequential_learn
	Using learner: AveragePerceptronLearner (average_perceptron)
	Interface object FirstOrderFeatureGenerator detected
		 with interface get_local_vector
	Using feature generator: FirstOrderFeatureGenerator (english_1st_fgen)
	Interface object EisnerParser detected
		 with interface parse
	Using parser: EisnerParser (ceisner)
	Traceback (most recent call last):
	  File "glm_parser.py", line 323, in <module>
	    config=config)
	  File "glm_parser.py", line 43, in __init__
	    self.train_data_pool = DataPool(train_regex, data_path, fgen=self.fgen, config_path=config)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-12/src/data/data_pool.py", line 54, in __init__
	    self.load()
	  File "/Users/jetic/Documents/Sink 2/glm-parser-12/src/data/data_pool.py", line 130, in load
	    self.data_list += self.get_data_list(file_path)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-12/src/data/data_pool.py", line 171, in get_data_list
	    column_list[field_name_list[i]].append(entity[i])
	IndexError: list index out of range

---

#13
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="fi_ftb-ud-train.conllu" --test="fi_ftb-ud-test.conllu" -d 30-03-2016_Finnish-FTB -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

stdout:

	Time accounting is ON
	Interface object AveragePerceptronLearner detected
		 with interface sequential_learn
	Using learner: AveragePerceptronLearner (average_perceptron)
	Interface object FirstOrderFeatureGenerator detected
		 with interface get_local_vector
	Using feature generator: FirstOrderFeatureGenerator (english_1st_fgen)
	Interface object EisnerParser detected
		 with interface parse
	Using parser: EisnerParser (ceisner)
	Traceback (most recent call last):
	  File "glm_parser.py", line 323, in <module>
	    config=config)
	  File "glm_parser.py", line 43, in __init__
	    self.train_data_pool = DataPool(train_regex, data_path, fgen=self.fgen, config_path=config)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-13/src/data/data_pool.py", line 54, in __init__
	    self.load()
	  File "/Users/jetic/Documents/Sink 2/glm-parser-13/src/data/data_pool.py", line 130, in load
	    self.data_list += self.get_data_list(file_path)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-13/src/data/data_pool.py", line 171, in get_data_list
	    column_list[field_name_list[i]].append(entity[i])
	IndexError: list index out of range

---

#14
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="fr-ud-train.conllu" --test="fr-ud-test.conllu" -d 30-03-2016_French -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

stdout:

	Time accounting is ON
	Interface object AveragePerceptronLearner detected
		 with interface sequential_learn
	Using learner: AveragePerceptronLearner (average_perceptron)
	Interface object FirstOrderFeatureGenerator detected
		 with interface get_local_vector
	Using feature generator: FirstOrderFeatureGenerator (english_1st_fgen)
	Interface object EisnerParser detected
		 with interface parse
	Using parser: EisnerParser (ceisner)
	Traceback (most recent call last):
	  File "glm_parser.py", line 323, in <module>
	    config=config)
	  File "glm_parser.py", line 43, in __init__
	    self.train_data_pool = DataPool(train_regex, data_path, fgen=self.fgen, config_path=config)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-14/src/data/data_pool.py", line 54, in __init__
	    self.load()
	  File "/Users/jetic/Documents/Sink 2/glm-parser-14/src/data/data_pool.py", line 130, in load
	    self.data_list += self.get_data_list(file_path)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-14/src/data/data_pool.py", line 171, in get_data_list
	    column_list[field_name_list[i]].append(entity[i])
	IndexError: list index out of range

---

#15
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="de-ud-train.conllu" --test="de-ud-test.conllu" -d 30-03-2016_German -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

stdout:

	Time accounting is ON
	Interface object AveragePerceptronLearner detected
		 with interface sequential_learn
	Using learner: AveragePerceptronLearner (average_perceptron)
	Interface object FirstOrderFeatureGenerator detected
		 with interface get_local_vector
	Using feature generator: FirstOrderFeatureGenerator (english_1st_fgen)
	Interface object EisnerParser detected
		 with interface parse
	Using parser: EisnerParser (ceisner)
	Traceback (most recent call last):
	  File "glm_parser.py", line 323, in <module>
	    config=config)
	  File "glm_parser.py", line 43, in __init__
	    self.train_data_pool = DataPool(train_regex, data_path, fgen=self.fgen, config_path=config)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-15/src/data/data_pool.py", line 54, in __init__
	    self.load()
	  File "/Users/jetic/Documents/Sink 2/glm-parser-15/src/data/data_pool.py", line 130, in load
	    self.data_list += self.get_data_list(file_path)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-15/src/data/data_pool.py", line 178, in get_data_list
	    sent = Sentence(column_list, field_name_list, self.fgen)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-15/src/data/sentence.py", line 97, in __init__
	    edge_list = self.construct_edge_set()
	  File "/Users/jetic/Documents/Sink 2/glm-parser-15/src/data/sentence.py", line 141, in construct_edge_set
	    node_key = (int(head), i + 1)
	ValueError: invalid literal for int() with base 10: '_'

---

#16
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="got-ud-train.conllu" --test="got-ud-test.conllu" -d 30-03-2016_Gothic -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

	30-03-2016_Gothic.log:
	03/31/2016 10:41:41 AM INFO: Training time usage(seconds): 615.068457
	03/31/2016 10:41:41 AM INFO: Feature count: 1080997
	03/31/2016 10:41:41 AM INFO: Unlabeled accuracy: 0.756494765413 (3902, 5158)
	03/31/2016 10:41:41 AM INFO: Unlabeled attachment accuracy: 0.777423356371 (4387, 5643)

---

#17
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="el-ud-train.conllu" --test="el-ud-test.conllu" -d 30-03-2016_Greek -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

stdout:

	Time accounting is ON
	Interface object AveragePerceptronLearner detected
		 with interface sequential_learn
	Using learner: AveragePerceptronLearner (average_perceptron)
	Interface object FirstOrderFeatureGenerator detected
		 with interface get_local_vector
	Using feature generator: FirstOrderFeatureGenerator (english_1st_fgen)
	Interface object EisnerParser detected
		 with interface parse
	Using parser: EisnerParser (ceisner)
	Traceback (most recent call last):
	  File "glm_parser.py", line 323, in <module>
	    config=config)
	  File "glm_parser.py", line 43, in __init__
	    self.train_data_pool = DataPool(train_regex, data_path, fgen=self.fgen, config_path=config)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-17/src/data/data_pool.py", line 54, in __init__
	    self.load()
	  File "/Users/jetic/Documents/Sink 2/glm-parser-17/src/data/data_pool.py", line 130, in load
	    self.data_list += self.get_data_list(file_path)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-17/src/data/data_pool.py", line 178, in get_data_list
	    sent = Sentence(column_list, field_name_list, self.fgen)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-17/src/data/sentence.py", line 97, in __init__
	    edge_list = self.construct_edge_set()
	  File "/Users/jetic/Documents/Sink 2/glm-parser-17/src/data/sentence.py", line 141, in construct_edge_set
	    node_key = (int(head), i + 1)
	ValueError: invalid literal for int() with base 10: '\xce\xb8\xce\xb5\xcf\x89\xcf\x81\xce\xae\xce\xb8\xce\xb7\xce\xba\xce\xb5'

---

#18
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="he-ud-train.conllu" --test="he-ud-test.conllu" -d 30-03-2016_Hebrew -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

stdout:

	Time accounting is ON
	Interface object AveragePerceptronLearner detected
		 with interface sequential_learn
	Using learner: AveragePerceptronLearner (average_perceptron)
	Interface object FirstOrderFeatureGenerator detected
		 with interface get_local_vector
	Using feature generator: FirstOrderFeatureGenerator (english_1st_fgen)
	Interface object EisnerParser detected
		 with interface parse
	Using parser: EisnerParser (ceisner)
	Traceback (most recent call last):
	  File "glm_parser.py", line 323, in <module>
	    config=config)
	  File "glm_parser.py", line 43, in __init__
	    self.train_data_pool = DataPool(train_regex, data_path, fgen=self.fgen, config_path=config)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-18/src/data/data_pool.py", line 54, in __init__
	    self.load()
	  File "/Users/jetic/Documents/Sink 2/glm-parser-18/src/data/data_pool.py", line 130, in load
	    self.data_list += self.get_data_list(file_path)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-18/src/data/data_pool.py", line 178, in get_data_list
	    sent = Sentence(column_list, field_name_list, self.fgen)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-18/src/data/sentence.py", line 97, in __init__
	    edge_list = self.construct_edge_set()
	  File "/Users/jetic/Documents/Sink 2/glm-parser-18/src/data/sentence.py", line 141, in construct_edge_set
	    node_key = (int(head), i + 1)
	ValueError: invalid literal for int() with base 10: '_'

---

#19
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="hi-ud-train.conllu" --test="hi-ud-test.conllu" -d 30-03-2016_Hindi -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

stdout:

	Time accounting is ON
	Interface object AveragePerceptronLearner detected
		 with interface sequential_learn
	Using learner: AveragePerceptronLearner (average_perceptron)
	Interface object FirstOrderFeatureGenerator detected
		 with interface get_local_vector
	Using feature generator: FirstOrderFeatureGenerator (english_1st_fgen)
	Interface object EisnerParser detected
		 with interface parse
	Using parser: EisnerParser (ceisner)
	Traceback (most recent call last):
	  File "glm_parser.py", line 323, in <module>
	    config=config)
	  File "glm_parser.py", line 43, in __init__
	    self.train_data_pool = DataPool(train_regex, data_path, fgen=self.fgen, config_path=config)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-19/src/data/data_pool.py", line 54, in __init__
	    self.load()
	  File "/Users/jetic/Documents/Sink 2/glm-parser-19/src/data/data_pool.py", line 130, in load
	    self.data_list += self.get_data_list(file_path)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-19/src/data/data_pool.py", line 171, in get_data_list
	    column_list[field_name_list[i]].append(entity[i])
	IndexError: list index out of range

---

#20
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="hu-ud-train.conllu" --test="hu-ud-test.conllu" -d 30-03-2016_Hungarian -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

	30-03-2016_Hungarian.log:
	03/31/2016 12:59:36 AM INFO: Training time usage(seconds): 751.919652
	03/31/2016 12:59:36 AM INFO: Feature count: 597436
	03/31/2016 12:59:36 AM INFO: Unlabeled accuracy: 0.776513761468 (2116, 2725)
	03/31/2016 12:59:36 AM INFO: Unlabeled attachment accuracy: 0.787286063570 (2254, 2863)

---

#21
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="id-ud-train.conllu" --test="id-ud-test.conllu" -d 30-03-2016_Indonesian -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

	30-03-2016_Indonesian.log:
	03/31/2016 12:23:27 PM INFO: Training time usage(seconds): 2268.629371
	03/31/2016 12:23:27 PM INFO: Feature count: 1772649
	03/31/2016 12:23:27 PM INFO: Unlabeled accuracy: 0.806791171477 (9504, 11780)
	03/31/2016 12:23:27 PM INFO: Unlabeled attachment accuracy: 0.815514306558 (10061, 12337)

---

#22
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="ga-ud-train.conllu" --test="ga-ud-test.conllu" -d 30-03-2016_Irish -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

	30-03-2016_Irish.log:
	03/31/2016 12:44:58 AM INFO: Training time usage(seconds): 1108.340801
	03/31/2016 12:44:58 AM INFO: Feature count: 454725
	03/31/2016 12:44:58 AM INFO: Unlabeled accuracy: 0.760010468464 (2904, 3821)
	03/31/2016 12:44:58 AM INFO: Unlabeled attachment accuracy: 0.769075799547 (3054, 3971)

---

#23
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="it-ud-train.conllu" --test="it-ud-test.conllu" -d 30-03-2016_Italian -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

stdout:

	Time accounting is ON
	Interface object AveragePerceptronLearner detected
		 with interface sequential_learn
	Using learner: AveragePerceptronLearner (average_perceptron)
	Interface object FirstOrderFeatureGenerator detected
		 with interface get_local_vector
	Using feature generator: FirstOrderFeatureGenerator (english_1st_fgen)
	Interface object EisnerParser detected
		 with interface parse
	Using parser: EisnerParser (ceisner)
	Traceback (most recent call last):
	  File "glm_parser.py", line 323, in <module>
	    config=config)
	  File "glm_parser.py", line 43, in __init__
	    self.train_data_pool = DataPool(train_regex, data_path, fgen=self.fgen, config_path=config)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-23/src/data/data_pool.py", line 54, in __init__
	    self.load()
	  File "/Users/jetic/Documents/Sink 2/glm-parser-23/src/data/data_pool.py", line 130, in load
	    self.data_list += self.get_data_list(file_path)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-23/src/data/data_pool.py", line 171, in get_data_list
	    column_list[field_name_list[i]].append(entity[i])
	IndexError: list index out of range

---

#24
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="ja_ktc-ud-train.conllu" --test="ja_ktc-ud-test.conllu" -d 30-03-2016_Japanese-KTC -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

stdout:

	Time accounting is ON
	Interface object AveragePerceptronLearner detected
		 with interface sequential_learn
	Using learner: AveragePerceptronLearner (average_perceptron)
	Interface object FirstOrderFeatureGenerator detected
		 with interface get_local_vector
	Using feature generator: FirstOrderFeatureGenerator (english_1st_fgen)
	Interface object EisnerParser detected
		 with interface parse
	Using parser: EisnerParser (ceisner)
	Traceback (most recent call last):
	  File "glm_parser.py", line 323, in <module>
	    config=config)
	  File "glm_parser.py", line 43, in __init__
	    self.train_data_pool = DataPool(train_regex, data_path, fgen=self.fgen, config_path=config)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-24/src/data/data_pool.py", line 54, in __init__
	    self.load()
	  File "/Users/jetic/Documents/Sink 2/glm-parser-24/src/data/data_pool.py", line 130, in load
	    self.data_list += self.get_data_list(file_path)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-24/src/data/data_pool.py", line 171, in get_data_list
	    column_list[field_name_list[i]].append(entity[i])
	IndexError: list index out of range

---

#25
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="la-ud-train.conllu" --test="la-ud-test.conllu" -d 30-03-2016_Latin -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

	30-03-2016_Latin.log:
	03/31/2016 10:18:40 AM INFO: Training time usage(seconds): 662.023184
	03/31/2016 10:18:40 AM INFO: Feature count: 1700315
	03/31/2016 10:18:40 AM INFO: Unlabeled accuracy: 0.541804635762 (2618, 4832)
	03/31/2016 10:18:40 AM INFO: Unlabeled attachment accuracy: 0.562623468985 (2848, 5062)

---

#26
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="la_itt-ud-train.conllu" --test="la_itt-ud-test.conllu" -d 30-03-2016_Latin-ITT -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

stdout:

	Time accounting is ON
	Interface object AveragePerceptronLearner detected
		 with interface sequential_learn
	Using learner: AveragePerceptronLearner (average_perceptron)
	Interface object FirstOrderFeatureGenerator detected
		 with interface get_local_vector
	Using feature generator: FirstOrderFeatureGenerator (english_1st_fgen)
	Interface object EisnerParser detected
		 with interface parse
	Using parser: EisnerParser (ceisner)
	Traceback (most recent call last):
	  File "glm_parser.py", line 323, in <module>
	    config=config)
	  File "glm_parser.py", line 43, in __init__
	    self.train_data_pool = DataPool(train_regex, data_path, fgen=self.fgen, config_path=config)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-26/src/data/data_pool.py", line 54, in __init__
	    self.load()
	  File "/Users/jetic/Documents/Sink 2/glm-parser-26/src/data/data_pool.py", line 130, in load
	    self.data_list += self.get_data_list(file_path)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-26/src/data/data_pool.py", line 171, in get_data_list
	    column_list[field_name_list[i]].append(entity[i])
	IndexError: list index out of range

---

#27
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="la_proiel-ud-train.conllu" --test="la_proiel-ud-test.conllu" -d 30-03-2016_Latin-PROIEL -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

	30-03-2016_Latin-PROIEL.log:
	03/31/2016 12:15:35 PM INFO: Training time usage(seconds): 2011.673218
	03/31/2016 12:15:35 PM INFO: Feature count: 3597369
	03/31/2016 12:15:35 PM INFO: Unlabeled accuracy: 0.697034751107 (10390, 14906)
	03/31/2016 12:15:35 PM INFO: Unlabeled attachment accuracy: 0.721886931888 (11722, 16238)

---

#28
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="no-ud-train.conllu" --test="no-ud-test.conllu" -d 30-03-2016_Norwegian -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

	30-03-2016_Norwegian.log:
	03/31/2016 10:11:29 AM INFO: Training time usage(seconds): 6562.772716
	03/31/2016 10:11:29 AM INFO: Feature count: 3050665
	03/31/2016 10:11:29 AM INFO: Unlabeled accuracy: 0.863488046880 (25934, 30034)
	03/31/2016 10:11:29 AM INFO: Unlabeled attachment accuracy: 0.871766803240 (27873, 31973)

---

#29
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="cu-ud-train.conllu" --test="cu-ud-test.conllu" -d 30-03-2016_Old_Church_Slavonic -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

	30-03-2016_Old_Church_Slavonic.log:
	03/31/2016 12:37:04 PM INFO: Training time usage(seconds): 763.456489
	03/31/2016 12:37:04 PM INFO: Feature count: 915602
	03/31/2016 12:37:04 PM INFO: Unlabeled accuracy: 0.802126402835 (4074, 5079)
	03/31/2016 12:37:04 PM INFO: Unlabeled attachment accuracy: 0.821903242956 (4638, 5643)

---

#30
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="fa-ud-train.conllu" --test="fa-ud-test.conllu" -d 30-03-2016_Persian -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

stdout:

	Time accounting is ON
	Interface object AveragePerceptronLearner detected
		 with interface sequential_learn
	Using learner: AveragePerceptronLearner (average_perceptron)
	Interface object FirstOrderFeatureGenerator detected
		 with interface get_local_vector
	Using feature generator: FirstOrderFeatureGenerator (english_1st_fgen)
	Interface object EisnerParser detected
		 with interface parse
	Using parser: EisnerParser (ceisner)
	Traceback (most recent call last):
	  File "glm_parser.py", line 323, in <module>
	    config=config)
	  File "glm_parser.py", line 43, in __init__
	    self.train_data_pool = DataPool(train_regex, data_path, fgen=self.fgen, config_path=config)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-30/src/data/data_pool.py", line 54, in __init__
	    self.load()
	  File "/Users/jetic/Documents/Sink 2/glm-parser-30/src/data/data_pool.py", line 130, in load
	    self.data_list += self.get_data_list(file_path)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-30/src/data/data_pool.py", line 178, in get_data_list
	    sent = Sentence(column_list, field_name_list, self.fgen)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-30/src/data/sentence.py", line 97, in __init__
	    edge_list = self.construct_edge_set()
	  File "/Users/jetic/Documents/Sink 2/glm-parser-30/src/data/sentence.py", line 141, in construct_edge_set
	    node_key = (int(head), i + 1)
	ValueError: invalid literal for int() with base 10: '_'

---

#31
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="pl-ud-train.conllu" --test="pl-ud-test.conllu" -d 30-03-2016_Polish -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

stdout:

	Time accounting is ON
	Interface object AveragePerceptronLearner detected
		 with interface sequential_learn
	Using learner: AveragePerceptronLearner (average_perceptron)
	Interface object FirstOrderFeatureGenerator detected
		 with interface get_local_vector
	Using feature generator: FirstOrderFeatureGenerator (english_1st_fgen)
	Interface object EisnerParser detected
		 with interface parse
	Using parser: EisnerParser (ceisner)
	Traceback (most recent call last):
	  File "glm_parser.py", line 323, in <module>
	    config=config)
	  File "glm_parser.py", line 43, in __init__
	    self.train_data_pool = DataPool(train_regex, data_path, fgen=self.fgen, config_path=config)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-31/src/data/data_pool.py", line 54, in __init__
	    self.load()
	  File "/Users/jetic/Documents/Sink 2/glm-parser-31/src/data/data_pool.py", line 130, in load
	    self.data_list += self.get_data_list(file_path)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-31/src/data/data_pool.py", line 171, in get_data_list
	    column_list[field_name_list[i]].append(entity[i])
	IndexError: list index out of range

---

#32
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="pt-ud-train.conllu" --test="pt-ud-test.conllu" -d 30-03-2016_Portuguese -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

stdout:

	Time accounting is ON
	Interface object AveragePerceptronLearner detected
		 with interface sequential_learn
	Using learner: AveragePerceptronLearner (average_perceptron)
	Interface object FirstOrderFeatureGenerator detected
		 with interface get_local_vector
	Using feature generator: FirstOrderFeatureGenerator (english_1st_fgen)
	Interface object EisnerParser detected
		 with interface parse
	Using parser: EisnerParser (ceisner)
	Traceback (most recent call last):
	  File "glm_parser.py", line 323, in <module>
	    config=config)
	  File "glm_parser.py", line 43, in __init__
	    self.train_data_pool = DataPool(train_regex, data_path, fgen=self.fgen, config_path=config)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-32/src/data/data_pool.py", line 54, in __init__
	    self.load()
	  File "/Users/jetic/Documents/Sink 2/glm-parser-32/src/data/data_pool.py", line 130, in load
	    self.data_list += self.get_data_list(file_path)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-32/src/data/data_pool.py", line 171, in get_data_list
	    column_list[field_name_list[i]].append(entity[i])
	IndexError: list index out of range

---

#33
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="ro-ud-train.conllu" --test="ro-ud-test.conllu" -d 30-03-2016_Romanian -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

stdout:

	Time accounting is ON
	Interface object AveragePerceptronLearner detected
		 with interface sequential_learn
	Using learner: AveragePerceptronLearner (average_perceptron)
	Interface object FirstOrderFeatureGenerator detected
		 with interface get_local_vector
	Using feature generator: FirstOrderFeatureGenerator (english_1st_fgen)
	Interface object EisnerParser detected
		 with interface parse
	Using parser: EisnerParser (ceisner)
	Traceback (most recent call last):
	  File "glm_parser.py", line 323, in <module>
	    config=config)
	  File "glm_parser.py", line 43, in __init__
	    self.train_data_pool = DataPool(train_regex, data_path, fgen=self.fgen, config_path=config)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-33/src/data/data_pool.py", line 54, in __init__
	    self.load()
	  File "/Users/jetic/Documents/Sink 2/glm-parser-33/src/data/data_pool.py", line 130, in load
	    self.data_list += self.get_data_list(file_path)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-33/src/data/data_pool.py", line 171, in get_data_list
	    column_list[field_name_list[i]].append(entity[i])
	IndexError: list index out of range

---

#34
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="sl-ud-train.conllu" --test="sl-ud-test.conllu" -d 30-03-2016_Slovenian -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

stdout:

	Time accounting is ON
	Interface object AveragePerceptronLearner detected
		 with interface sequential_learn
	Using learner: AveragePerceptronLearner (average_perceptron)
	Interface object FirstOrderFeatureGenerator detected
		 with interface get_local_vector
	Using feature generator: FirstOrderFeatureGenerator (english_1st_fgen)
	Interface object EisnerParser detected
		 with interface parse
	Using parser: EisnerParser (ceisner)
	Traceback (most recent call last):
	  File "glm_parser.py", line 323, in <module>
	    config=config)
	  File "glm_parser.py", line 43, in __init__
	    self.train_data_pool = DataPool(train_regex, data_path, fgen=self.fgen, config_path=config)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-34/src/data/data_pool.py", line 54, in __init__
	    self.load()
	  File "/Users/jetic/Documents/Sink 2/glm-parser-34/src/data/data_pool.py", line 130, in load
	    self.data_list += self.get_data_list(file_path)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-34/src/data/data_pool.py", line 171, in get_data_list
	    column_list[field_name_list[i]].append(entity[i])
	IndexError: list index out of range

---

#35
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="es-ud-train.conllu" --test="es-ud-test.conllu" -d 30-03-2016_Spanish -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

stdout:

	Time accounting is ON
	Interface object AveragePerceptronLearner detected
		 with interface sequential_learn
	Using learner: AveragePerceptronLearner (average_perceptron)
	Interface object FirstOrderFeatureGenerator detected
		 with interface get_local_vector
	Using feature generator: FirstOrderFeatureGenerator (english_1st_fgen)
	Interface object EisnerParser detected
		 with interface parse
	Using parser: EisnerParser (ceisner)
	Traceback (most recent call last):
	  File "glm_parser.py", line 323, in <module>
	    config=config)
	  File "glm_parser.py", line 43, in __init__
	    self.train_data_pool = DataPool(train_regex, data_path, fgen=self.fgen, config_path=config)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-35/src/data/data_pool.py", line 54, in __init__
	    self.load()
	  File "/Users/jetic/Documents/Sink 2/glm-parser-35/src/data/data_pool.py", line 130, in load
	    self.data_list += self.get_data_list(file_path)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-35/src/data/data_pool.py", line 171, in get_data_list
	    column_list[field_name_list[i]].append(entity[i])
	IndexError: list index out of range

---

#36
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="sv-ud-train.conllu" --test="sv-ud-test.conllu" -d 30-03-2016_Swedish -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

	30-03-2016_Swedish.log:
	03/31/2016 10:32:33 AM INFO: Training time usage(seconds): 1156.850661
	03/31/2016 10:32:34 AM INFO: Feature count: 1131539
	03/31/2016 10:32:34 AM INFO: Unlabeled accuracy: 0.831918339304 (16952, 20377)
	03/31/2016 10:32:34 AM INFO: Unlabeled attachment accuracy: 0.841405815892 (18171, 21596)

---

#37
	python glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="ta-ud-train.conllu" --test="ta-ud-test.conllu" -d 30-03-2016_Tamil -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

stdout:

	Time accounting is ON
	Interface object AveragePerceptronLearner detected
		 with interface sequential_learn
	Using learner: AveragePerceptronLearner (average_perceptron)
	Interface object FirstOrderFeatureGenerator detected
		 with interface get_local_vector
	Using feature generator: FirstOrderFeatureGenerator (english_1st_fgen)
	Interface object EisnerParser detected
		 with interface parse
	Using parser: EisnerParser (ceisner)
	Traceback (most recent call last):
	  File "glm_parser.py", line 323, in <module>
	    config=config)
	  File "glm_parser.py", line 43, in __init__
	    self.train_data_pool = DataPool(train_regex, data_path, fgen=self.fgen, config_path=config)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-37/src/data/data_pool.py", line 54, in __init__
	    self.load()
	  File "/Users/jetic/Documents/Sink 2/glm-parser-37/src/data/data_pool.py", line 130, in load
	    self.data_list += self.get_data_list(file_path)
	  File "/Users/jetic/Documents/Sink 2/glm-parser-37/src/data/data_pool.py", line 171, in get_data_list
	    column_list[field_name_list[i]].append(entity[i])
	IndexError: list index out of range

