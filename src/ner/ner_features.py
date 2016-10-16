
import string
import copy

# the NER feature generator 
class Ner_feat_gen():

	def __init__(self, wordlist):
		self.wl = wordlist
		self.per_list = self.loading_list('./ner/ned_PER_list.txt')
		self.loc_list = self.loading_list('./ner/ned_LOC_list.txt')
	
# function to check if the word contains a digit / dollar /exclamatory /hyphen	
	def contains_digits(self,s): 
		return any(char.isdigit() for char in s) 
	def contains_dollar(self,s):
	    return any(char =="$" for char in s)
	def contains_exclamatory(self,s):
	    return any(char =="!" for char in s)

	def contains_hyphen(self,s):
		return any(char=="-" for char in s)

# function to check if word contains upper case characters
	def contains_upper(self,s):
		return any(char.isupper() for char in s)
# function to check if word contains any punctuations
	def contains_punc(self,s):
		return any(char in string.punctuation for char in s)
# fucntion to check if word starts with capital letter
	def starts_capital(self,s):
	    if s[0].isupper():
	       return 1
	    else:
	       return 0 
# function to check if word ends with a period              
	def ends_with_period(self,s):
	    if s[:-1] == '.':
	       return 1
	    else :
	       return 0
# function to check is the word is in Upper case              
	def all_upper(self,s):
	    for k in s:
	        if not k.isupper():
	            return 0
	    return 1
# function tp check if the word has an internal period/apostrophe/amphasand	        
	def contains_internal_period(self,s):
	    return any(char=='.' for char in s)
            
	def has_internal_apostrophe(self,s):
	    return any(char=="'" for char in s)
         
	def contains_hyphen(self,s):
	    return any(char=="-" for char in s)
		         
	def contains_amphasand(self,s):
		return any(char=="&" for char in s)  
    
# function to check if word contains both upper and lower characters    
	def contains_upper_lower(self,s):
	    return (any(char.isupper() for char in s) and any(char.islower() for char in s))
        
#function to check if the word is alphanumeric 
	def contains_alphanumeric(self,s):
	    return any(char.isalnum() for char in s)

# this function checks is all word contains only digits
	def contains_all_num(self,s):
	    for x in s:
	        if not x.isdigit():
	            return 0
	    return 1
        
	def contains_digits(self,s):
		return any(char.isdigit() for char in s)

# checking if the word is of the formn .X where x is any alphabet
	def containsPInitial(self,s):
	    if len(s) == 2:
	    	if s[0] == '.' and s[1].isalpha():
			print s
			return 1
	    	return 0

	def contains_hyphen(self,s):
		return any(char=="-" for char in s)

	def contains_all_upper(self,s):
	    x =[char for char in s if s.isdigit()]
	    return len(x)

	def contains_upper(self,s):
	    return any(char.isupper() for char in s)

# function to replace all digits in a word with 'D'

	def lexical_f(self,s):
	    for i in s:
	        if i.isdigit():
	            s = s.replace(i,"D")
	    return s

	def list_PER_isPresent(self,s):
	    y = '\'s'
	    if s != y:
	        if s in self.per_list:
	            return 1
	    return 0

# function to generate ortho features	

	def ortho_feature_alphanumeric(self,s):
	    for i in s:
	        if i.isdigit():
	            s = s.replace(i,"D")
	        elif i.isalpha():
	            s = s.replace(i,"A")
	    return s

# function to check is all charcters are in lower case	    
	def all_lower(self,s):
	    for i in s:
	        if not i.islower():
	            return 0
	    return 1

	def possesive_feature(self,s):
	    y = '\'s'
	    if s == y :
		#print y
		return 1
	    return 0
# function to perform binary search in a gazatteer
	def binarySearch(self,item,alist):
	    first = 0
	    last = len(alist)-1
	    found = False
	
	    while first<=last and not found:
	        midpoint = (first + last)//2
	        if alist[midpoint] == item:
	            found = True
	        else:
	            if item < alist[midpoint]:
	                last = midpoint-1
	            else:
	                first = midpoint+1
	
	    return found
    
	def loading_list(self,list_file):
	    c = open(list_file,'r')
	    alist = []
	    for line in c:
    	        x = line.split()
    	        alist.append(x[1])
	    c.close()
	    return alist

