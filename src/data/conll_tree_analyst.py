from conll_tree_loader import *
from parsed_tree_loader import *

class ConllTreeAnalyst():
    def __init__(self, conll_tree_path, parsed_tree_path, start_section, end_section):
        self.conll_tree_path = conll_tree_path
        self.parsed_tree_path = parsed_tree_path
        self.start_section = start_section
        self.end_section = end_section

        # attributes for statistics
        self.init_stats_attrs()

        ctl = ConllTreeLoader()
        self.conll_tree_sent_list = ctl.load_conll_trees(conll_tree_path, start_section, end_section)

        ptl = ParsedTreeLoader()
        self.parsed_tree_list = ptl.load_parsed_trees(parsed_tree_path, start_section, end_section)
        return

    def init_stats_attrs(self):
        self.etree_count_dict = {}
        self.height_count_dict = {}
        self.r1_count = 0
        self.r0_count = 0
        self.s1_count = 0
        self.s0_count = 0
        self.tag_set = []
        self.pos_set = []

    def set_etree_count_dict(self):
        self.etree_count_dict = {}
        for sent in self.conll_tree_sent_list:
            for node in sent.word_list:
                if not node.spine.pprint() in self.etree_count_dict:
                    self.etree_count_dict[node.spine.pprint()] = 1
                else:
                    self.etree_count_dict[node.spine.pprint()] += 1

        #print self.etree_count_dict

    def set_height_count_dict(self):
        self.height_count_dict = {}
        for sent in self.conll_tree_sent_list:
            for node in sent.word_list:
                if not node.spine.height() in self.height_count_dict:
                    self.height_count_dict[node.spine.height()] = 1
                else:
                    self.height_count_dict[node.spine.height()] += 1
        #print self.height_count_dict

    def get_tree_in_height(self, height):
        spine_list = []
        sent_list = []
        for i in range(len(self.conll_tree_sent_list)):
            sent = self.conll_tree_sent_list[i]
            for node in sent.word_list:
                if node.spine.height() == height:
                    spine_list.append((node.spine, node.word))
                    sent.set_parsed_tree(self.parsed_tree_list[i])
                    sent_list.append(sent)
        return spine_list, sent_list

    def count_adjoin_type(self):
        self.r1_count = 0
        self.r0_count = 0
        self.s1_count = 0
        self.s0_count = 0
        for sent in self.conll_tree_sent_list:
            for node in sent.word_list:
                if node.adjoin_type == "s" and node.is_adj == 0:
                    self.s0_count += 1
                elif node.adjoin_type == "s" and node.is_adj == 1:
                    self.s1_count += 1
                elif node.adjoin_type == "r" and node.is_adj == 0:
                    self.r0_count += 1
                elif node.adjoin_type == "r" and node.is_adj == 1:
                    self.r1_count += 1

    def set_tag_set(self):
        self.tag_set = []
        for sent in self.conll_tree_sent_list:
            for node in sent.word_list:
                if not node.tag in self.tag_set:
                    self.tag_set.append(node.tag)

    def set_pos_set(self):
        self.pos_set = []
        for sent in self.conll_tree_sent_list:
            for node in sent.word_list:
                self._set_pos_set(node.spine)

    def _set_pos_set(self, spine):
        if not spine.node in self.pos_set:
            self.pos_set.append(spine.node)
        for child in spine:
            self._set_pos_set(child)

    def generate_report(self, output_file):
        dir = os.path.dirname(output_file)
        try:
            os.stat(dir)
        except:
            os.mkdir(dir)

        fp = open(output_file,"w")
        
        fp.write("Report for Conll Tree Data\n\n")
        fp.write("Section %d to %d\n" % (self.start_section, self.end_section))
        fp.write("Conll Tree Path: %s\n" % self.conll_tree_path)
        fp.write("Parsed Tree Path: %s\n\n" % self.parsed_tree_path)
        fp.write("Number of Sentences: %d \n\n\n" % len(self.conll_tree_sent_list))
        fp.write("Spine Statistics:\n")

        self.set_etree_count_dict()
        fp.write("Number of Distinct Elementry Trees (Spines): %d\n\n" % len(self.etree_count_dict))

        self.set_height_count_dict()
        fp.write("Height    | Count \n")
        for key in self.height_count_dict:
            fp.write("   %d    | %d \n" % (key, self.height_count_dict[key]))
        fp.write("\n\n")

        max_height = max([key for key in self.height_count_dict])
        fp.write("Sentences and Trees containing spines of height %d\n\n" % max_height)

        spine_list, sent_list = self.get_tree_in_height(max_height)
        for i in range(len(spine_list)):
            spine = spine_list[i][0]
            word = spine_list[i][1]
            sent = sent_list[i]
            fp.write("Spine: %s\n" % spine.pprint())
            fp.write("Word: %s\n" % word)
            fp.write("From File: %s \n" % sent.filename)
            fp.write("In Sentence: %s \n" % sent.get_sent_words())
            fp.write("Parsed Tree:\n %s\n\n\n" % sent.parsed_tree.pprint())

        self.count_adjoin_type()
        fp.write("Number of s0: %d\n" % self.s0_count)
        fp.write("Number of s1: %d\n" % self.s1_count)
        fp.write("Number of r0: %d\n" % self.r0_count)
        fp.write("Number of r1: %d\n\n" % self.r1_count)

        self.set_tag_set()
        fp.write("Number of tags: %d\n" % len(self.tag_set))
        fp.write("Tags used: %s\n\n" % "   ".join(sorted(self.tag_set)))
        
        self.set_pos_set()
        fp.write("Number of pos: %d\n" % len(self.pos_set))
        fp.write("POS used: %s\n" % ", ".join(sorted(self.pos_set)))
        fp.close()

if __name__ == "__main__":
    cta = ConllTreeAnalyst("../../../wsj_conll_tree/", "../../../wsj/", 0, 24)
    cta.generate_report("./lossless_spine_report.txt")
    """ 
    print "number of sentences -- conll tree", len(cta.conll_tree_sent_list)
    print "number of sentences -- parsed tree", len(cta.parsed_tree_list)

    cta.count_adjoin_type()
    print "number of s0:", cta.s0_count
    print "number of s1:", cta.s1_count
    print "number of r0:", cta.r0_count
    print "number of r1:", cta.r1_count
    total_adjoin = cta.s0_count + cta.s1_count + cta.r0_count + cta.r1_count
    print "sum:", total_adjoin
    print "number of spine", total_adjoin + len(cta.parsed_tree_list)

    z = 0
    for sent in cta.conll_tree_sent_list:
        z += len(sent.word_list)
    print "number of spine", z

    cta.set_etree_count_dict()
    print "number of distinct spine", len(cta.etree_count_dict)

    a = 0
    for key in cta.etree_count_dict:
        a += cta.etree_count_dict[key]
    print "number of spine", a

    cta.set_height_count_dict()
    print "number of distinct height", len(cta.height_count_dict)
    b = 0
    for key in cta.height_count_dict:
        b += cta.height_count_dict[key]
    print "number of spine", b
    
    spine_list, sent_list = cta.get_tree_in_height(5)
    for i in range(len(spine_list)):
        print spine_list[i]
        print sent_list[i].get_sent_words()
        print sent_list[i].filename
        sent_list[i].parsed_tree.draw()
    
    cta.set_tag_set()
    print "number of tags", len(cta.tag_set)
    print sorted(cta.tag_set)

    cta.set_pos_set()
    print "number of pos", len(cta.pos_set)
    print sorted(cta.pos_set)
    """
