machine: linearb
commit: 7c201acf45c54a6c653a946dea2b809892a44855
branch: pos-parser-merge-step-1

learner: average_perceptron
parser: ceisner
feature-generator: english_1st_fgen
dataset: penn-wsj-deps
train: wsj_0[2-9][0-9][0-9].mrg.3.pa.gs.tab|wsj_1[0-9][0-9][0-9].mrg.3.pa.gs.tab|wsj_2[0-1][0-9][0-9].mrg.3.pa.gs.tab
test: wsj_0[0-1][0-9][0-9].mrg.3.pa.gs.tab|wsj_22[0-9][0-9].mrg.3.pa.gs.tab|wsj_24[0-9][0-9].mrg.3.pa.gs.tab
shards: 1

timestamp: 06/21/2016 03:46:25 PM
training-time: 17964.505008
feature-count: 6836627
accuracy:
    unlabeled: 0.897033294623
    unlabeled-attachment: 0.901151631478
