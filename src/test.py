##########################################################################
#               Test script for average perceptron
##########################################################################
if __name__ == '__main__':

    from glm_parser import *
    from learn.average_perceptron import *
    gp = GlmParser([(2,2)], [2], "../../../../penn-wsj-deps/small_")
    gp.learner = AveragePerceptronLearner(gp.w_vector, 2)
    gp.sequential_train(max_iter=2)

    for k in gp.w_vector.data_dict.keys():
        if not gp.w_vector.data_dict[k] == 0:
            print k, gp.w_vector.data_dict[k]
