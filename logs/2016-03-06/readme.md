##6. March 2016
The test is conducted on a 2012 Quad-core Mac Pro. It consists of 10 individual testing, each uses one copy of glm-parser.

###01
	python glm_parser.py -i 5 -p ~/Daten/glm-parser-data/CoNLL-X/Bulgarian/data --train=bulgarian_bultreebank_train.conll --test=bulgarian_bultreebank_test.conll -d 06-03-2016_Bulgarian -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllx.config

###02
	python glm_parser.py -i 5 -p ~/Daten/glm-parser-data/CoNLL-X/Danish/data --train=danish_ddt_train.conll --test=danish_ddt_test.conll -d 06-03-2016_Danish -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllx.config

###03

	python glm_parser.py -i 5 -p ~/Daten/glm-parser-data/CoNLL-X/Dutch/data --train=dutch_alpino_train.conll --test=dutch_alpino_test.conll -d 06-03-2016_Dutch -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllx.config

###04

	python glm_parser.py -i 5 -p ~/Daten/glm-parser-data/CoNLL-X/German/data --train=german_tiger_train.conll --test=german_tiger_test.conll -d 06-03-2016_German -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllx.config

###05

	python glm_parser.py -i 5 -p ~/Daten/glm-parser-data/CoNLL-X/Japanese/data --train=japanese_verbmobil_train.conll --test=japanese_verbmobil_test.conll -d 06-03-2016_Japanese -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllx.config

###06

	python glm_parser.py -i 5 -p ~/Daten/glm-parser-data/CoNLL-X/Portuguese/data --train=portuguese_bosque_train.conll --test=portuguese_bosque_test.conll -d 06-03-2016_Portuguese -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllx.config

###07

	python glm_parser.py -i 5 -p ~/Daten/glm-parser-data/CoNLL-X/Slovene/data --train=slovene_sdt_train.conll --test=slovene_sdt_test.conll -d 06-03-2016_Slovene -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllx.config

###08

	python glm_parser.py -i 5 -p ~/Daten/glm-parser-data/CoNLL-X/Spanish/data --train=spanish_cast3lb_train.conll --test=spanish_cast3lb_test.conll -d 06-03-2016_Spanish -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllx.config

###09

	python glm_parser.py -i 5 -p ~/Daten/glm-parser-data/CoNLL-X/Swedish/data --train=swedish_talbanken05_train.conll --test=swedish_talbanken05_test.conll -d 06-03-2016_Swedish -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllx.config

###10

	python glm_parser.py -i 5 -p ~/Daten/glm-parser-data/CoNLL-X/Turkish/data --train=turkish_metu_sabanci_train.conll --test=turkish_metu_sabanci_test.conll -d 06-03-2016_Turkish -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllx.config

