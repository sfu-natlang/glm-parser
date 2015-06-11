
# GLM Parser Documentation

## Code Structure

The code for this project is organized into the following main directories:

* `src`: contains all the source code.
* `scripts`: all the scripts for running experiments including scripts to submit jobs to the RCG cluster.
* `logs`: keep all your experiment logs in here organized by date. keep the enviroment and command that was run to obtain the results.
* `docs`: all the documentation of the project.

The contents of `src` are organized as follows:

### `data`

This module contains the classes used to load test data from Penn
Treebank and creates the class DependencyTree which stores the
information of test data: wordlist, taglist (part-of-speech tags),
edges in the dependency tree.

- `DependencyTree`
: This data structure represents the output of a dependency parser.
  Each class instance stores four types of information: node set,
  part-of-speech (POS) set, edge set and edge type. This information
  is sufficient to construct a dependency tree. This class also
  provides interfaces to manipulate the information, including
  retrieving nodes, edges, types, modifying nodes, edges, types, and
  other relevant tasks.
- `DataPool`
: Stores the test data as a list of DependencyTree objects.

### `feature`

This module contains the classes deal with features, such as
extracting features from tagged sentences and holding the weight
information of the features. 

- `FeatureVector`
: Stores the features of an edge in a collection (currently as a `hvector` dictionary).
- List of features used: check the docstrings in the `feature` directory.

### `parse`

This module contains the parsing algorithm for the parser, such as
the cubic time Eisner algorithm and modified Eisner algorithm with
second order features, third order features, etc.

The alternative parsers can easily substitute for each other as
long as they have the function:

    parse(sentence, score_function)

### `learn`

This module contains the weight learning algorithm for the GLM
parser, such as perceptron, average perceptron and MIRA, etc.

Alternative weight learning algorithms can substitute for each other
as long as it contains the function:

    learn(feature_set, current_global_vector, gold_global_vector)

### `evaluate`

This module contains the evaluation algorithm. The evaluator takes
the test data and the currently used parser, and calculates the
accuracy for the parser. The accuracy reported is the unlabeled
dependency accuracy and the unlabeled attachment score (UAS).

To add more accuracy test, you can either create alternative
evaluators or add functions inside the evaluator. The alternative
or modified evaluator should have function:

    evaluate(data_pool, parser, feature_set)

### `backend`

This module works with feature module to dump the learned weight
vector as a file using pickle. The weight file can be loaded by
the parser at a later time.

