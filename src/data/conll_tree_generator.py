from nltk.tree import Tree

class ConllTreeGenerator():
	def __init__(self):
		self.load_trees("../../wsj/00/wsj_0001.mrg")
		return

	def load_trees(self, filename):
		ptree_list = []

		trees = open(filename)
		ptree = ""

		for tree in trees:
			tree = tree[:-1]
			if tree == '':
				continue

			#print tree

			if tree[0] == '(' and not ptree == "":
				ptree_list.append(Tree.parse(ptree))
				ptree = ""

			ptree += tree.strip(' ')

		if not ptree == "":
			ptree_list.append(Tree.parse(ptree))
		
		self.ptree_list = ptree_list

	def get_spines(self, tree):
		#if tree.height() <= 2:
		#	return [tree]

		return self.get_root_path(tree)

	def get_root_path(self, subtree):
		spine_list = []

		if subtree.height() == 2:
			return [subtree]
		else:
			for child in subtree:
				spine_list += self.get_root_path(child)
			
			spine_list = [Tree(subtree.node, [children]) for children in spine_list]

		return spine_list


if __name__ == "__main__":
	ctg = ConllTreeGenerator()
	#ctg.ptree_list[0]
	tree0 = Tree('NP',['hellp'])
	tree1 = Tree('PP',['with'])
	tree3 = Tree('ASP', [tree0, tree1])
	spine_list = ctg.get_spines(ctg.ptree_list[0])
	for i in spine_list:
		print(i)
	#ctg.ptree_list[0].draw()
