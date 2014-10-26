from nltk.tree import *
import os
from parsed_tree_loader import *
from dep_tree_loader import *
import settings

class ConllTreeGenerator():
    def __init__(self, conll_path, tree_path, dump_path, section_list=[], is_rm_none_word=True, is_lossy=False, is_short_tag=True):
        self.section_list = section_list;
        self.conll_path = conll_path
        self.tree_path = tree_path
        self.dump_path = dump_path

        self.is_rm_none_word = is_rm_none_word
        self.is_lossy = is_lossy
        self.is_short_tag = is_short_tag

        return

    def generate_conll_trees(self, dump=False):
        ptl = ParsedTreeLoader()
        dtl = DepTreeLoader()
        for section in self.section_list:
            for tree_filename in os.listdir(self.tree_path + "%02d" % section):

                # get file that is to be loaded
                print tree_filename
                conll_file = self.conll_path + "%02d/" % section + tree_filename + ".3.pa.gs.tab"
                tree_file = self.tree_path + "%02d/" % section + tree_filename

                # load the files
                self.tree_list = ptl.load_parsed_tree(tree_file)
                self.conll_list = dtl.load_dep_tree(conll_file)

                # remove structure with none word leaf
                if self.is_rm_none_word:
                    ptl.remove_nonword(self.tree_list)

                # shorthen the tags in a tree to make them consistent to the penn treebank
                if self.is_short_tag:
                    ptl.shorten_tag(self.tree_list)

                self.enumerate_leaves()

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

            self.generate_spine(leaf_node, len(modifier_treeposition), ('_','_'), '_', sent_conll, sent_conll_tree)
            sent_conll_tree.sort(key=lambda tup: tup[0]) 
            sent_conll_tree_list.append(sent_conll_tree)

        if not dump_filename == "":
            self.write_file(dump_filename, sent_conll_tree_list)

    def generate_spine(self, sub_spine, spine_len, adjoin_type, join_position, sent_conll, sent_conll_tree):
        while not sub_spine.height() == spine_len:
            sub_spine, adjoin_type, join_position, spine_len = self.recursive_generate_spine(sub_spine, spine_len, adjoin_type, join_position, sent_conll, sent_conll_tree)
        
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
        
        spine = sub_spine.parent() # height at least 3
        left_sibling = sub_spine.left_sibling()
        right_sibling = sub_spine.right_sibling()

        if not self.is_r_adjoin(spine, sub_spine):   

            # s-adjoin
            j = len(spine) - 1  

            while j >= 0 :

                child_tree = spine[j]

                #except the spine of the current header
                if spine[j] == sub_spine:
                    j = j - 1
                    continue


                if spine[j] == left_sibling or spine[j] == right_sibling:
                    child_adjoin_type = ('s', 0)
                else:
                    child_adjoin_type = ('s', 1)

                spine.remove(spine[j])
                child_sub_spine, child_spine_len = self.get_child_info(child_tree, sub_spine.leaves()[0][0], sent_conll)
                child_join_position = sub_spine.height() - 1 #  + 1 - 2
                #child_adjoin_type = "s"

                self.generate_spine(child_sub_spine, child_spine_len, child_adjoin_type, child_join_position, sent_conll, sent_conll_tree)
                j = j - 1
        
        else:

            # r-adjoin
            j = len(spine) - 1
            while j >= 0:
                child_tree = spine[j]
                if spine[j] == sub_spine:
                    j = j - 1
                    continue

                if spine[j] == left_sibling or spine[j] == right_sibling:
                    child_adjoin_type = ('r', 0)
                else:
                    child_adjoin_type = ('r', 1)

                spine.remove(spine[j])
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
        if not spine.label() == sub_spine.label():
            return False

        # only two same adj node:
        if spine.parent() == None or (not spine.parent().label() == spine.label()):
            print "two same adj nodes -- r adjoin"
            return True

        # Tree adj node without left sub sibling but with left sibling (same as right):
        if self.is_lossy == False:
            if (spine.left_sibling() and not sub_spine.left_sibling()) or (spine.right_sibling() and not sub_spine.right_sibling()):
                print "Tree adj node without left sub sibling but with left sibling (same as right)"
                return False

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
        if node.height() <= 2:
            return node

        treeposition = tree.leaf_treeposition(leaf_index)

        for i in treeposition:
            node = node[i]
            if node.height() <= 2:
                break
        return node

    def write_file(self, filename, sent_conll_tree_list):
	dir = os.path.dirname(filename)
        try:
            os.stat(dir)
        except:
            os.mkdir(dir)

        fp = open(filename.rstrip("\.mrg")+".spine","w")
        for sent_conll_tree in sent_conll_tree_list:

            for row in sent_conll_tree:
                # sent_index, word, tag, sent_conll_row[2], sent_conll_row[3], sub_spine, join_position, adjoin_type
                #     Pierre    _    NNP    NNP    _    2    NMOD    _    _    (NNP Pierre)    1    s    0

                fp.write("%d    %s    _    %s    %s    _    %d    %s    _    _    \"%s\"    %s    %s    %s\n"
                    % (row[0],row[1],row[2],row[2],row[3],row[4],row[5].pprint(),str(row[6]),row[7][0],str(row[7][1])))

            fp.write("\n")
        fp.close()

    def remove_tag_word(self, spine):
        # if nothing went wrong, the spine would contain both word and tag
        treeposition = spine.leaf_treeposition(0)
        word = spine.leaves()[0][1]
        tag = spine[treeposition[:-1]].label()

        if len(treeposition) == 1:
            spine = ParentedTree("",[])
        else:
            sub_spine = spine[treeposition[:-2]]
            sub_spine.pop()
            sub_spine.append(ParentedTree("",[]))
        return word, tag, spine

    def get_spine(self, treeposition, tree):
        # assume one word per pos tag
        if len(treeposition) == 1:
            return tree
        else:
            subpath = self.get_spine(treeposition[1:], tree[treeposition[0]])

            return Tree(tree.label(), [subpath])

    def enumerate_leaves(self):
        for tree in self.tree_list:
            leaves = tree.leaves()
            for i in range(len(leaves)):
                tree[tree.leaf_treeposition(i)] = (i+1, leaves[i])

    



