from nltk.tree import *
import os

class ConllTreeGenerator():
    def __init__(self, conll_path, tree_path, dump_path, section_list=[]):
        self.section_list = section_list;
        self.conll_path = conll_path
        self.tree_path = tree_path
        self.dump_path = dump_path

        self.is_rm_none_word = True
        return

    def generate_conll_trees(self, dump=False):
        for section in self.section_list:
            for tree_filename in os.listdir(self.tree_path + "%02d" % section):

                # get file that is to be loaded
                print tree_filename
                conll_file = self.conll_path + "%02d/" % section + tree_filename + ".3.pa.gs.tab"
                tree_file = self.tree_path + "%02d/" % section + tree_filename

                # load the files
                self.load_trees(tree_file)
                self.load_conll(conll_file)
                # remove structure with none word leaf
                if self.is_rm_none_word:
                    self.remove_nonword()

                #print "print tree list"
                #print self.tree_list
                #for tree in self.tree_list:
                #    print tree.pprint()
                #print "finished ... "

                self.enumerate_leaves()

                #print "print tree list"
                #print self.tree_list
                #for tree in self.tree_list:
                #    print tree.pprint()
                #print "after enumerate finished ... "

                dump_filename = ""
                if dump == True:
                    dump_filename = self.dump_path + "%02d/" % section + tree_filename

                 #47 done
                self.generate_conll_tree(dump_filename)

    def generate_conll_tree(self, dump_filename=""):
        """
            Assuming the order of sentences in ptree_list and conll_list are the same
        """
        if not len(self.tree_list) == len(self.conll_list):
            print "Incompatible parsing tree and conll data !!!"
            return

        sent_conll_tree_list = []
        for i in range(len(self.conll_list)):

            # Every sentence 
            sent_conll = self.conll_list[i]
            #print self.tree_list[i].pprint()
            sent_tree = self.tree_list[i].copy(True)
            sent_conll_tree = []

            tree_words = sent_tree.leaves()
            conll_words = [r[0] for r in sent_conll]
            
            for i in range(len(sent_conll)):
                if sent_conll[i][2] == 0:
                    break

            modifier = i

            modifier_treeposition = sent_tree.leaf_treeposition(modifier)

            if len(modifier_treeposition) < 1:
                print "Invalid tree";
                return

            leaf_node = self.find_leaf_node(modifier, sent_tree)

            self.generate_spine(leaf_node, len(modifier_treeposition), '_', '_', sent_conll, sent_conll_tree)
            sent_conll_tree.sort(key=lambda tup: tup[0]) 
            sent_conll_tree_list.append(sent_conll_tree)

        #print sent_conll_tree_list
        if not dump_filename == "":
            self.write_file(dump_filename, sent_conll_tree_list)

    def generate_spine(self, sub_spine, spine_len, adjoin_type, join_position, sent_conll, sent_conll_tree):
        while not sub_spine.height() == spine_len:
            sub_spine, adjoin_type, join_position, spine_len = self.recursive_generate_spine(sub_spine, spine_len, adjoin_type, join_position, sent_conll, sent_conll_tree)
        
        #sub_spine.draw()
        #print sub_spine.pprint()
        sent_index = sub_spine.leaves()[0][0]     # start from 1 considering ROOT
        sent_conll_row = sent_conll[sent_index-1] # sent_index start from 0 in the sent_conll

        word, tag, sub_spine = self.remove_tag_word(sub_spine)
        sent_conll_tree.append((sent_index, word, tag, sent_conll_row[2], sent_conll_row[3], sub_spine, join_position, adjoin_type))

    def recursive_generate_spine(self, sub_spine, spine_len, adjoin_type, join_position, sent_conll, sent_conll_tree):
        """
            adjoin_type --- flag indicates if the node has r-adjoin before it in the same level,
                        -1 if it is s-adjoin, 0 if it is the 1st r-adjoin, 1 if it is r-adjoin but not the 1st one)
            join_position --- the height in the head spine that the modifier adjoins (before any r-adjoin)
            sent_conll_tree --- store the results
        """

        if sub_spine.height() < 2:
            print "error the spine is too short"
            return
        
        #print sub_spine.pprint()
        spine = sub_spine.parent() # height at least 3
        #print spine.pprint()
        if not self.is_r_adjoin(spine, sub_spine):   

            # s-adjoin
            j = len(spine) - 1  

            while j >= 0 :

                child_tree = spine[j]

                #except the spine of the current header
                if spine[j] == sub_spine:
                    j = j - 1
                    continue
                #print spine.pprint()
                spine.remove(spine[j])
                #print spine.pprint()
                child_sub_spine, child_spine_len = self.get_child_info(child_tree, sub_spine.leaves()[0][0], sent_conll)
                child_join_position = sub_spine.height() - 1 #  + 1 - 2
                child_adjoin_type = "s"

                self.generate_spine(child_sub_spine, child_spine_len, child_adjoin_type, child_join_position, sent_conll, sent_conll_tree)
                j = j - 1
        
        else:

            # r-adjoin
            j = len(spine) - 1
            left_sibling = sub_spine.left_sibling()
            right_sibling = sub_spine.right_sibling()

            while j >= 0:
                child_tree = spine[j]
                if spine[j] == sub_spine:
                    j = j - 1
                    continue

                if spine[j] == left_sibling or spine[j] == right_sibling:
                    child_adjoin_type = "r-0"
                else:
                    child_adjoin_type = "r-1"
                spine.remove(spine[j])
                #print child_adjoin_type
                child_sub_spine, child_spine_len = self.get_child_info(child_tree, sub_spine.leaves()[0][0], sent_conll)
                child_join_position = sub_spine.height() - 2 # the height that the child join to, first node as height 1

                self.generate_spine(child_sub_spine, child_spine_len, child_adjoin_type, child_join_position, sent_conll, sent_conll_tree)
                j = j - 1
                
            # remove the node added by r adjoinction
            spine = self.change_tree(spine, sub_spine)
            spine_len = spine_len - 1


        return spine, adjoin_type, join_position, spine_len

    def is_r_adjoin(self, spine, sub_spine):
        # no adj node:
        if not spine.node == sub_spine.node:
            return False

        # only two same adj node:
        if spine.parent() == None or (not spine.parent().node == spine.node):
            print "two same adj nodes -- r adjoin"
            return True

        # Tree adj node without left sub sibling but with left sibling (same as right):
        if (spine.left_sibling() and not sub_spine.left_sibling()) or (spine.right_sibling() and not sub_spine.right_sibling()):
            print "Tree adj node without left sub sibling but with left sibling (same as right)"
            return False

        else:
            print "r-adjoin"
            return True

    def change_tree(self, tree_to_remove, tree_to_add):
        parent_tree = tree_to_remove.parent()
        p_index = tree_to_remove.parent_index()
                
        tree_to_add.parent()._delparent(tree_to_add, tree_to_add.parent_index()) 
                
        if not parent_tree == None:     
            parent_tree.pop(p_index)
            parent_tree.insert(p_index, tree_to_add)

        return tree_to_add

    def get_child_info(self, child_tree, head_sent_index, sent_conll):
        for i in range(child_tree.leaves()[0][0]-1, child_tree.leaves()[-1][0]):             
            if sent_conll[i][2] == head_sent_index:
                break

        child_head_subtree_index = i - child_tree.leaves()[0][0] + 1                
        child_spine_len = len(child_tree.leaf_treeposition(child_head_subtree_index))+1
        child_sub_spine = self.find_leaf_node(child_head_subtree_index, child_tree)
        return child_sub_spine, child_spine_len

    def find_leaf_node(self, leaf_index, tree):
        """
            leaf_index is the index in the tree passed into the function
        """
        node = tree
        #print tree.pprint()
        if node.height() <= 2:
            return node

        treeposition = tree.leaf_treeposition(leaf_index)

        #print treeposition
        for i in treeposition:
            node = node[i]
            #print node
            if node.height() <= 2:
                break
        #print node.pprint()
        return node

    def write_file(self, filename, sent_conll_tree_list):
        dir = os.path.dirname(filename)
        try:
            os.stat(dir)
        except:
            os.mkdir(dir)

        fp = open(filename,"w")
        for sent_conll_tree in sent_conll_tree_list:

            for row in sent_conll_tree:
                # sent_index, word, tag, sent_conll_row[2], sent_conll_row[3], sub_spine, join_position, adjoin_type
                #     Pierre    _    NNP    NNP    _    2    NMOD    _    _    (NNP Pierre)    1

                #print spine
                fp.write("%d    %s    _    %s    %s    _    %d    %s    _    _    \"%s\"    %s    %s\n"
                    % (row[0],row[1],row[2],row[2],row[3],row[4],row[5].pprint(),str(row[6]),row[7]))

                #row[4] = row[4].pprint()  
                #row = [str(k) for k in row]              
                #fp.write("    ".join(row) + "\n")
            fp.write("\n")
        fp.close()

    def remove_tag_word(self, spine):
        # if nothing went wrong, the spine would contain both word and tag
        treeposition = spine.leaf_treeposition(0)
        word = spine.leaves()[0][1]
        tag = spine[treeposition[:-1]].node
        #print treeposition
        if len(treeposition) == 1:
            spine = ParentedTree("",[])
        else:
            sub_spine = spine[treeposition[:-2]]
            sub_spine.pop()
        return word, tag, spine

    def get_spine(self, treeposition, tree):
        # assume one word per pos tag
        if len(treeposition) == 1:
            return tree
        else:
            subpath = self.get_spine(treeposition[1:], tree[treeposition[0]])
            #print subpath
            return Tree(tree.node, [subpath])

    def enumerate_leaves(self):
        for tree in self.tree_list:
            leaves = tree.leaves()
            for i in range(len(leaves)):
                tree[tree.leaf_treeposition(i)] = (i+1, leaves[i])

    def load_trees(self, filename):
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
        
        self.tree_list = tree_list
        print "load tree finished"

    def remove_nonword(self):
        for tree in self.tree_list:
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

        self.conll_list = sent_list


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

if __name__ == "__main__":
    ctg = ConllTreeGenerator("../../../penn-wsj-deps/", "../../../wsj/", "../../../wsj_conll_tree/", [0])
    #ctg.ptree_list[0]
    tree0 = Tree('NP',['hellp'])
    tree1 = Tree('PP',['with'])
    tree3 = Tree('ASP', [tree0, tree1])
    #spine_list = ctg.get_root_path(ctg.tree_list[0])
    #for i in spine_list:
    #    print(i)
    #ctg.tree_list[0].draw()
    #a = ctg.load_conll("../../../penn-wsj-deps/00/wsj_0001.mrg.3.pa.gs.tab")
    #for m in a:
    #    print m
    #ctg.load_trees("../../../wsj/55/wsj_0110.mrg")
    #ctg.remove_nonword()
    #ctg.tree_list[0].draw()
    #self.load_conll("../../../penn-wsj-deps/00/wsj_0001.mrg.3.pa.gs.tab")
    #ctg.load_conll("../../../penn-wsj-deps/00/wsj_0071.mrg.3.pa.gs.tab")
    #ctg.load_trees("../../../wsj/00/wsj_0071.mrg")
    #ctg.tree_list[0].draw()
    ctg.generate_conll_trees(True)
    