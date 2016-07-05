
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
	            if self.ortho_feature_alphanumeric(word):    
	            	fv[('ortho_feature',word),tag]+=1
		 
	                # special features
	            if self.ends_with_period(word):
	                fv[('ends_with_period'),tag]+=1
	            
            

