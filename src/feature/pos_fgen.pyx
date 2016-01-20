import feature_vector
import feature_generator_base
import debug.debug
import string
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
	def contains_punc(self,s):
		return any(char in string.punctuation for char in s)
	def get_pos_feature(self,fv, i, pretag_1, pretag_2):
		word = self.wl[i]
		fv.append((0,word))
		fv.append((1,self.wl[i-1]))
		fv.append((2,self.wl[i-2]))
		fv.append((3,self.wl[i+1]))
		fv.append((4,self.wl[i+2]))
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
		if self.contains_upper(word):
			fv.append((17,"hasUpperCase"))
		elif word.islower():
			fv.append((18,"lowerCase"))
		if self.contains_punc(word):
			fv.append((19,"hasPunctuation"))

    