# main function used to obtain the features of a word   
               	
	def get_ner_feature(self,fv, i, pretag_1, pretag_2,pos_list,chunk_list):
		word = self.wl[i]
		if self.all_upper(word):
		    fv.append((1,'cur_upper'))
		if self.all_upper(self.wl[i-1]):
		    fv.append((2,'prev_upper'))
		if self.all_upper(self.wl[i-2]):
		    fv.append((3,'prev_prev_upper'))
		if self.all_upper(self.wl[i+1]):
		    fv.append((4,'after_upper'))
		if self.all_upper(self.wl[i+2]):
		    fv.append((5,'after_after_upper'))
		fv.append((6,'previous_2_tag',pretag_1, pretag_2))
		fv.append((7,'previous+cur',pretag_1,pretag_2,word))
		fv.append((8,'cur',word))
		fv.append((9,'prev',self.wl[i-1]))
		fv.append((10,'prev_prev',self.wl[i-2]))
		fv.append((11,'after',self.wl[i+1]))
		fv.append((12,'after_after',self.wl[i+2]))
		fv.append((13,self.wl[i-2],self.wl[i-1],word,self.wl[i+1],self.wl[i+2]))
		if self.starts_capital(word):
		    fv.append((14,'cur_cap'))
		if self.starts_capital(self.wl[i-1]):
		    fv.append((15,'prev_cap'))
		if self.starts_capital(self.wl[i-2]):
		    fv.append((16,'prev_prev_cap'))
		if self.starts_capital(self.wl[i+1]):
		    fv.append((17,'after_cap'))
		if self.starts_capital(self.wl[i+2]):
		    fv.append((18,'after_after_cap'))
		    
		fv.append((19,word[:1]))
		fv.append((20,word[-1:]))
		fv.append((21,word[:2]))
		fv.append((22,word[-2:]))
		fv.append((23,word[:3]))
		fv.append((24,word[-3:]))
		fv.append((25,word[:4]))
		fv.append((26,word[-4:]))
                fv.append((29,len(word)))
		fv.append((30,i))
		if self.possesive_feature(word):
		    fv.append((36,pretag_1))
		    fv.append((37,pos_list[i-1]))
		
		fv.append((27,pos_list[i]))
		fv.append((28,chunk_list[i]))
		
		if self.contains_all_num(word):
		    fv.append((29,'all_digits'))
		if self.contains_digits(word):
		    if self.contains_hyphen(word):
		        fv.append((30,'digits_punc'))
		    elif self.contains_internal_period(word):
		        fv.append((31,'digits_punc'))
		    elif self.has_internal_apostrophe(word):
		        fv.append((32,'digits_punc'))
		    elif self.contains_internal_period(word):
		        fv.append((33,'digits_punc'))
		    elif self.contains_amphasand(word):
		        fv.append((34,'digits_punc'))      
		if self.contains_alphanumeric(word) and self.contains_hyphen(word):
		    fv.append((35,'alphanum_hyphen')) 
		if self.binarySearch(word,self.per_list):
		    fv.append((38,'PER_list'))		
		if self.binarySearch(word,self.loc_list):
		    fv.append((39,'LOC_list'))  
		fv.append((40,self.wl[i-1],word))
		fv.append((41,word,self.wl[i+1]))
		if self.all_lower(word):
		    fv.append((42,'islower'))
		if self.contains_hyphen(word):
		    fv.append((43,'hyphen'))
		#if self.starts_capital(word):
		 #   fv.append((44,'caps'))    
		#if self.containsPInitial(word):
		 #   fv.append((36,'Initials'))    
		'''
		fv.append((36,pos_list[i-1],pos_list[i-2]))
		'''

