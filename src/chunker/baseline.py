
import perc
import sys, os, optparse, logging, time
from collections import defaultdict

def get_truth(labeled_list):
    true_output = []
    for i in labeled_list:
        (w, t, label) = i.split()
        true_output.append(label)
    return true_output

def perc_train(train_data, tagset, n):
    # insert your code here
    if len(tagset) <= 0:
        raise ValueError("Empty tagset")
    default_tag = tagset[0]
    feat_vec = defaultdict(int)

    epochs = n
    for round in range(0,epochs):
        num_mistakes = 0
        for (labeled_list, feat_list) in train_data:
            output = perc.perc_test(feat_vec, labeled_list, feat_list, tagset, default_tag)
            true_output = get_truth(labeled_list)
            logging.info("arg max output: %s" % (" ".join(output)))
            logging.info("truth: %s" % (" ".join(true_output)))
            #print >>sys.stderr, "\noutput:", output, "\ntruth:", true_output
            if output != true_output:
                num_mistakes += 1
                output.insert(0,'B_-1')
                output.append('B_+1')
                true_output.insert(0,'B_-1')
                true_output.append('B_+1')
                feat_index = 0
                for i in range(1,len(output)-1):
                    #print >>sys.stderr, output[i], true_output[i]
                    (feat_index, feats) = perc.feats_for_word(feat_index, feat_list)
                    if len(feats) == 0:
                        print >>sys.stderr, " ".join(labeled_list), " ".join(feat_list), "\n"
                        raise ValueError("features do not align with input sentence")
                    #print >>sys.stderr, feats
                    feat_vec_update = defaultdict(int)
                    for feat in feats:
                        #!!!Debug: output_feat is not truth feat....
                        output_feat = truth_feat = feat

                        feat_vec_update[output_feat, output[i]] += -1
                        feat_vec_update[truth_feat, true_output[i]] += 1

                    for (upd_feat, upd_tag) in feat_vec_update:
                        if feat_vec_update[upd_feat, upd_tag] != 0:
                            feat_vec[upd_feat, upd_tag] += feat_vec_update[upd_feat, upd_tag]
                            logging.info("updating feat_vec with feature_id: (%s, %s) value: %d" % (upd_feat, upd_tag, feat_vec_update[upd_feat, upd_tag]))
        print >>sys.stderr, "number of mistakes:", num_mistakes
        logging.info("current number of mistakes: %d" % (num_mistakes))
    return feat_vec
#lazy update
def avg_perc_train(train_data, tagset, n):
    # insert your code here
    if len(tagset) <= 0:
        raise ValueError("Empty tagset")
    default_tag = tagset[0]

    feat_vec = defaultdict(int)
    avg_vec = defaultdict(int)
    last_iter = {}

    epochs = n
    num_updates = 0
    for round in range(0,epochs):
        num_mistakes = 0
        for (labeled_list, feat_list) in train_data:
            num_updates += 1
            output = perc.perc_test(feat_vec, labeled_list, feat_list, tagset, default_tag)
            true_output = get_truth(labeled_list)
            logging.info("arg max output: %s" % (" ".join(output)))
            logging.info("truth: %s" % (" ".join(true_output)))
            #print >>sys.stderr, "\noutput:", output, "\ntruth:", true_output
            if output != true_output:
                num_mistakes += 1
                output.insert(0,'B_-1')
                output.append('B_+1')
                true_output.insert(0,'B_-1')
                true_output.append('B_+1')
                feat_index = 0
                for i in range(1,len(output)-1):
                    #print >>sys.stderr, output[i], true_output[i]
                    (feat_index, feats) = perc.feats_for_word(feat_index, feat_list)
                    if len(feats) == 0:
                        print >>sys.stderr, " ".join(labeled_list), " ".join(feat_list), "\n"
                        raise ValueError("features do not align with input sentence")
                    #print >>sys.stderr, feats
                    feat_vec_update = defaultdict(int)
                    for feat in feats:
                        if feat == 'B':
                            output_feat = 'B:' + output[i-1]
                            truth_feat = 'B:' + true_output[i-1]
                        else:
                            output_feat = truth_feat = feat

                        feat_vec_update[output_feat, output[i]] += -1
                        feat_vec_update[truth_feat, true_output[i]] += 1
                        #reason: if output[i]==true_output[i] update = 0
                    for (upd_feat, upd_tag) in feat_vec_update:
                        if feat_vec_update[upd_feat, upd_tag] != 0:
                            feat_vec[upd_feat, upd_tag] += feat_vec_update[upd_feat, upd_tag]
                            logging.info("updating feat_vec with feature_id: (%s, %s) value: %d" % (upd_feat, upd_tag, feat_vec_update[upd_feat, upd_tag]))
                            if (upd_feat, upd_tag) in last_iter:
                                avg_vec[upd_feat, upd_tag] += (num_updates - last_iter[upd_feat, upd_tag]) * feat_vec[upd_feat, upd_tag]
                            else:
                                avg_vec[upd_feat, upd_tag] = feat_vec[upd_feat, upd_tag]
                            last_iter[upd_feat, upd_tag] = num_updates
        print >>sys.stderr, "number of mistakes:", num_mistakes
    for (feat, tag) in feat_vec:
        if (feat, tag) in last_iter:
            avg_vec[feat, tag] += (num_updates - last_iter[feat, tag]) * feat_vec[feat, tag]
        else:
            avg_vec[feat, tag] = feat_vec[feat, tag]
        feat_vec[feat, tag] = avg_vec[feat, tag] / num_updates
    return feat_vec

if __name__ == '__main__':
    optparser = optparse.OptionParser()
    optparser.add_option("-t", "--tagsetfile", dest="tagsetfile", default=os.path.join("data", "tagset.txt"), help="tagset that contains all the labels produced in the output, i.e. the y in \phi(x,y)")
    optparser.add_option("-i", "--trainfile", dest="trainfile", default=os.path.join("data", "train.txt.gz"), help="input data, i.e. the x in \phi(x,y)")
    optparser.add_option("-f", "--featfile", dest="featfile", default=os.path.join("data", "train.feats.gz"), help="precomputed features for the input data, i.e. the values of \phi(x,_) without y")
    optparser.add_option("-a", "--average", action="store_true", dest="average", default=False, help="run averaged perceptron")
    optparser.add_option("-e", "--numepochs", dest="numepochs", default=int(20), help="number of epochs of training; in each epoch we iterate over over all the training examples")
    optparser.add_option("-m", "--modelfile", dest="modelfile", default=os.path.join("data", "default.model"), help="weights for all features stored on disk")
    optparser.add_option("-l", "--logfile", dest="logfile", default=None, help="logging output file")
    (opts, _) = optparser.parse_args()

    # each element in the feat_vec dictionary is:
    # key=feature_id value=weight
    feat_vec = {}
    tagset = []
    train_data = []

    if opts.logfile:
        logging.basicConfig(filename=opts.logfile, filemode='w', level=logging.INFO)

    tagset = perc.read_tagset(opts.tagsetfile)
    print >>sys.stderr, "reading data ..."
    train_data = perc.read_labeled_data(opts.trainfile, opts.featfile)
    print >>sys.stderr, "done."
    print "start timer..."
    t0 = time.time()
    if opts.average:
        feat_vec = avg_perc_train(train_data, tagset, int(opts.numepochs))
    else:
        feat_vec = perc_train(train_data, tagset, int(opts.numepochs))
    print (time.time() - t0, "seconds wall time")
    perc.perc_write_to_file(feat_vec, opts.modelfile)

