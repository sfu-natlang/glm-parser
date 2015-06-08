run:

    python glm_parser.py -b 2 -e 21 -t 0 -p ~/data/glm-parser-data/penn-wsj-deps/ -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner

result (`tail -6 glm_parser.log`):

    06/08/2015 03:13:59 PM DEBUG: Loading section 00 
    06/08/2015 03:14:00 PM DEBUG: Start evaluating ...
    06/08/2015 03:14:00 PM INFO: Feature count: 9108159
    06/08/2015 03:14:00 PM DEBUG: Data finishing 0.00% ...
    06/08/2015 03:14:23 PM DEBUG: Data finishing 52.06% ...
    06/08/2015 03:14:49 PM INFO: Unlabeled accuracy: 0.858345353168 (39871, 46451)
