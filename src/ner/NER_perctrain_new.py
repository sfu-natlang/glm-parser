#! /usr/bin/python
from __future__ import division
import sys
import ner_viterbi
import time,copy,logging
import os,sys,inspect
from collections import defaultdict


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from weight import weight_vector

# Debug output flag
debug = False
fileptr = open('log_feature_generator.txt','w')



class Trainer:
    def __init__(self,w_vector=None):
        self.tags = set()
        #self.weight_vec = defaultdict(float)
        self.sentences = []
        self.ner_tags = []
        self.pos_tags = []
        self.chunking_tags = []
        self.w_vector = w_vector
        self.list_LOC = []
        self.list_PER = []

    def read_training_data(self, training_file):
        """
        Read the conll2003 english training file
        :param training_file: the path of the training file
        """
        if debug: sys.stdout.write("Reading training data...\n")

        file = open(training_file, 'r')
        # file.seek(0) sets the file's current reading position at offset 0
        file.seek(0)
        sentence = []
        tags = []
        pos_tag = []
        chunking_tag = []
        for line in file:
            #String.strip([chars]);
            #returns a copy of the string in which all chars have been stripped from the beginning and the end of the string.
            #e.g str = "0000000this is string example....wow!!!0000000"; 
            #    print str.strip( '0' )
            # answer: this is string example....wow!!!
            line = line.strip()
            if line: # Non-empty line
                #method split() returns a list of all the words in the string, using a delimiter (splits on all whitespace if left unspecified)
                token = line.split()
                word = token[0]
                tag  = token[3]
                p_tag = token[1]
                ch_tag = token[2]
                #appends the word at the end of the list
                sentence.append(word)
                #appends the tag at the end of the list
                tags.append(tag)
                pos_tag.append(p_tag)
                chunking_tag.append(ch_tag)
                
            else: # End of sentence reached
                #converts the sentence list to a tuple and then appends that tuple to the end of the self.x list
                self.sentences.append(tuple(sentence))
                self.ner_tags.append(tuple(tags))
                self.pos_tags.append(tuple(pos_tag))
                self.chunking_tags.append(tuple(chunking_tag))
                #set object is an unordered collection of items and don't have duplicate items
                #set.update(other, ...)
                #Update the set, adding elements from all others
                # so self.tags.update(tags) keeps only the distinct # of tags for that sentence
                self.tags.update(tags)
                sentence = []
                tags = []
                pos_tag = []
                chunking_tag = []
        file.close()

    def contains_upper(self,s):
        return any(char.isupper() for char in s)
   
    # all case features

    def starts_capital(self,s):
        if s[0].isupper():
           return 1
        else:
           return 0 
              
    def ends_with_period(self,s):
        if s[:-1] == '.':
            return 1
        else :
            return 0
              
    def all_upper(self,s):
        for s in s:
            if not s.isupper():
               return 0
        return 1
    
    def has_internal_apostrophe(self,s):
        return any(char =="'" for char in s)
         
    def contains_hyphen(self,s):
        return any(char=="-" for char in s)
		         
    def contains_amphasand(self,s):
	    return any(char=="&" for char in s)  
    
    
    def contains_upper_lower(self,s):
        return (any(char.isupper() for char in s) and any(char.islower() for char in s))
        
    def contains_alphanumeric(self,s):
        return any(char.isalnum() for char in s)

    def contains_all_num(self,s):
        x =[char for char in s if s.isdigit()]
        return len(x)
         
    def contains_digits(self,s):
		return any(char.isdigit() for char in s)

    def contains_hyphen(self,s):
		return any(char=="-" for char in s)

    def contains_all_upper(self,s):
        x =[char for char in s if s.isdigit()]
        return len(x)

    def contains_upper(self,s):
        return any(char.isupper() for char in s)

    def lexical_f(self,s):
        for i in s:
            if i.isdigit():
                s = s.replace(i,"D")
        return s
        
             
    def LOC_list_formation(self):
        fileptr = open('ned.list.LOC','r')
        for line in fileptr:
            x = line.split()
            self.list_LOC.append(x)
        print self.list_LOC
        fileptr.close()
        
    def PER_list_formation(self):
        fileptr = open('ned.list.PER','r')
        for line in fileptr:
            x = line.split()
            self.list_PER.append(x)
        #print self.list_PER
        fileptr.close()
   
   
    def list_PER_isPresent(self,s):
        y = '\'s'
        if s != y:
            for per in self.list_PER: 
                if s in per:
                #print s+"\n"
                    return 1
               
            return 0
                    
    def list_LOC_isPresent(self,s):
        y = '\'s'
        if s != y:
            for loc in self.list_LOC:
                if s in self.list_LOC:
                #print s+"\n"
                    return 1
                #print s+"\n"
            return 0
            
    def ortho_feature_alphanumeric(self,s):
        for i in s:
            if i.isdigit():
                s = s.replace(i,"D")
            elif i.isalpha():
                s = s.replace(i,"A")
        return s
        
    def sent_feat_gen(self, fv, sent, tags, pos_tags,chunking_tags):
        #fileptr.write("...........................\n")
        #fileptr.write("%s\n" %(sent))
        for i in range(3, len(sent)-2):
            word = sent[i]
            tag = tags[i]
            #if word != "the":
            #	fileptr.write("word is %s\n" %(word))
            # 	fileptr.write("tag is %s\n" %(tag))
            #fileptr.write("word is %s\n" %(word))
            #fileptr.write("tag is %s\n" %(tag))
            y = '\'s'
            if word == y:
                fv[('apostrophere-word',tags[i-1],word,sent[i-1]),tag]+=1
                #print word
            fv[('TAG',word),tag]+=1
            fv[('PREFIX',word[:3]),tag]+=1
            fv[('SUFFIX',word[-3:]),tag]+=1
            fv[('BIGRAM',tags[i-1],tag)]+=1
            fv[('TRIGRAM',tags[i-2],tags[i-1]),tag]+=1
            
            
            
            fv[('PREFIX',word[:4]),tag]+=1
            fv[('SUFFIX',word[-4:]),tag]+=1
            if self.contains_upper(word):
                fv[('HasUpperCase'),tag]+=1
                #if word != "the":
                #	fileptr.write("feature tag is %s\n" %(fv[('TAG',word),tag]))
                #	fileptr.write("feature prefix is %s\n" %(fv[('PREFIX',word[:3]),tag]))
                #	fileptr.write("feature suffic is %s\n" %(fv[('SUFFIX',word[-3:]),tag]))
                #fileptr.write("feature tag is %s\n" %(fv[('TAG',word),tag]))
            #fileptr.write("feature prefix is %s\n" %(fv[('PREFIX',word[:3]),tag]))
            #fileptr.write("feature suffic is %s\n" %(fv[('SUFFIX',word[-3:]),tag]))
            #print fv
       
            # case features 
            if self.starts_capital(word):
                fv[('start_capital'),tag]+=1
            if self.all_upper(word):
                fv[('all_capital'),tag]+=1
            if self.contains_upper_lower(word):
                fv[('upper&lower'),tag]+=1
                
                
            #internal characters
            if self.has_internal_apostrophe(word):
                fv[('has_internal_characters'),tag]+=1
                #print word
            if self.contains_hyphen(word):
                fv[('contains_hyphen'),tag]+=1
                #print word
                if self.contains_amphasand(word):
                    fv[('contains_amphasand'),tag]+=1 
                #print word  
                
                
            if self.contains_alphanumeric(word):
                fv[('has_alnum'),tag]+=1
            if self.contains_all_num(word):
                fv[('has_all_digits'),tag]+=1
                #lexical features
                l_word = self.lexical_f(word)
                fv[(l_word),tag]+=1
            if self.contains_all_upper(word):
                fv[('has_all_capital'),tag]+=1
                
            fv[('relative_pos',i),tag]+=1
            fv[('relative_word_postion',word,i),tag]+=1
            
            
            fv[('PREFIX',word[:1]),tag]+=1
            fv[('SUFIX',word[-1:]),tag]+=1
            fv[('PREFIX',word[:2]),tag]+=1
            fv[('SUFIX',word[-2:]),tag]+=1
            fv[('pretag_1',word),tags[i-1]]+=1
            fv[('pretag_2',word,tag),tags[i-1]]+=1
                #pos tag
            fv[("pos_tag",pos_tags[i]),tag]+=1
            fv[("chunking_tag",chunking_tags[i]),tag]+=1
                
                #new features 
            
            fv[('window-3',word,sent[i-1],sent[i+1]),tag]+=1
            fv[('window-5',word,sent[i-1],sent[i-2],sent[i+1],sent[i+2]),tag]+=1
            
            
                #present in LOC list
                #present in PER list
            #ans = self.list_LOC_isPresent(word)
            #if ans == 'present':
            #    fv[('LOC_list_f1',word,sent[i-1],sent[i+1]),tag]+=1
            #    fv[('LOC_list_f2'),tag]+=1
                
            #ans = self.list_PER_isPresent(word)
            #if ans == 'present':
            #    fv[('PER_list_f1',word,sent[i-1],sent[i+1]),tag]+=1
            #    fv[('PER_list_f2'),tag]+=1
                
            fv[('ortho_feature',word,self.ortho_feature_alphanumeric(word)),tag]+=1
		 
                # special features
            if self.ends_with_period(word):
                fv[('ends_with_period'),tag]+=1
            
            
    def reset_weights(self):
        """
        Reset all the weights to zero in the weight vector.
        """
        for feature in self.weight_vec:
            self.weight_vec[feature] = 0


    def perceptron_algorithm(self, iterations):
        """
        Run the perceptron algorithm to estimate (or improve) the weight vector.
        """
        weight_vec = defaultdict(float)
        #self.reset_weights()
        num_updates = 0
        avg_vec = defaultdict(float)
        feat_count = defaultdict(int)
        last_iter = {}
        num_updates = 0
        argmax = ner_viterbi.Viterbi()
        for iteration in range(iterations):
            num_mistakes = 0
            for i in range(len(self.sentences)):
                #list(self.x[i]) converts the given tuple into a list.
                sentence = list(self.sentences[i])
                #list(self.y[i]) converts the given sentence tuple into a list.
                tags = list(self.ner_tags[i])
                POS_tags = list(self.pos_tags[i])
                chunk_tags = list(self.chunking_tags[i])
                #chunk_tags = list(self.chunking_tags[i])
                # Find the best tagging sequence using the Viterbi algorithm
                predict_tags = argmax.perc_test(weight_vec, sentence, self.tags)
		fileptr.write("....................................\n")
		#fileptr.write("predicted tags%s\n" %(predict_tags))
                #fileptr.write(" actual tags%s\n" %(tags))
                num_updates += 1

                if predict_tags != tags:
                    num_mistakes += 1
                    labels = copy.deepcopy(sentence)
                    out_cp = copy.deepcopy(predict_tags)
                    tags_cp = copy.deepcopy(tags)

                    labels.insert(0, '_B_-1')
                    labels.insert(0, '_B_-2') # first two 'words' are B_-2 B_-1
                    labels.append('_B_+1')
                    labels.append('_B_+2') # last two 'words' are B_+1 B_+2

                    out_cp.insert(0,'B_-1')
                    out_cp.insert(0,'B_-2')

                    tags_cp.insert(0,'B_-1')
                    tags_cp.insert(0,'B_-2')
                    
                    POS_tags.insert(0,'B_-1')
                    POS_tags.insert(0,'B_-1')
                    
                    POS_tags.append('B_+1')
                    POS_tags.append('B_+1')
                    
                    chunk_tags.append('B_+1')
                    chunk_tags.append('B_+2')
                    
                    chunk_tags.insert(0,'B_+1')
                    chunk_tags.insert(0,'B_+2')

                    #pos_feat = pos_features.Pos_feat_gen(labels)

                    gold_out_fv = defaultdict(int)
                    self.sent_feat_gen(gold_out_fv,labels, tags_cp,POS_tags,chunk_tags)
                    #fileptr.write("gold_feat_gen%s\n" %(gold_out_fv))
                    cur_out_fv = defaultdict(int)
                    self.sent_feat_gen(cur_out_fv,labels, out_cp,POS_tags,chunk_tags)
                    #fileptr.write("cur_feat_gen%s\n" %(cur_out_fv))
                    feat_vec_update = defaultdict(int)

                    for feature in gold_out_fv:
			feat_vec_update[feature]+=gold_out_fv[feature]
                        feat_count[feature]+=gold_out_fv[feature]
			#fileptr.write("feature is %s\n" %str(feature))
			#fileptr.write("feat_vec_update due to gold_vec %s\n" %(feat_vec_update)
			#fileptr.write("feat_count%s\n" %(feat_count[feature]))
                    for feature in cur_out_fv:
                        feat_vec_update[feature]-=cur_out_fv[feature]
			#fileptr.write("feat_vec_update due to cur_vec %s\n" %(feat_vec_update)
		    #num_updates = number of times the featue_vectors have been updated = num_sentences*iterations
                    for upd_feat in feat_vec_update.keys():
                        if feat_vec_update[upd_feat] != 0:
                            weight_vec[upd_feat] += feat_vec_update[upd_feat]
                            if (upd_feat) in last_iter:
                                avg_vec[upd_feat] += (num_updates - last_iter[upd_feat]) * weight_vec[upd_feat]
                            else:
                                avg_vec[upd_feat] = weight_vec[upd_feat]
                            last_iter[upd_feat] = num_updates
		    #fileptr.write("last_iter%s\n" %(last_iter))
            
            print "number of mistakes:", num_mistakes, " iteration:", iteration+1
            #dump_vector("fv",round,weight_vec,last_iter,avg_vec, num_updates)
        #fileptr.write("%s\n" %(self.weight_vec))
        fileptr.close()
        for feat in weight_vec:
            if feat in last_iter:
                avg_vec[feat] += (num_updates - last_iter[feat]) * weight_vec[feat]
            else:
                avg_vec[feat] = weight_vec[feat]
            weight_vec[feat] = avg_vec[feat] / num_updates
        #print self.weight_vec
        self.dump_vector("NER", iterations, weight_vec)
        return weight_vec

    def dump_vector(self, filename, i, fv):
        w_vector = weight_vector.WeightVector()
        w_vector.data_dict.iadd(fv)
        w_vector.dump(filename + "_Iter_%d.db"%i)

    def tag_data(self, test_file, weight_vec):
	self.sentences = []
	self.pos_tags = []
	self.chunks = []
	self.ner_tags = []
	self.tags = set()
	argmax = ner_viterbi.Viterbi()
        infile = open(test_file, 'r')
        # file.seek(0) sets the file's current reading position at offset 0
        infile.seek(0)
        sentence = []
        pos_tag = []
        chunk = []
        ner_tag = []
        for line in infile:
            line = line.strip()
            if line: # Non-empty line
                #method split() returns a list of all the words in the string, using a delimiter (splits on all whitespace if left unspecified)
                token = line.split()
                word = token[0]
                ptag  = token[1]
                ctag = token[2]
                nertag = token[3]
                #appends the word at the end of the list
                sentence.append(word)
                pos_tag.append(ptag)
                chunk.append(ctag)

                #appends the tag at the end of the list
                ner_tag.append(nertag)
            else: # End of sentence reached
                #converts the sentence list to a tuple and then appends that tuple to the end of the self.x list
                self.sentences.append(tuple(sentence))
                self.pos_tags.append(tuple(pos_tag))
                self.chunks.append(tuple(chunk))
                self.ner_tags.append(tuple(ner_tag))
                self.tags.update(ner_tag)
                sentence = []
                pos_tag = []
                chunk = []
                ner_tag = []
        infile.close()

        target = open('out_file.txt', 'w')
        #log = open('log_file.text','w')
        for i in range(len(self.sentences)):
            sentence = list(self.sentences[i])
            pos_tag = list(self.pos_tags[i])
            ner_tag = list(self.ner_tags[i])
            #log.write("this is ner_tag %s\n" %(self.ner_tags))
            tags = argmax.perc_test(weight_vec, sentence, self.tags)
            #log.write("this is tag from perc_test %s\n" %(tags))
            for n in range(len(sentence)):
                target.write("%s %s %s %s\n" % (sentence[n], pos_tag[n], ner_tag[n], tags[n]))
            #print sentence[n] + pos_tag[n] + ner_tag[n] + tags[n]
            #print "\n"
            target.write("\n")

        target.close()
        #log.close()



def main(training_file):
    """
    """

    trainer = Trainer()
    #trainer.LOC_list_formation()
    #trainer.PER_list_formation()
    # Read the training data (x, y)
    trainer.read_training_data(training_file)

    # Compute the weight vector using the Perceptron algorithm
    w_vec  = trainer.perceptron_algorithm(1)
    print "evaluating"
    trainer.tag_data('eng.testa',w_vec)


def usage():
    sys.stderr.write("""
    Usage: python ner_training.py [training_file]\n
        Find the weight vector for ner tagging.\n""")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
    main(sys.argv[1])
    #main("eng.train")
