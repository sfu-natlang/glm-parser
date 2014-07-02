from nltk.tree import *
import copy

class ConllTreeGenerator():
	def __init__(self):
		self.tree_list = []
		self.conll_list = []

		self.load_trees("../../../wsj/00/wsj_0001.mrg")
		self.load_conll("../../../penn-wsj-deps/00/wsj_0001.mrg.3.pa.gs.tab")
		return

	def generate_conll_tree(self):
		"""
			Assuming the order of sentences in ptree_list and conll_list are the same
		"""
		if not len(self.tree_list) == len(self.conll_list):
			print "Incompatible parsing tree and conll data !!!"
			return

		for i in range(len(self.conll_list)):
			sent_conll = self.conll_list[i]
			sent_tree = self.tree_list[i]

			for w in range(len(sent_conll)):
				# index not includes root
				head = sent_conll[w][2]-1
				modifier = w

				if head < 0:
					head_treeposition = ()
				else:
					head_treeposition = sent_tree.leaf_treeposition(head)
	
				modifier_treeposition = sent_tree.leaf_treeposition(modifier)
				subtree = sent_tree

				n = 0
				while n < len(head_treeposition) and head_treeposition[n] == modifier_treeposition[n]:
					subtree = subtree[modifier_treeposition[n]]
					n += 1
				
				#print n, modifier_treeposition[n:], subtree
				spine = self.get_spine(modifier_treeposition[n+1:], subtree[modifier_treeposition[n]])
				print spine


			sent_tree.draw()

	def get_spine(self, treeposition, tree):
		#print treeposition, tree
		# assume one word per pos tag
		if len(treeposition) == 1:
			return tree
		else:
			subpath = self.get_spine(treeposition[1:], tree[treeposition[0]])
			#print subpath
			return Tree(tree.node, [subpath])


	def generate_conll_tree1(self):
		"""
			Assuming the order of sentences in ptree_list and conll_list are the same
		"""
		if not len(self.tree_list) == len(self.conll_list):
			print "Incompatible parsing tree and conll data !!!"
			return

		for i in range(len(self.conll_list)):
			sent_conll = self.conll_list[i]
			sent_paths = self.get_root_path(self.tree_list[i])
			sent_spines = []

			for w in range(len(sent_conll)):
				# index not includes root
				spine = self.get_spine(sent_conll[w][2]-1, w, sent_paths)
				print spine
				sent_spines.append(spine)

			#for a in sent_paths:
			#	print(a)
			print 
			self.tree_list[i].draw()

	def get_spine1(self, head, modifier, sent_paths):
		if head == -1:
			return sent_paths[modifier]
		
		print head, modifier
		head_spine = sent_paths[head]
		modifier_spine = sent_paths[modifier]
		
		print head_spine
		print modifier_spine
		if head_spine.height() <= 2:

			print "Error in get spine!!! Head_spine Height less than 3!!"
			#print head, modifier
			#print head_spine
			return

		while head_spine.node == modifier_spine.node:
			if modifier_spine.height() < 3:
				# the smallest spine is the word plus its POS tag
				return modifier_spine

			head_spine = head_spine[0]
			modifier_spine = modifier_spine[0]

		return modifier_spine

	def load_trees(self, filename):
		tree_list = []

		trees = open(filename)
		ptree = ""

		for tree in trees:
			tree = tree[:-1]
			if tree == '':
				continue

			#print tree

			if tree[0] == '(' and not ptree == "":
				tree_list.append(Tree.parse(ptree))
				ptree = ""

			ptree += tree.strip(' ')

		if not ptree == "":
			tree_list.append(Tree.parse(ptree))
		
		self.tree_list += tree_list

	def load_conll(self, filename):
		data = open(filename)

		sent_list = []
		sent = []
		for line in data:
			line = line[:-1]

			if not line == "":
				line = line.split()
				line[2] = int(line[2])
				sent.append(line)
			else:
				if not sent == []:
					sent_list.append(sent)
					sent = []

		self.conll_list += sent_list

	def get_root_path(self, subtree):
		spine_list = []

		if subtree.height() == 2:
			return [subtree]
		else:
			for child in subtree:
				spine_list += self.get_root_path(child)
			
			spine_list = [Tree(subtree.node, [child])  
				#if type(child) == str or not subtree.node == child.node else child
				for child in spine_list ]

		return spine_list






if __name__ == "__main__":
	ctg = ConllTreeGenerator()
	#ctg.ptree_list[0]
	tree0 = Tree('NP',['hellp'])
	tree1 = Tree('PP',['with'])
	tree3 = Tree('ASP', [tree0, tree1])
	#spine_list = ctg.get_root_path(ctg.tree_list[0])
	#for i in spine_list:
	#	print(i)
	#ctg.tree_list[0].draw()
	#a = ctg.load_conll("../../../penn-wsj-deps/00/wsj_0001.mrg.3.pa.gs.tab")
	#for m in a:
	#	print m

	ctg.generate_conll_tree()