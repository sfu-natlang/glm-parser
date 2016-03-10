
import string
import copy


class Pos_feat_gen():

	def __init__(self, wordlist):
		self.wl = wordlist

	def contains_digits(self,s):
		return any(char.isdigit() for char in s)

	def contains_hyphen(self,s):
		return any(char=="-" for char in s)

	def contains_upper(self,s):
		return any(char.isupper() for char in s)

	def contains_punc(self,s):
		return any(char in string.punctuation for char in s)
	
	def get_pos_feature(self,fv, i, pretag_1, pretag_2):
		word = self.wl[i].lower()
		fv.append((0,word))
		fv.append((1,self.wl[i-1].lower()))
		fv.append((2,self.wl[i-2].lower()))
		fv.append((3,self.wl[i+1].lower()))
		fv.append((4,self.wl[i+2].lower()))
		fv.append((5,word[:1]))
		fv.append((6,word[-1:]))
		if len(word)>=2:
			fv.append((7,word[:2]))
			fv.append((8,word[-2:]))
		if len(word)>=3:
			fv.append((9,word[:3]))
			fv.append((10,word[-3:]))
		if len(word)>=4:
			fv.append((11,word[:4]))
			fv.append((12,word[-4:]))
		fv.append((13,pretag_1))
		fv.append((14,pretag_2,pretag_1))
		if self.contains_digits(word):
			fv.append((15,"hasNumber"))
		if self.contains_hyphen(word) :
			fv.append((16,"hasHyphen"))
		if self.contains_upper(self.wl[i]):
			fv.append((17,"hasUpperCase"))
		fv.append((18,pretag_2))
		fv.append((19,self.wl[i-1].lower()[-3:]))
		fv.append((20,self.wl[i+1].lower()[-3:]))

	
	def get_sent_feature(self, fv, poslist):
		for i in range(3, len(self.wl)-2):
			word = self.wl[i].lower()
			tag = poslist[i]
			fv[(0,word),tag]+=1
			fv[(1,self.wl[i-1].lower()),tag]+=1
			fv[(2,self.wl[i-2].lower()),tag]+=1
			fv[(3,self.wl[i+1].lower()),tag]+=1
			fv[(4,self.wl[i+2].lower()),tag]+=1
			fv[(5,word[:1]),tag]+=1
			fv[(6,word[-1:]),tag]+=1
			if len(word)>=2:
				fv[(7,word[:2]),tag]+=1
				fv[(8,word[-2:]),tag]+=1
			if len(word)>=3:
				fv[(9,word[:3]),tag]+=1
				fv[(10,word[-3:]),tag]+=1
			if len(word)>=4:
				fv[(11,word[:4]),tag]+=1
				fv[(12,word[-4:]),tag]+=1
			fv[(13,poslist[i-1],tag)]+=1
			fv[(14,poslist[i-2],poslist[i-1]),tag]+=1
			if self.contains_digits(word):
				fv[(15,"hasNumber"),tag]+=1
			if self.contains_hyphen(word):
				fv[(16,"hasHyphen"),tag]+=1
			if self.contains_upper(self.wl[i]):
				fv[(17,"hasUpperCase"),tag]+=1
			fv[(18,poslist[i-2]),tag]+=1
			fv[(19,self.wl[i-1].lower()[-3:]),tag]+=1
			fv[(20,self.wl[i+1].lower()[-3:]),tag]+=1

    