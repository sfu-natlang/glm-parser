run

python glm_parser.py -i 5 -p ~/penn-wsj-deps/ --train="wsj_02[0-9][0-9].mrg.3.pa.gs.tab" --test="wsj_00[0-9][0-9].mrg.3.pa.gs.tab" -d 05-11-2015 -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/penn2malt.config

result

03/09/2016 03:52:56 PM DEBUG: Starting sequential train ... 
03/09/2016 03:52:56 PM DEBUG: Iteration: 0
03/09/2016 03:52:56 PM DEBUG: Data size: 2024
...
03/09/2016 03:55:01 PM DEBUG: Iteration: 1
03/09/2016 03:55:01 PM DEBUG: Data size: 2024
...
03/09/2016 03:57:04 PM DEBUG: Iteration: 2
03/09/2016 03:57:04 PM DEBUG: Data size: 2024
...
03/09/2016 03:59:14 PM DEBUG: Iteration: 3
03/09/2016 03:59:14 PM DEBUG: Data size: 2024
...
03/09/2016 04:01:25 PM DEBUG: Iteration: 4
03/09/2016 04:01:25 PM DEBUG: Data size: 2024
...
03/09/2016 04:05:35 PM INFO: Training time usage(seconds): 645.636075
03/09/2016 04:05:35 PM INFO: Feature count: 881651
03/09/2016 04:05:35 PM INFO: Unlabeled accuracy: 0.839529827130 (38997, 46451)
03/09/2016 04:05:35 PM INFO: Unlabeled attachment accuracy: 0.845902588274 (40918, 48372)
