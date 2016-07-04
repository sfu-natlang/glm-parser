
import string
import copy


class Ner_feat_gen():

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
	def contains_internal_period(self,s):
            return any(char =='.' for char in s)
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
        
	def sent_feat_gen(self, fv, sent, tags, pos_tags, chunking_tags):
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
	            fv[(1,'TAG',word),tag]+=1
	            fv[(2,'PREFIX',word[:3]),tag]+=1
	            fv[(3,'SUFFIX',word[-3:]),tag]+=1
	            fv[(4,'BIGRAM',tags[i-1],tag)]+=1
	            fv[(5,'TRIGRAM',tags[i-2],tags[i-1]),tag]+=1
	            
            
            
	            fv[(6,'PREFIX',word[:4]),tag]+=1
	            fv[(7,'SUFFIX',word[-4:]),tag]+=1
	            if self.contains_upper(word):
	                fv[(8,'HasUpperCase'),tag]+=1
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
	                fv[(9,'start_capital'),tag]+=1
	            if self.all_upper(word):
	                fv[(10,'all_capital'),tag]+=1
	            if self.contains_upper_lower(word):
	                fv[(11,'upper&lower'),tag]+=1
	                
                
	            #internal characters
	            if self.has_internal_apostrophe(word):
	                fv[(12,'has_internal_characters'),tag]+=1
	                #print word
	            if self.contains_hyphen(word):
	                fv[(13,'contains_hyphen'),tag]+=1
	                #print word
	                if self.contains_amphasand(word):
	                    fv[(14,'contains_amphasand'),tag]+=1 
	                #print word  
	                
                
	            if self.contains_alphanumeric(word):
	                fv[(15,'has_alnum'),tag]+=1
	            if self.contains_all_num(word):
	                fv[(16,'has_all_digits'),tag]+=1
	                #lexical features
	                l_word = self.lexical_f(word)
	                fv[(22,'l_feature',l_word),tag]+=1
	            if self.contains_all_upper(word):
	                fv[(17,'has_all_capital'),tag]+=1
                
	            fv[(18,'relative_pos',i),tag]+=1
	            fv[(19,'relative_word_postion',word,i),tag]+=1
	            if self.ends_with_period(word):
	                fv[(20,'ends_with_period'),tag]+=1
	            fv[(21,'word_len',len(word)),tag]+=1
	            if self.contains_internal_period(word):
	                fv[(23,'conatins_int_period'),tag]+=1 
	                 
	def get_ner_features(self,fv, i, pretag_1, pretag_2, sent):
	        word = sent[i]
	        fv.append((1,'TAG',word))
	        fv.append((2,'PREFIX-3',word[:3]))
	        fv.append((3,'SUFFIX-3',word[-3:]))
	        fv.append((4,'BIGRAM',pretag_1))
	        fv.append((5,'TRIGRAM',pretag_2,pretag_1))
	        fv.append((6,'PREFIX-4',word[:4]))
	        fv.append((7,'SUFFIX-4',word[-4:]))
	        if self.contains_upper(word):
	            fv.append((8,'HasUpperCase'))
	        if self.starts_capital(word):
	            fv.append((9,'start_capital'))
	        if self.all_upper(word):
	            fv.append((10,'all_capital'))
	            
	        if self.contains_upper_lower(word):
	            fv.append((11,'upper&lower'))
	        if self.has_internal_apostrophe(word):
	            fv.append((12,'has_internal_characters'))
	        if self.contains_hyphen(word):
	            fv.append((13,'contains_hyphen'))
	        if self.contains_amphasand(word):
	            fv.append((14,'contains_amphasand'))
	        if self.contains_internal_period(word):
	            fv.append((23,'conatins_int_period'))  
	        if self.contains_alphanumeric(word):
	            fv.append((15,'has_alnum'))
	        if self.contains_all_num(word):
	            fv.append((16,'has_all_digits'))
	            l_word = self.lexical_f(word)
	            fv.append((22,'l_feature',l_word))
	        if self.contains_all_upper(word):
	            fv.append((17,'has_all_capital'))
	     
	        fv.append((18,'relative_pos',i))
	        fv.append((19,'relative_word_postion',word,i))
	        fv.append((21,'word_len',len(word)))
	        if self.ends_with_period(word):
	            fv.append((20,'ends_with_period'))
