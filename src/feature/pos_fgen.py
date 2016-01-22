import feature_vector
import feature_generator_base
import debug.debug
import copy


class Pos_feat_gen():
	def __init__(self, wordlist):
		self.wl = wordlist
		#self.taglist = taglist
	def contains_digits(self,s):
		return any(char.isdigit() for char in s)
	def contains_hyphen(self,s):
		return any(char=="-" for char in s)
	def contains_upper(self,s):
		return any(char.isupper() for char in s)
	'''
	def get_pos_feature(self,fv, i, pretag_1, pretag_2):
	    fv.append((0,self.wl[i]))
	    fv.append((1,self.wl[i-1]))
	    fv.append((2,self.wl[i-2]))
	    fv.append((3,self.wl[i+1]))
	    fv.append((4,self.wl[i+2]))
	    fv.append((5,self.wl[i][:1]))
	    fv.append((6,self.wl[i][:2]))
	    fv.append((7,self.wl[i][:3]))
	    fv.append((8,self.wl[i][:4]))
	    fv.append((9,self.wl[i][-1:]))
	    fv.append((10,self.wl[i][-2:]))
	    fv.append((11,self.wl[i][-3:]))
	    fv.append((12,self.wl[i][-4:]))
	    fv.append((13,pretag_1))
	    fv.append((14,pretag_1,pretag_2))
	    if(self.contains_digits(self.wl[i])):
	        fv.append((15,"hasNumber"))
	    if(self.contains_hyphen(self.wl[i])):
	        fv.append((16,"hasHyphen"))
	    if(self.contains_upper(self.wl[i])):
	        fv.append((17,"hasUpperCase"))
	'''
	def get_sent_pos_feature(self, fv, poslist):
		for i in range(2, len(poslist)):
			word = self.wl[i]
			tag = poslist[i]
		    fv[(0,word)]+=1
		    fv[(1,self.wl[i-1]),tag]+=1
		    fv[(2,self.wl[i-2]),tag]+=1
		    fv[(3,self.wl[i+1]),tag]+=1
		    fv[(4,self.wl[i+2]),tag]+=1
		    fv[(5,word[:1]),tag]+=1
		    fv[(6,word[:2]),tag]+=1
		    fv[(7,word[:3]),tag]+=1
		    fv[(8,word[:4]),tag]+=1
		    fv[(9,word[-1:]),tag]+=1
		    fv[(10,word[-2:]),tag]+=1
		    fv[(11,word[-3:]),tag]+=1
		    fv[(12,word[-4:]),tag]+=1
		    fv[(13,poslist[i-1],tag)]+=1
		    fv[(14,poslist[i-1],poslist[i-2]),tag]+=1
		    if(self.contains_digits(word)):
		        fv[(15,"hasNumber"),tag]+=1
		    if(self.contains_hyphen(word)):
		        fv[(16,"hasHyphen"),tag]+=1
		    if(self.contains_upper(word)):
		        fv[(17,"hasUpperCase"),tag]+=1


    