from nltk.tree import *
import os

class ConllTreeLoader():
    def __init__(self):
        return

    def load_conll_trees(self, conll_tree_path, start_section, end_section):
        conll_tree_sent_list = []
        for section in range(start_section, end_section+1):
            for conll_tree_filename in sorted(os.listdir(conll_tree_path + "%02d" % section)):
                print conll_tree_filename
                conll_tree_file = conll_tree_path + "%02d/" % section + conll_tree_filename
                conll_tree_sent_list = conll_tree_sent_list + self.load_conll_tree(conll_tree_file)
        return conll_tree_sent_list

    def load_conll_tree(self, filename):
        conll_tree_sent_list = []
        conll_trees = open(filename)
        word_list = []
        for line in conll_trees:
            line = line[:-1]
            if line == "":
                if not word_list == []:
                    conll_tree_sent_list.append(ConllTreeSent(word_list, filename))
                    word_list = []
                continue

            line = line.split("    ")
            # print line
            # sent_index, word, tag, sent_conll_row[2], sent_conll_row[3], sub_spine, join_position, adjoin_type
            ctw = ConllTreeWord()
            ctw.sent_index = int(line[0])
            ctw.word = line[1]
            ctw.tag = line[3]
            ctw.head_index = line[6]
            ctw.dep_type = line[7]
            ctw.set_spine(line[10])
            ctw.set_join_position(line[11])
            ctw.set_adjoin_type(line[12])
            ctw.set_is_adj(line[13])
            word_list.append(ctw)

        if not word_list == []:
            conll_tree_sent_list.append(ConllTreeSent(word_list, filename))

        #print "load conll tree finished ..."
        return conll_tree_sent_list

class ConllTreeSent():
    def __init__(self, word_list, filename=None):
        import ntpath
        self.word_list = word_list
        self.filename = ntpath.basename(filename)
        self.parsed_tree = None

    def get_sent_words(self):
        sent_words = [node.word for node in self.word_list]
        sent_words = " ".join(sent_words)
        return sent_words

    def set_parsed_tree(self, tree):
        self.parsed_tree = tree

class ConllTreeWord():
    def __init__(self):
        self.sent_index = None
        self.word = None
        self.tag = None
        self.head_index = None
        self.dep_type = None
        self.spine = None
        self.join_position = None
        self.adjoin_type = None
        self.is_adj = None

    def set_spine(self, spine_str):
        #print spine_str
        self.spine = ParentedTree.parse(spine_str[1:-1])

    def set_join_position(self, position):
        if position == "_":
            return
        self.join_position = int(position)

    def set_adjoin_type(self, adjoin_type):
        if adjoin_type == "_":
            return
        self.adjoin_type = adjoin_type

    def set_is_adj(self, is_adj):
        if is_adj == "_":
            return
        self.is_adj = int(is_adj)
