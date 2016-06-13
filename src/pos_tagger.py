from data import data_pool
from pos import pos_decode, pos_perctrain, pos_features
from weight import weight_vector
import debug.debug
import debug.interact
import os,sys
import timeit
import time
import ConfigParser

from ConfigParser import SafeConfigParser
from collections import defaultdict

class PosTagger():
    def __init__(self, train_regex="", test_regex="", data_path="../../penn-wsj-deps/", tag_file="tagset.txt",
                 max_iter=1,data_format="format/penn2malt.format"):
        self.train_data = self.load_data(train_regex, data_path, data_format)
        self.test_data = self.load_data(test_regex, data_path, data_format)
        self.max_iter = max_iter
        self.default_tag = "NN"

    def load_data(self, regex, data_path, data_format):
        dp = data_pool.DataPool(regex, data_path, format_path=data_format)
        data_list =[]
        sentence_count = 0
        while dp.has_next_data():
            sentence_count+=1
            data = dp.get_next_data()
            word_list = data.column_list["FORM"]
            pos_list = data.column_list["POSTAG"]

            del word_list[0]
            del pos_list[0] # delet Root

            word_list.insert(0, '_B_-1')
            word_list.insert(0, '_B_-2') # first two 'words' are B_-2 B_-1
            word_list.append('_B_+1')
            word_list.append('_B_+2') # last two 'words' are B_+1 B_+2
            pos_list.insert(0,'B_-1')
            pos_list.insert(0,'B_-2')

            pos_feat = pos_features.Pos_feat_gen(word_list)

            gold_out_fv = defaultdict(int)
            pos_feat.get_sent_feature(gold_out_fv,pos_list)

            data_list.append((word_list,pos_list,gold_out_fv))

        print "Sentence Number: %d" % sentence_count
        return data_list

    def perc_train(self, dump_data=True):
        perc = pos_perctrain.PosPerceptron(max_iter=max_iter, default_tag="NN", tag_file="tagset.txt")
        self.w_vector = perc.avg_perc_train(self.train_data)
        if dump_data:
            perc.dump_vector("fv",max_iter,self.w_vector)

    def eveluate(self, fv_path=None):
        tester = pos_decode.Decoder(self.test_data)
        if fv_path is not None:
            feat_vec = weight_vector.WeightVector()
            feat_vec.load(fv_path)
            self.w_vector = feat_vec.data_dict

        acc = tester.get_accuracy(self.w_vector)
HELP_MSG =\
"""

options:
    -h:     Print this help message

    -p:     Path to data files (to the parent directory for all sections)
            default "./penn-wsj-deps/"

    -i:     Number of iterations
            default 1

    --train=
            Sections for training
        Input a regular expression to indicate which files to read e.g.
        "-r (0[2-9])|(1[0-9])|(2[0-1])/*.tab"

    --test=
            Sections for testing
        Input a regular expression to indicate which files to test on e.g.
        "-r (0[2-9])|(1[0-9])|(2[0-1])/*.tab"

	--tag_target=
			Specifying tagging target file
"""

MAJOR_VERSION = 0
MINOR_VERSION = 1

if __name__ == '__main__':

    import getopt, sys

    train_regex = ''
    test_regex = ''
    max_iter = 1
    test_data_path = ''  #"./penn-wsj-deps/"
    tag_file = 'tagset.txt'
    data_format = 'format/penn2malt.format'


    #tag_file = sys.argv[1]
    #max_iter = int(sys.argv[2])
    #data_path = sys.argv[3]
    #train_regex = sys.argv[4]
    #test_regex = sys.argv[5]
    #data_format = sys.argv[6]

    try:
        opt_spec = "aht:f:r:c:p:"
        long_opt_spec = ['train=','test=','format=', 'tag_target=']

        # load configuration from file
        #   configuration files are stored under src/format/
        #   configuration files: *.format
        if os.path.isfile(sys.argv[1]) == True:
            print("Reading configurations from file: %s" % (sys.argv[1]))
            cf = SafeConfigParser(os.environ)
            cf.read(sys.argv[1])

            train_regex    = cf.get("data", "train")
            test_regex     = cf.get("data", "test")
            test_data_path = cf.get("data", "data_path")
            data_format    = cf.get("data", "format")
            tag_file       = cf.get("data", "tag_file")

            max_iter                             = cf.getint(    "option", "iteration")

            opts, args = getopt.getopt(sys.argv[2:], opt_spec, long_opt_spec)
        else:
            opts, args = getopt.getopt(sys.argv[1:], opt_spec, long_opt_spec)

        # load configuration from command line
        for opt, value in opts:
            if opt == "-h":
                print("")
                print("Part Of Speech (POS) Tagger")
                print("Version %d.%d" % (MAJOR_VERSION, MINOR_VERSION))
                print(HELP_MSG)
                sys.exit(0)
            elif opt == "-p":
                test_data_path = value
            elif opt == "-i":
                max_iter = int(value)
            elif opt == '--train':
                train_regex = value
            elif opt == '--test':
                test_regex = value
            elif opt == '--format':
                data_format = value
            elif opt == '--tag_target':
                tag_file = value
            else:
                #print "Invalid argument, try -h"
                sys.exit(0)

        start_time = time.time()
        tagger = PosTagger(train_regex, test_regex, test_data_path, tag_file, max_iter, data_format)
        tagger.perc_train()
        end_time = time.time()
        training_time = end_time - start_time
        print "Total Training Time: ", training_time

        tagger.eveluate()
    except getopt.GetoptError, e:
        print("Invalid argument. \n")
        print(HELP_MSG)
        # Make sure we know what's the error
        raise
