from __future__ import division
import optparse, sys, codecs, re, logging, os
from collections import Counter, defaultdict

allChunks = '__ALL__'

def readTestFile(handle):
    contents = re.sub(r'\n\s*\n', r'\n\n', handle.read())
    contents = contents.rstrip()
    testContents = defaultdict(list)
    referenceContents = defaultdict(list)
    conlleval_error_msg = "change number of features using -n, " + \
        "line does not have correct number of fields: expecting conlleval format, " + \
        "number of features:%d\n%s"
    test_error_msg = "change number of features using -n, " + \
        "line does not have correct number of fields: not expecting conlleval format, " + \
        "number of features:%d\n%s"
    for (i,sentence) in enumerate(contents.split('\n\n')):
        for line in sentence.split('\n'):
            info = line.strip().split()
            if len(info) < 1:
                continue
            if info[0] == opts.boundary:
                if opts.conlleval:
                    info = [ opts.boundary, opts.boundary, opts.outside, opts.outside ]
                else:
                    info = [ opts.boundary, opts.boundary, opts.outside ]
            if opts.conlleval:
                if len(info) != numfeats + 2:
                    logging.error(conlleval_error_msg % (numfeats,line))
                    return (testContents, referenceContents)
                testContents[i].append( (info[0], info[len(info)-1]) )
                referenceContents[i].append( (info[0], info[len(info)-2]) )
            else:
                if len(info) != int(opts.numfeats) + 1:
                    logging.error(test_error_msg % (numfeats,line))
                    return (testContents, referenceContents)
                testContents[i].append( (info[0], info[len(info)-1]) )
        if len(testContents[i]) == 0:
            logging.error("zero length sentence found: %s" % (sentence))
            return (testContents, referenceContents)
        else:
            (lastWord, lastTag) = testContents[i][len(testContents[i])-1]
            if lastTag != 'O':
                if opts.conlleval:
                    testContents[i].append( (opts.boundary, 'O') )
                    referenceContents[i].append( (opts.boundary, 'O') )
                else:
                    testContents[i].append( (opts.boundary, 'O') )
    return (testContents, referenceContents)

def collectSpans(output, msg):
    startChunk = { 
        'BB': True,
        'IB': True,
        'OB': True,
        'OI': True,
        'OE': True,
        'EE': True,
        'EI': True,
        '[': True,
        ']': True,
        }
    endChunk = { 
        'BB': True,
        'BO': True,
        'IB': True,
        'IO': True,
        'EE': True,
        'EI': True,
        'EO': True,
        '[': True,
        ']': True,
        } 
    prevChunkTag = ''
    prevChunkType = ''
    startIndex = 0
    endIndex = 0
    insideChunk = False
    spans = defaultdict(set)
    for (i, (word,label)) in enumerate(output):
        if label == 'O':
            endIndex = i
            if insideChunk:
                spans[allChunks].add( (startIndex, endIndex, prevChunkType) )
                spans[prevChunkType].add( (startIndex, endIndex) )
                logging.info("%s:%d:%d:%s:%s" % (msg, startIndex, endIndex, prevChunkType, output[startIndex:endIndex]))
            prevChunkTag = 'O'
            prevChunkType = 'O'
            startIndex = i
            insideChunk = False
            # conlleval does not give any credit to finding O phrases, so the following is commented out
            #spans[allChunks].add( (startIndex, endIndex+1, prevChunkType) )
            #spans[prevChunkType].add( (startIndex, endIndex+1) )
            logging.info("%s:%d:%d:%s:%s" % (msg, startIndex, endIndex+1, prevChunkType, output[startIndex:endIndex+1]))
        else:
            (chunkTag, chunkType) = label.split('-')
            if insideChunk and (prevChunkType != chunkType or prevChunkTag + chunkTag in endChunk):
                endIndex = i
                spans[allChunks].add( (startIndex, endIndex, prevChunkType) )
                spans[prevChunkType].add( (startIndex, endIndex) )
                logging.info("%s:%d:%d:%s:%s" % (msg, startIndex, endIndex, prevChunkType, output[startIndex:endIndex]))
                insideChunk = False
            if prevChunkType == '' or prevChunkType != chunkType or prevChunkTag + chunkTag in startChunk:
                startIndex = i
                endIndex = i
                insideChunk = True
            prevChunkTag = chunkTag
            prevChunkType = chunkType
    return spans

