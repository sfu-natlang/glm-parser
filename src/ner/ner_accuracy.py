from __future__ import division
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import ner_viterbi
import time

class Decoder():
    def __init__(self, test_list=None):
        self.test_list = test_list

    def get_accuracy(self):
        f = open(self.test_list,'r')
	total_Ner = 0
	correct_identified_Ner = 0
	for line in f:
    		x = line.split()	
    		if not x:
       			continue
   		else:
			total_Ner = total_Ner + 1
			if x[2] == x[3]:
				correct_identified_Ner = correct_identified_Ner + 1
	#print correct_identified_Ner
	#print "\n"
	#print total_Ner
        acc = correct_identified_Ner/total_Ner
	print "accuracy is"+str(acc) 	
	f.close()

