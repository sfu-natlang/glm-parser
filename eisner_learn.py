
class EisnerLearner():
    """
    A class that implements the learning alrogithm of dependency graphs.
    """
    def __init__():
        return

    def parse_file_string(s):
        """
        Parses the string read from the training file.

        :param s: String read from treebank
        :type s: str

        :return: A list of words and a list of edges, i.e. G = (V,E)
        :rtype: tuple(list,list), the first is the word list and the second is
        the edge list
        """
        # Each line represents one word and its relations
        line_list = s.splitlines()
        # list(tuple(word,POS))
        word_list = [('ROOT','ROOT')]
        # list(tuple(parene_node_index,child_node_index,edge_type))
        edge_list = []
        curret_index = 1
        for line in line_list:
            # A list of 4 elements
            # WORD  POS     PARENT INDEX    EDGE TYPE
            line_tuple = line.split()
            word_list.append((line_tuple[0],line_tuple[1]))
            edge_list.append((line_tupke[2],current_index,line_tuple[3]))
            
            # Do not forget this!!!!!!!!!!!!!!!!!!!!!!
            current_index += 1
        return (word_list,edge_list)


