
    pyspark glm_parser.py -i 1 -s 4 --spark -p /cs/natlang-projects/glm-parser/penn-wsj-deps/ --train="wsj_02[0-9][0-9].mrg.3.pa.gs.tab" --test="wsj_00[0-9][0-9].mrg.3.pa.gs.tab" --learner=perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/penn2malt.config

    03/18/2016 12:26:24 PM INFO: Training time usage(seconds): 112.629859
    03/18/2016 12:26:24 PM INFO: Feature count: 840788
    03/18/2016 12:26:24 PM INFO: Unlabeled accuracy: 0.815762846871 (37893, 46451)
    03/18/2016 12:26:24 PM INFO: Unlabeled attachment accuracy: 0.823079467461 (39814, 48372)

    python glm_parser.py -i 1 -p /cs/natlang-projects/glm-parser/penn-wsj-deps/ --train="wsj_02[0-9][0-9].mrg.3.pa.gs.tab" --test="wsj_00[0-9][0-9].mrg.3.pa.gs.tab" -d 03-18-2016 -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/penn2malt.config

    03/18/2016 04:42:47 PM INFO: Training time usage(seconds): 186.472745
    03/18/2016 04:42:47 PM INFO: Feature count: 697965
    03/18/2016 04:42:47 PM INFO: Unlabeled accuracy: 0.822070568987 (38186, 46451)
    03/18/2016 04:42:47 PM INFO: Unlabeled attachment accuracy: 0.829136690647 (40107, 48372)
