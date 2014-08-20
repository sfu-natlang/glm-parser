from nltk.tree import *
import os

class ParsedTreeLoader():
    def __init__(self):
        return

    def load_parsed_trees(self, parsed_tree_path, start_section, end_section, is_rm_none_word=True, is_short_tag=True):
        parsed_tree_list = []
        for section in range(start_section, end_section+1):
            for tree_filename in sorted(os.listdir(parsed_tree_path + "%02d" % section)):
                print tree_filename
                tree_file = parsed_tree_path + "%02d/" % section + tree_filename
                parsed_tree_list = parsed_tree_list + self.load_parsed_tree(tree_file)

        # remove structure with none word leaf
        if is_rm_none_word:
            self.remove_nonword(parsed_tree_list)

        # shorthen the tags in a tree to make them consistent to the penn treebank
        if is_short_tag:
            self.shorten_tag(parsed_tree_list)

        return parsed_tree_list

    def load_parsed_tree(self, filename):
        tree_list = []

        trees = open(filename)
        ptree = ""

        for tree in trees:
            tree = tree[:-1]
            if tree == '':
                continue

            if tree[0] == '(' and not ptree == "":
                tree_list.append(ParentedTree.parse(ptree))
                ptree = ""

            ptree += tree.strip(' ')

        if not ptree == "":
            tree_list.append(ParentedTree.parse(ptree))
        
        #print "load parsed tree finished"
        return tree_list

    def remove_nonword(self, tree_list):
        for tree in tree_list:
            _, tree = self.remove_nonword_leaf(tree)
            #print tree.pprint()
        print "remove nonword finished.."

    def remove_nonword_leaf(self, tree):

        trans_dict = TreeConllTranslateDict() 
        if tree.height() == 2:
            # make the word of the spine the same as the penn-wsj-dep
            if trans_dict.has_key(tree[0]):
                tree[0] = trans_dict[tree[0]]

            # detect none word
            if tree.node == '-NONE-':
                return False, tree
            else:
                return True, tree
        else:
            i = 0
            k = len(tree)
            while i < k:
                r, tree[i] = self.remove_nonword_leaf(tree[i])
                if not r:
                    tree.pop(i)
                    k = k - 1
                    i = i - 1                
                i = i + 1

            if len(tree) == 1 and tree.node == tree[0].node:
                print "collaspe the tree"
                #tree.parent.remove(tree)
                tree._delparent(tree[0], 0)  
                tree = tree[0] 

            if tree.height() == 1:
                return False, tree
            else:
                return True, tree

    def shorten_tag(self, tree_list):
        for tree in tree_list:
            self._shorten_tag(tree)

        print "shorten tag finished"

    def _shorten_tag(self, tree):
        if type(tree) == str:
            return
        else:
            tag = tree.node.split("-")
            tree.node = tag[0]

            tag = tree.node.split("=")
            tree.node = tag[0]

            if len(tree.node) > 1 and tree.node[-1] == '$':
                tree.node = tree.node[:-1]
            for sub_tree in tree:
                self._shorten_tag(sub_tree)

class TreeConllTranslateDict():
    """translation dict from tree word to conll word"""
    def __init__(self):
        self.trans_dict = {}
        self.trans_dict["-LCB-"] = "{"
        self.trans_dict["-RCB-"] = "}"
        self.trans_dict["-LRB-"] = "("
        self.trans_dict["-RRB-"] = ")"

    def __getitem__(self,index):
        return self.trans_dict[index]

    def has_key(self,index):
        return self.trans_dict.has_key(index)
