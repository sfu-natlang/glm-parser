~/Desktop/spark-1.5.2/bin/spark-submit glm_parser.py -i 1 -s 4 -p ~/data/penn-wsj-deps/ --train='wsj_02[0-9][0-9].mrg.3.pa.gs.tab' --test='wsj_00[0-9][0-9].mrg.3.pa.gs.tab' --learner=perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/penn2malt.config

03/30/2016 01:44:04 PM INFO: Training time usage(seconds): 209.322667
03/30/2016 01:44:04 PM INFO: Feature count: 844636
03/30/2016 01:44:04 PM INFO: Unlabeled accuracy: 0.814987836645 (37857, 46451)
03/30/2016 01:44:04 PM INFO: Unlabeled attachment accuracy: 0.822335235260 (39778, 48372)


~/Desktop/spark-1.5.2/bin/spark-submit glm_parser.py -i 5 -s 4 -p ~/data/penn-wsj-deps/ --train='wsj_02[0-9][0-9].mrg.3.pa.gs.tab' --test='wsj_00[0-9][0-9].mrg.3.pa.gs.tab' --learner=perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/penn2malt.config

03/30/2016 02:26:27 PM INFO: Training time usage(seconds): 1441.403626
03/30/2016 02:26:27 PM INFO: Feature count: 1008212
03/30/2016 02:26:27 PM INFO: Unlabeled accuracy: 0.834492260662 (38763, 46451)
03/30/2016 02:26:27 PM INFO: Unlabeled attachment accuracy: 0.841065078971 (40684, 48372)

~/Desktop/spark-1.5.2/bin/spark-submit glm_parser.py -i 10 -s 4 -p ~/data/penn-wsj-deps/ --train='wsj_02[0-9][0-9].mrg.3.pa.gs.tab' --test='wsj_00[0-9][0-9].mrg.3.pa.gs.tab' --learner=perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/penn2malt.config

03/30/2016 04:41:46 PM INFO: Training time usage(seconds): 6111.095743
03/30/2016 04:41:47 PM INFO: Feature count: 1019186
03/30/2016 04:41:47 PM INFO: Unlabeled accuracy: 0.837355492885 (38896, 46451)
03/30/2016 04:41:47 PM INFO: Unlabeled attachment accuracy: 0.843814603490 (40817, 48372)

on linearb:
spark-submit glm_parser.py -i 10 -s 4 -p ~/data/penn-wsj-deps/ --train='wsj_02[0-9][0-9].mrg.3.pa.gs.tab' --test='wsj_00[0-9][0-9].mrg.3.pa.gs.tab' --learner=perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/penn2malt.config

03/31/2016 01:18:59 AM INFO: Unlabeled accuracy: 0.901684485256 (150630, 167054)
03/31/2016 01:18:59 AM INFO: Unlabeled attachment accuracy: 0.905616789454 (157590, 174014)