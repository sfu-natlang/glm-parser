from nltk.tree import *
import copy
import os

class ConllTreeGenerator():
    def __init__(self, conll_path, tree_path, dump_path, section_list=[]):
        self.section_list = section_list;
        self.conll_path = conll_path
        self.tree_path = tree_path
        self.dump_path = dump_path

        return

    def generate_conll_trees(self, dump=False):
        for section in self.section_list:
            for tree_filename in os.listdir(self.tree_path + "%02d" % section):
                print tree_filename
                conll_file = self.conll_path + "%02d/" % section + tree_filename + ".3.pa.gs.tab"
                tree_file = self.tree_path + "%02d/" % section + tree_filename
                self.load_trees(tree_file)
                self.load_conll(conll_file)

                dump_filename = ""
                if dump == True:
                    dump_filename = self.dump_path + "%02d/" % section + tree_filename
                self.generate_conll_tree(dump_filename)


    def generate_conll_tree(self, dump_filename=""):
        """
            Assuming the order of sentences in ptree_list and conll_list are the same
        """
        if not len(self.tree_list) == len(self.conll_list):
            print "Incompatible parsing tree and conll data !!!"
            return

        # TODO organize the code and make it more clear
        trans_dict = TreeConllTranslateDict() 
        sent_conll_tree_list = []
        for i in range(len(self.conll_list)):
            print i
            sent_conll = self.conll_list[i]
            sent_tree = self.tree_list[i]
            sent_conll_tree = []

            tree_words = sent_tree.leaves()
            conll_words = [r[0] for r in sent_conll]
            #print tree_words
            #print conll_words
            modifier = -1
            for w in range(len(sent_conll)):
                # index not includes root, assume no punctuation as header
                modifier += 1

                while not tree_words[modifier] == conll_words[w]:
                    if trans_dict.has_key(tree_words[modifier]) and trans_dict[tree_words[modifier]] == conll_words[w]:
                        break
                    modifier += 1

                head = sent_conll[w][2]-1
                while not tree_words[head] == conll_words[sent_conll[w][2]-1] or head == modifier:
                    if trans_dict.has_key(tree_words[head]) and trans_dict[tree_words[head]] == conll_words[sent_conll[w][2]-1]:
                        break
                    head += 1

                #print head, tree_words[head], modifier, tree_words[modifier]
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
                
                spine = self.get_spine(modifier_treeposition[n+1:], subtree[modifier_treeposition[n]])

                # store n as the position of the original head "spine" where modifier attaches to
                # the real possition would be n_modifier - n_head - 1 (start from 0)
                sent_conll_tree.append(sent_conll[w]+[spine, n])

            for word in sent_conll_tree:
                #print word
                head = word[2] - 1 # not include the ROOT
                if head < 0:
                    word.append('_')
                else:
                    word.append(word[5]-sent_conll_tree[head][5]-1)

            if not sent_conll_tree == []:
                sent_conll_tree_list.append(sent_conll_tree)

        if not dump_filename == "":
            self.write_file(dump_filename, sent_conll_tree_list)


            
    def write_file(self, filename, sent_conll_tree_list):
        dir = os.path.dirname(filename)
        try:
            os.stat(dir)
        except:
            os.mkdir(dir)

        fp = open(filename,"w")
        for sent_conll_tree in sent_conll_tree_list:
            i = 1
            for row in sent_conll_tree:
                fp.write("%d    %s    _    %s    %s    _    %d    %s    _    _    %s    %s\n"
                    % (i,row[0],row[1],row[1],row[2],row[3],row[4].pprint(),str(row[6])))
                i += 1
                #row[4] = row[4].pprint()  
                #row = [str(k) for k in row]              
                #fp.write("    ".join(row) + "\n")
            fp.write("\n")
        fp.close()

    def get_spine(self, treeposition, tree):
        # assume one word per pos tag
        if len(treeposition) == 1:
            return tree
        else:
            subpath = self.get_spine(treeposition[1:], tree[treeposition[0]])
            #print subpath
            return Tree(tree.node, [subpath])


    def load_trees(self, filename):
        tree_list = []

        trees = open(filename)
        ptree = ""

        for tree in trees:
            tree = tree[:-1]
            if tree == '':
                continue

            if tree[0] == '(' and not ptree == "":
                tree_list.append(Tree.parse(ptree))
                ptree = ""

            ptree += tree.strip(' ')

        if not ptree == "":
            tree_list.append(Tree.parse(ptree))
        
        self.tree_list = tree_list

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
    #self.load_trees("../../../wsj/00/wsj_0001.mrg")
    #self.load_conll("../../../penn-wsj-deps/00/wsj_0001.mrg.3.pa.gs.tab")
    #ctg.load_conll("../../../penn-wsj-deps/00/wsj_0071.mrg.3.pa.gs.tab")
    #ctg.load_trees("../../../wsj/00/wsj_0071.mrg")
    #ctg.tree_list[29].draw()
    ctg.generate_conll_trees(True)