def corpus_fmeasure(reference, test):
    if opts.equalcheck:
        if len(test.keys()) != len(reference.keys()):
            logging.error("Error: output and reference do not have identical number of lines")
            return -1

    sentScore = defaultdict(Counter)
    numSents = 0
    numTokens = 0
    numTestPhrases = 0
    numReferencePhrases = 0
    accuracyCorrect = 0
    accuracyTokens = 0

    #for (i,j) in zip(test.keys(), reference.keys()):
    for i in reference.keys():
        numSents += 1
        numTokens += len(set(reference[i]))
        if i not in test:
            logging.error("Error: output and reference are mismatched: test: %d missing" % (i))
            return -1
        # count how many test token labels match the reference token labels using set intersection
        accuracyCorrect += len(set(test[i]) & set(reference[i]))
        testSpans = collectSpans(test[i], "tst")
        referenceSpans = collectSpans(reference[i], "ref") 
        if len(referenceSpans) == 0:
            continue
        if allChunks not in referenceSpans:
            logging.error("could not find any spans in reference data:\n%s" % (reference[i]))
            return -1
        if len(testSpans) == 0:
            numReferencePhrases += len(referenceSpans[allChunks])
            for key in set(referenceSpans.keys()):
                sentScore[key].update(correct=0, numGuessed=0, numCorrect=len(referenceSpans[key]))
            continue
        if allChunks not in testSpans:
            logging.error("could not find any spans in test data:\n%s" % (test[i]))
            return -1
        numTestPhrases += len(testSpans[allChunks])
        numReferencePhrases += len(referenceSpans[allChunks])
        # check the union of the keys in test and reference 
        for key in (set(referenceSpans.keys()) | set(testSpans.keys())):
            if key not in testSpans:
                sentScore[key].update(correct=0, numGuessed=0, numCorrect=len(referenceSpans[key]))
            elif key not in referenceSpans:
                sentScore[key].update(correct=0, numGuessed=len(testSpans[key]), numCorrect=0)
            else:
                intersection = referenceSpans[key] & testSpans[key]
                sentScore[key].update(correct=len(intersection), numGuessed=len(testSpans[key]), numCorrect=len(referenceSpans[key]))

    print "processed %d sentences with %d tokens and %d phrases; found phrases: %d; correct phrases: %d" % \
        (numSents, numTokens, numReferencePhrases, numTestPhrases, sentScore[allChunks]['correct'])

    for key in sorted(sentScore.keys()):
        if sentScore[key]['numGuessed'] == 0:
            precision = 0.
        else:
            precision = sentScore[key]['correct']/sentScore[key]['numGuessed']
        if sentScore[key]['numCorrect'] == 0:
            recall = 0.
        else:
            recall = sentScore[key]['correct']/sentScore[key]['numCorrect']
        if precision == 0. or recall == 0.:
            fmeasure = 0.
        else:
            fmeasure = (2*precision*recall/(precision+recall))
        if key == allChunks:
            print "accuracy: %6.2f%%; precision: %6.2f%%; recall: %6.2f%%; F1: %6.2f" % \
                (accuracyCorrect/numTokens * 100., precision*100., recall*100., fmeasure*100.)
        else:
            print "%17s: precision: %6.2f%%; recall: %6.2f%%; F1: %6.2f; found: %6d; correct: %6d" % \
                (key, precision*100., recall*100., fmeasure*100., sentScore[key]['numGuessed'], sentScore[key]['numCorrect'])
    return fmeasure*100.

if __name__ == '__main__':
    optparser = optparse.OptionParser()
    optparser.add_option("-t", "--testfile", dest="testfile", default=None, help="output from your chunker program")
    optparser.add_option("-r", "--referencefile", dest="referencefile", default=os.path.join("data", "reference250.txt"), help="reference chunking")
    optparser.add_option("-n", "--numfeatures", dest="numfeats", default=2, help="number of features, default is two: word and POS tag")
    optparser.add_option("-c", "--conlleval", action="store_true", dest="conlleval", default=False, help="behave like the conlleval perl script with a single testfile input that includes the true label followed by the predicted label as the last two columns of input in testfile or sys.stdin")
    optparser.add_option("-e", "--equalcheck", action="store_true", dest="equalcheck", default=False, help="check if reference and output from chunker are the same length")
    optparser.add_option("-b", "--boundary", dest="boundary", default="-X-", help="boundary label that can be used to mark the end of a sentence")
    optparser.add_option("-l", "--logfile", dest="logfile", default=None, help="log file name")
    optparser.add_option("-o", "--outsidelabel", dest="outside", default="O", help="chunk tag for words outside any labeled chunk")
    (opts, _) = optparser.parse_args()
    numfeats = int(opts.numfeats)
    if opts.logfile is not None:
        logging.basicConfig(filename=opts.logfile, filemode='w', level=logging.INFO)

    if opts.testfile is None:
        (test, reference) = readTestFile(sys.stdin)
    else:
        with open(opts.testfile) as f:
            (test, reference) = readTestFile(f)

    if not opts.conlleval:
        with open(opts.referencefile) as f:
            (reference, _) = readTestFile(f)

    print "Score: %.2f" % corpus_fmeasure(reference, test)
