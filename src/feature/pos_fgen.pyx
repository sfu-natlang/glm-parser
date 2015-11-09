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


    