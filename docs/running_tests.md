Running Full Tests with penn2malt on GLM Parser in The Purpose of Debugging
------

###Introduction

The GLM Parser now runs in three modes, with two learners and an additional
option. Each and every single one of the combinations of all these options
should be tested for the purpose of debugging.

###Part 1. options

####Three running modes:

1. Sequential mode. The glm_parser will load all the data, format file, and
config file from local filesystem and the log file would be `glm_parser.log`
under `src/`.

2. Spark Standalone. The glm_parser will by default of the programme treat all
file paths as local paths, and the log file would be `glm_parser.log` under
`src/`. When testing in Spark Standalone mode, please use a few data shards(4
is the recommended number of shards)

3. Spark YARN cluster mode. This mode is different because by default all the
files should be uploaded to and read from the hadoop cluster. Logs which are
supposed to be saved to `src/glm_parser.log` will not be supported. In this
case one should make sure all the necessary information get posted to stdout,
which can be accessed by YARN log command or Hadoop History Server webUI.

Spark Yarn mode is the only spark cluster mode which supports running python
codes, which in its nature is submitting the pyspark executables along with our
own code to the hadoop YARN cluster. When testing in Spark Standalone mode,
please use a few data shards(8 is the recommended number of shards).

####Two Learners:

1. average_perceptron: the default selection of learner in all of the config
files under `src/config/`, which is an improved version of perceptron.

2. perceptron: used by command line option `--learner=perceptron`.

####One Additional option:

1. without tagger_w_vector, which uses the gold Part of Speech Tags while
evaluating the trained GLM Parser weight vector;

2. with tagger_w_vector, which uses the Part of Speech Tags produced by our own
tagger while evaluating the trained GLM Parser weight vector.

###Part 2. Datasets and Iterations

####config/debug.config

debug.config uses 1 of 24 data sections of penn2malt dataset, which is mainly
used for debugging with the smallest dataset. While running with debug.config,
one iteration is enough. The purpose is to see if the programme or a specific
module runs(finishes with exit code 0).

####config/default.config

default.config is a sub set of the penn2malt dataset, it contains more sections
than debug.config but takes relatively shorter time to complete the training
than the entire penn2malt, which is perfect for the purpose of a more thorough
debug run to see if the programme actually works(finishes with exit code 0 and
the results matches previous tests). It is important that one tests with
default.config with more iterations(usually 5) before committing, because some
bugs only surface when running on multiple data sections and more iterations.

When one is running tests with default.config, it is recommended but not
mandatory that one evaluates on all five iterations: 1, 2, 3, 4, 5. Such is
just for the sake of being more cautious.

####config/penn-wsj-deps.config

penn-wsj-deps.config uses all the sections of the penn2malt dataset with five
iterations. It would normally take about 5 hours to finish. Testing with
penn-wsj-deps while debugging is not necessary.

###Part 3. A Full Debug Test

When running a full debug test for the SFU Natlang Lab on the GLM Parser, one
is advised to complete the following tests in the following order:

1. debug.config, 1 iteration, sequential mode;

2. debug.config, 1 iteration, spark standalone, 4 shards;

3. debug.config, 1 iteration, spark yarn mode, 8 shards;

4. debug.config, 1 iteration, sequential mode, perceptron learner;

5. debug.config, 1 iteration, spark standalone, 4 shards, perceptron learner;

6. debug.config, 1 iteration, spark yarn mode, 8 shards, perceptron learner;

7. debug.config, 1 iteration, sequential mode, with tagger-w-vector;

8. debug.config, 1 iteration, spark standalone, 4 shards, with tagger-w-vector;

9. debug.config, 1 iteration, spark yarn mode, 8 shards, with tagger-w-vector;

10. default.config, 5 iteration, sequential mode;

11. default.config, 5 iteration, spark standalone, 4 shards;

12. default.config, 5 iteration, spark yarn mode, 8 shards;

13. default.config, 5 iteration, sequential mode, perceptron learner;

14. default.config, 5 iteration, spark standalone, 4 shards, perceptron learner;

15. default.config, 5 iteration, spark yarn mode, 8 shards, perceptron learner;

16. default.config, 5 iteration, sequential mode, with tagger-w-vector;

17. default.config, 5 iteration, spark standalone, 4 shards, with tagger-w-vector;

18. default.config, 5 iteration, spark yarn mode, 8 shards, with tagger-w-vector;

Explanations:

Test 1-9 are ones with debug.config, which take less time to finish is perfect
for early stage debugging, it will help the tester to quickly locate bugs and
get them fixed.

Test 10-18 are ones with default.config, which take a considerable amount of
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
