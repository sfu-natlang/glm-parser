run

    python glm_parser.py -i 5 -b 2 -e 21 -t 0 -p ~/data/penn-wsj-deps/ -a -d 08-15-2015 --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner

result (`tail -3 glm_parser.log`):
    
    08/15/2015 07:20:28 PM INFO: Feature count: 6825155
    08/15/2015 07:20:28 PM INFO: Unlabeled accuracy: 0.903898731997 (41987, 46451)           
    08/15/2015 07:20:28 PM INFO: Unlabeled attachment accuracy: 0.907715207145 (43908, 48372)

