This is an experiment on feature request

The experiment is done on section 2 first 10 sentences. The output has two columns. The first column is the feature requested, and the second column is the number of such requests.

It is obvious from the log, that for most of the features in one iteration, they are only requested for once. But for some of the features, they are evaluated more than once, but no more than twice.

Since speed is now of our biggest concern, it is necessary for us to figure out those features that have > 1 request count, and cache them into sentence instance. The result of this experiment could be a guideline to the development of caching utility.
