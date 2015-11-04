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
	'''
	def get_sent_pos_feature(self, fv, poslist):
		nwl = copy.deepcopy(self.wl)
		npl = copy.deepcopy(poslist)
		nwl[0] = "_B-1"
		nwl.insert(0,"_B-2")
		nwl.append("_B+1")
		nwl.append("_B+2")
		npl[0] = "_B-1"
		npl.insert(0,"_B-2")
		for i in range(2, len(nwl)-2):
		    fv.append((0,nwl[i]))
		    fv.append((1,nwl[i-1]))
		    fv.append((2,nwl[i-2]))
		    fv.append((3,nwl[i+1]))
		    fv.append((4,nwl[i+2]))
		    fv.append((5,nwl[i][:1]))
		    fv.append((6,nwl[i][:2]))
		    fv.append((7,nwl[i][:3]))
		    fv.append((8,nwl[i][:4]))
		    fv.append((9,nwl[i][-1:]))
		    fv.append((10,nwl[i][-2:]))
		    fv.append((11,nwl[i][-3:]))
		    fv.append((12,nwl[i][-4:]))
		    #fv.append((13,npl[i-1]))
		    #fv.append((14,npl[i-1],npl[i-2]))
		    if(self.contains_digits(nwl[i])):
		        fv.append((15,"hasNumber"))
		    if(self.contains_hyphen(nwl[i])):
		        fv.append((16,"hasHyphen"))
		    if(self.contains_upper(nwl[i])):
		        fv.append((17,"hasUpperCase"))
	'''


    