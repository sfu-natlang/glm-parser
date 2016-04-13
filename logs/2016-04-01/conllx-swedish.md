run:

    python glm_parser.py -i 5 -p ~/data/CoNLL-X/Swedish/data --train="swedish_talbanken05_train.conll" --test="swedish_talbanken05_test.conll" -d 05-11-2015 -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllx.config

result:

    03/31/2016 05:04:29 PM DEBUG: Iteration: 0
    03/31/2016 05:04:29 PM DEBUG: Data size: 11042

    03/31/2016 05:13:22 PM DEBUG: Iteration: 1
    03/31/2016 05:13:22 PM DEBUG: Data size: 11042

    03/31/2016 05:21:01 PM DEBUG: Iteration: 2
    03/31/2016 05:21:01 PM DEBUG: Data size: 11042

    03/31/2016 05:29:05 PM DEBUG: Iteration: 3
    03/31/2016 05:29:05 PM DEBUG: Data size: 11042

    03/31/2016 05:37:11 PM DEBUG: Iteration: 4
    03/31/2016 05:37:11 PM DEBUG: Data size: 11042

    03/31/2016 05:45:22 PM INFO: Training time usage(seconds): 2464.025773
    03/31/2016 05:45:22 PM INFO: Feature count: 2511204
    03/31/2016 05:45:22 PM INFO: Unlabeled accuracy: 0.868104667610 (4910, 5656)
    03/31/2016 05:45:22 PM INFO: Unlabeled attachment accuracy: 0.876592224979 (5299, 6045)
