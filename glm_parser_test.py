# -*- coding: utf-8 -*-
import glm_parser

if __name__ == "__main__":
    gp = glm_parser.GlmParser()
    gp.train([(2,21)])
    print gp.unlabeled_accuracy([0,1,22,24])