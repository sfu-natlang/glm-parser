import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
import pos_viterbi, pos_common
import time

class Decoder():
    def __init__(self, test_list=None, tag_file="pos_tagset.txt"):
        self.test_list = test_list
        self.tagset = pos_common.read_tagset(tag_file)

    def sent_evaluate(self, result_list, gold_list):
        result_size = len(result_list)
        gold_size = len(gold_list)
        if(result_size!=gold_size):
            raise ValueError("TAGGER [ERRO]: Tag results do not align with gold results")
        correct_num = 0
        for i in range(result_size):
            if result_list[i] == gold_list[i]:
                correct_num += 1
        return correct_num, gold_size

    def get_accuracy(self, w_vec):
        argmax = pos_viterbi.Viterbi()
        correct_num = gold_set_size = 0
	y = ['_B_-1','_B_-2','_B_+1','_B_+2']
	f = open('./pos/output.txt','w')
        for (word_list, pos_list, fv) in self.test_list:
            output = argmax.perc_test(w_vec,word_list,self.tagset,"NN")
	    x= len(word_list)
            for n in range(0,x):
                x= len(word_list)
            for n in range(0,x):
                if word_list[n] not in y: 
                #print word_list[n] +"\t"+ pos_list[n] +"\t"+chunk_list[n]+"\t"+ner_list[n]+"\t"
                    f.write("%s %s\n" % (word_list[n], pos_list[n]))
            f.write("\n")
            cnum, gnum = self.sent_evaluate(output,pos_list)
            correct_num += cnum
            gold_set_size += gnum
        acc = float(correct_num) /gold_set_size
        print "TAGGER [INFO]: Total Accraccy: ", acc
        return acc
