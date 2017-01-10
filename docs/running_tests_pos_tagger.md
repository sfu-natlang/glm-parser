Running Full Tests with penn2malt on POS Tagger in The Purpose of Debugging
------

###Introduction

The Tagger now runs in three modes, with two learners. It is recommended that
one only test with average_perceptron learner only, but on all three modes.

###Part 1. options

####Three running modes:

1. Sequential mode. The pos_tagger will load all the data, format file, and
config file from local filesystem and the log file would be `pos_tagger.log`
under `src/`.

2. Spark Standalone. The pos_tagger will by default of the programme treat all
file paths as local paths, and the log file would be `pos_tagger.log` under
`src/`. When testing in Spark Standalone mode, please use a few data shards(4
is the recommended number of shards)

3. Spark YARN cluster mode. This mode is different because by default all the
files should be uploaded to and read from the hadoop cluster. Logs which are
supposed to be saved to `src/pos_tagger.log` will not be supported. In this
case one should make sure all the necessary information get posted to stdout,
which can be accessed by YARN log command or Hadoop History Server webUI.

Spark Yarn mode is the only spark cluster mode which supports running python
codes, which in its nature is submitting the pyspark executables along with our
own code to the hadoop YARN cluster. When testing in Spark Standalone mode,
please use a few data shards(8 is the recommended number of shards).

####Two Learners:

1. average_perceptron: the default selection of learner in all of the config
files under `src/config/pos_*.config`, which is an improved version of perceptron.

2. perceptron: used by command line option `--learner=perceptron`. Testing with
perceptron is not necessary.

###Part 2. Datasets and Iterations

####config/pos_debug.config

pos_debug.config uses 1 of 24 data sections of penn2malt dataset, which is
mainly used for debugging with the smallest dataset. While running with
pos_debug.config, one iteration is enough. The purpose is to see if the
programme or a specific module runs(finishes with exit code 0). Note that the
tagger normally runs slower than the glm_parser. A pos_debug sequential run
will take about an hour.

####config/pos_default.config

pos_default.config is a sub set of the penn2malt dataset, it contains more
sections than pos_debug.config but takes relatively shorter time to complete
the training than the entire penn2malt, which is perfect for the purpose of a
more thorough debug run to see if the programme actually works(finishes with
exit code 0 and the results matches previous tests). It is important that one
tests with pos_default.config with more iterations(usually 5) before
committing, because some bugs only surface when running on multiple data
sections and more iterations.

When one is running tests with default.config, it is recommended but not
mandatory that one evaluates on all five iterations: 1, 2, 3, 4, 5. Such is
just for the sake of being more cautious.

####config/penn-wsj-deps.config

pos_penn-wsj-deps.config uses all the sections of the penn2malt dataset with
five iterations. It would normally take more than a day to finish. Testing with
penn-wsj-deps while debugging is not necessary.

###Part 3. A Full Debug Test

When running a full debug test for the SFU Natlang Lab on the GLM Parser, one
is advised to complete the following tests in the following order:

1. debug.config, 1 iteration, sequential mode;

2. debug.config, 1 iteration, spark standalone, 4 shards;

3. debug.config, 1 iteration, spark yarn mode, 8 shards;

4. default.config, 5 iteration, sequential mode;

5. default.config, 5 iteration, spark standalone, 4 shards;

6. default.config, 5 iteration, spark yarn mode, 8 shards;

Explanations:

Test 1-3 are ones with pos_debug.config, which take less time to finish is perfect
for early stage debugging, it will help the tester to quickly locate bugs and
get them fixed.

Test 4-6 are ones with pos_default.config, which take a considerable amount of
time to finish but never the less necessary.

In the event that ones work doesn't effect in any way some of the modules,
such as one only fixed a minor bug in a specific learner, it would not be
necessary to do a full debug test but only the directly or potentially effected
options. But still, it is advised that one consider doing a full debug test
before submitting a pull request to develop and master branch.

###Part 4. Processing The Log Files and Submitting results

One is advised to include ones test environment and all the options involved in
ones test report alongside the processed log.

And the test environment specs should include:

1. Python version

2. versions of packages which are used

3. If running in spark standalone mode, the version of pyspark

4. If running in spark yarn mode, the version of pyspark and hadoop cluster.

The test information should include:

1. Options you used (all of the options you used, both in command line and config file)

2. The branch you are testing

3. The date and time of the test

The processed log should include: (it is recommended that one uses `scripts/proc_log.sh` to process the log file)

1. Feature Count

2. Training Time

3. Evaluation Time

4. Unlabelled Accuracy

5. Unlabelled Attachment Accuracy