HELP_MSG =\
"""

script for extract spine from penn-wsj-dep

options:
    -h:     help message
    
    -b:     begining section 
    -e:     ending section 
    (   training would not be processed
        unless both begin and ending section is specfied    )
    
    -c:     path to penn-wsj-dep, default: "./penn-wsj-deps/"

    -t:     path to wsj parsed tree, default: "./wsj/"
            
    -d:     path to dump conll_tree format
    -n:     not remove nonword leaf
            (otherwise, the nonword leaf would be removed)
    -l:     lossy extraction
    -s:     not shorten the tags

"""

if __name__ == "__main__":
    import getopt, sys
    
    sec_begin = 0
    sec_end = 24
    conll_path = settings.PENN_PATH  
    tree_path = settings.WSJ_PATH
    d_filename = settings.WSJ_CONLL_PATH + "loseless/"
    is_rm_none_word = True
    is_lossy = False
    is_short_tag = True

    try:
        opt_spec = "hb:e:c:t:d:nl"
        opts, args = getopt.getopt(sys.argv[1:], opt_spec)
        for opt, value in opts:
            if opt == "-h":
                print HELP_MSG
                sys.exit(0)
            elif opt == "-n":
                is_rm_none_word = False
            elif opt == "-l":
                is_lossy = True
            elif opt == "-s":
                is_short_tag = False
            elif opt == "-b":
                sec_begin = int(value)
            elif opt == "-e":
                sec_end = int(value)
            elif opt == "-c":
                conll_path = value
            elif opt == "-t":
                tree_path = value
            elif opt == "-d":
                d_filename = value
            else:
                print "invalid input, see -h"
                sys.exit(0)

        if sec_begin >= 0 and sec_end >= 0:
            extract_sec = range(sec_begin, sec_end+1)
            ctg = ConllTreeGenerator(conll_path, tree_path, d_filename, extract_sec, is_rm_none_word, is_lossy)
            ctg.generate_conll_trees(True)

    except getopt.GetoptError, e:
        print "invalid arguments!! \n" + HELP_MSG
        sys.exit(1)
