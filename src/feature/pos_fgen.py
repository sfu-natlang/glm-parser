import feature_vector
import feature_generator_base
import debug.debug
import copy


class Pos_feat_gen():
	def __init__(self, wordlist, taglist):
		self.wordlist = wordlist
		self.taglist = taglist
	def contains_digits(self,s):
		return any(char.isdigit() for char in s)
	def contains_hyphen(self,s):
		return any(char=="-" for char in s)
	def contains_upper(self,s):
		return any(char.isupper() for char in s)
	def get_pos_feature(self,fv):
		wl = copy.deepcopy(self.wordlist)
		#pl = copy.deepcopy(self.poslist) 
		wl[0] = "_B-1"
		wl.insert(0,"_B-2")
		wl.append("_B+1")
		wl.append("_B+2")
		feature_num = 0
		for i in range(2, len(wl)-2):
		    fv.append((0,wl[i]))
		    fv.append((1,wl[i-1]))
		    fv.append((2,wl[i-2]))
		    fv.append((3,wl[i+1]))
		    fv.append((4,wl[i+2]))
		    fv.append((5,wl[i][:1]))
		    fv.append((6,wl[i][:2]))
		    fv.append((7,wl[i][:3]))
		    fv.append((8,wl[i][:4]))
		    fv.append((9,wl[i][-1:]))
		    fv.append((10,wl[i][-2:]))
		    fv.append((11,wl[i][-3:]))
		    fv.append((12,wl[i][-4:]))
		    if(self.contains_digits(wl[i])):
		        fv.append((13,"hasNumber"))
		    if(self.contains_hyphen(wl[i])):
		        fv.append((14,"hasHyphen"))
		    if(self.contains_upper(wl[i])):
		        fv.append((15,"hasUpperCase"))
		    feature_index = 16
		    for j in self.taglist:
		    	fv.append((feature_index, j))
		    	feature_index += 1
		    for j in self.taglist:
		    	for k in self.taglist:
		    		fv.append((feature_index,j,k))
		    		feature_index += 1
		    feature_num += feature_index
		
		print feature_num

		return



    