# function to update those weights whose features match 
	
	def get_sent_feature(self, fv, nerlist,pos_list,chunk_list):
		for i in range(3, len(self.wl)-2):
			word = self.wl[i]
			tag = nerlist[i]
			if self.all_upper(word):
			    fv[(1,'cur_upper'),tag]+=1
			if self.all_upper(self.wl[i-1]):
			    fv[(2,'prev_upper'),tag]+=1
			if self.all_upper(self.wl[i-2]):
			    fv[(3,'prev_prev_upper'),tag]+=1
			if self.all_upper(self.wl[i+1]):
			    fv[(4,'after_upper'),tag]+=1
			if self.all_upper(self.wl[i+2]):
			    fv[(5,'after_after_upper'),tag]+=1
			fv[(6,'previous_2_tag',nerlist[i-1], nerlist[i-2]),tag]+=1
			fv[(7,'previous+cur',nerlist[i-1],nerlist[i-2],word),tag]+=1
			
			fv[(8,'cur',word),tag]+=1
			fv[(9,'prev',self.wl[i-1]),tag]+=1
			fv[(10,'prev_prev',self.wl[i-2]),tag]+=1
			fv[(11,'after',self.wl[i+1]),tag]+=1
			fv[(12,'after_after',self.wl[i+2]),tag]+=1
			fv[(13,self.wl[i-2],self.wl[i-1],word,self.wl[i+1],self.wl[i+2]),tag]+=1
			
			if self.starts_capital(word):
			    fv[(14,'cur_cap'),tag]+=1
			if self.starts_capital(self.wl[i-1]):
			    fv[(15,'prev_cap'),tag]+=1
			if self.starts_capital(self.wl[i-2]):
			    fv[(16,'prev_prev_cap'),tag]+=1
			if self.starts_capital(self.wl[i+1]):
			    fv[(17,'after_cap'),tag]+=1
			if self.starts_capital(self.wl[i+2]):
			    fv[(18,'after_after_cap'),tag]+=1
			    
			fv[(19,word[:1]),tag]+=1
			fv[(20,word[-1:]),tag]+=1
			fv[(21,word[:2]),tag]+=1
			fv[(22,word[-2:]),tag]+=1
			fv[(23,word[:3]),tag]+=1
			fv[(24,word[-3:]),tag]+=1
			fv[(25,word[:4]),tag]+=1
			fv[(26,word[-4:]),tag]+=1
                        fv[(29,len(word)),tag]+=1
			fv[(30,i),tag]+=1
			if self.possesive_feature(word):
			    fv[(36,nerlist[i-1]),tag]+=1
			    fv[(37,pos_list[i-1]),nerlist[i-1]]+=1
			
			fv[(27,pos_list[i]),tag]+=1
			fv[(28,chunk_list[i]),tag]+=1
			fv[(32,pos_list[i-1],pos_list[i]),tag]+=1
			fv[(33,chunk_list[i-1],chunk_list[i]),tag]+=1
			
			if self.contains_all_num(word):
			    fv[(29,'all_digits'),tag]+=1    
			if self.contains_digits(word):
			    if self.contains_hyphen(word):
			        fv[(30,'digits_punc'),tag]+=1
			    elif self.contains_internal_period(word):
			        fv[(31,'digits_punc'),tag]+=1
			    elif self.has_internal_apostrophe(word):
			        fv[(32,'digits_punc'),tag]+=1
			    elif self.contains_internal_period(word):
			        fv[(33,'digits_punc'),tag]+=1
			    elif self.contains_amphasand(word):
			        fv[(34,'digits_punc'),tag]+=1        
			if self.contains_alphanumeric(word) and self.contains_hyphen(word):
			    fv[(35,'alphanum_hyphen'),tag]+=1 
			if self.binarySearch(word,self.per_list):
			    fv[(38,'PER_list'),tag]+=1
			if self.binarySearch(word,self.loc_list):
			    fv[(39,'LOC_list'),tag]+=1
			fv[(40,self.wl[i-1],word),tag]+=1
			fv[(41,word,self.wl[i+1]),tag]+=1
			if self.all_lower(word):
			    fv[(42,'islower'),tag]+=1
			if self.contains_hyphen(word):
			    fv[(43,'hyphen'),tag]+=1
			#if self.starts_capital(word):
			 #   fv[(44,'caps'),tag]+=1    
			#if self.containsPInitial(word):
			 #   fv[(36,'Inititals'),'I-PER']+=1
			'''
			fv[(36,pos_list[i-1],pos_list[i-2]),tag]+=1
			'''
            
