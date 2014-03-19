# -*- coding: utf-8 -*-
import glm_parser
import re, sys

HELP_MSG =\
"""

script for train and test glm_parser

options:
    -h:     help message
    
    -b:     begining section of training data
    -e:     ending section of training data
    (   training would not be processed
        unless both begin and ending section is specfied    )

    -a:     list of sections that should be used in accuracy testing
            please seperate the sections with ','
            i.e.  "-a 1,2,3,4,55"
    (   accuracy test would not be processed
        if testing sections are not specified   )
    
    -d:     name of the db file to load for parsing
    -o:     prefix of the name of the output file
            default: "weight"
            the name would be prefix + iteration number
            i.e. "weight_iter_0.db"
    
"""

if __name__ == "__main__":
    import getopt
    db_name = None
    train = False
    test = False
    train_begin = -1
    train_end = -1
    #trainsection = [(2,21)]
    #testsection = [0,1,22,24]
    output_file = "weight"
    try:
        opt_spec = "hb:e:a:d:o:"
        opts, args = getopt.getopt(sys.argv[1:], opt_spec)
        for opt, value in opts:
            if opt == "-h":
                print HELP_MSG
                sys.exit(0)
            elif opt == "-b":
                train_begin = int(value)
            elif opt == "-e":
                train_end = int(value)
            elif opt == "-a":
                testsection = [int(sec) for sec in value.split(',')]
                test = True
            elif opt == "-d":
                db_name = value
            elif opt == "-o":
                output_file = value
            else:
                print "invalid input, see -h"
                sys.exit(0)
                
        if train_begin >= 0 and train_end >= 0:
            trainsection = [(train_begin, train_end)]
            train = True
            
        gp = glm_parser.GlmParser(db_name)
        if train:
            print output_file, trainsection
            gp.train(trainsection, output_file=output_file)
        if test:
            print gp.unlabeled_accuracy(testsection)
    except getopt.GetoptError, e:
        print "invalid arguments!! \n" + HELP_MSG
        sys.exit(1)
        
    
