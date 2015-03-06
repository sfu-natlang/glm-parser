
#
# Global Linear Model Parser
# Simon Fraser University
# NLP Lab
#
# Author: Yulan Huang, Ziqi Wang, Anoop Sarkar
# (Please add on your name if you have authored this file)
#

# Dict-like object that stores features
import feature_vector
import english_1st_fgen
import debug.debug


class SecondOrderFeatureGenerator():
    """
    Second order feature generator: Sibling features and grandchild features
    """
    def __init__(self, sent):
        # Construct a first order feature generator, and pre-cache some necessary data
        # We just wrap around first order
        self.first_order_generator = english_1st_fgen.FirstOrderFeatureGenerator(sent)

        # Make shortcuts - Not necessary, but saves some key strokes
        self.word_list = self.first_order_generator.word_list
        self.pos_list = self.first_order_generator.pos_list
        self.key_gen_func = self.first_order_generator.key_gen_func
        self.five_gram_word_list = self.first_order_generator.five_gram_word_list

        return

    def get_2nd_sibling_feature(self, fv, head_index, dep_index, sib_index):
        """
        Add second order sibling feature to feature vector

          |------->>>-----|
        head-->sibling   dep *or*
          |-------<<<-----|
        dep   sibling<--head

        head = xi, dep = xj, sibling = xk

        +------------------------+
        | xi_pos, xk_pos, xj_pos | type = 1
        | xk_pos, xj_pos         | type = 2
        | xk_word, xj_word       | type = 3
        | xk_word, xj_pos        | type = 4
        | xk_pos, xj_word        | type = 5
        +------------------------+

        (4, type, [remaining components in the above order])

        :param fv: Feature vector instance. This object will be changed in-place
        :param head_index: The index of the head node (parent node)
        :param dep_index: The index of the dependency node (outer side node)
        :param sib_index: The index of the sibling node (inner side node)
        :return: None
        """
        # Extract POS and word
        xi_pos = self.pos_list[head_index]
        xj_pos = self.pos_list[dep_index]
        xk_pos = self.pos_list[sib_index]
        xk_word = self.word_list[sib_index]
        xj_word = self.word_list[dep_index]

        key_gen_func = self.key_gen_func

        type1_str = key_gen_func((4, 1, xi_pos, xk_pos, xj_pos))
        type2_str = key_gen_func((4, 2, xk_pos, xj_pos))
        type3_str = key_gen_func((4, 3, xk_word, xj_word))
        type4_str = key_gen_func((4, 4, xk_word, xj_pos))
        type5_str = key_gen_func((4, 5, xk_pos, xj_word))

        fv[type1_str] = 1
        fv[type2_str] = 1
        fv[type3_str] = 1
        fv[type4_str] = 1
        fv[type5_str] = 1

        return

    def get_2nd_grandparent_feature(self, fv, head_index, dep_index, gc_index):
        """
        Add grandchild feature into the feature vector

        head-->dep-->grandchild *or*
        grandchild<--dep<--head *or*
             |------<<<-----|
        grandchild  head-->dep  *or*
         |------>>>------|
        dep<--head  grandchild

        head = xi, dep = xj, gc = xk

        +------------------------+
        | xi_pos, xk_pos, xj_pos | type = 1
        | xk_pos, xj_pos         | type = 2
        | xk_word, xj_word       | type = 3
        | xk_word, xj_pos        | type = 4
        | xk_pos, xj_word        | type = 5
        +------------------------+

        (5, type, [remaining components in the above order])

        :param fv: Feature vector
        :param head_index: Index of the header
        :param dep_index: Index of the dependent node
        :param gc_index: Index of the grand child node
        :return: None
        """
        xi_pos = self.pos_list[head_index]
        xj_pos = self.pos_list[dep_index]
        xk_pos = self.pos_list[gc_index]
        xk_word = self.word_list[gc_index]
        xj_word = self.word_list[dep_index]

        key_gen_func = self.key_gen_func

        type1_str = key_gen_func((5, 1, xi_pos, xk_pos, xj_pos))
        type2_str = key_gen_func((5, 2, xk_pos, xj_pos))
        type3_str = key_gen_func((5, 3, xk_word, xj_word))
        type4_str = key_gen_func((5, 4, xk_word, xj_pos))
        type5_str = key_gen_func((5, 5, xk_pos, xj_word))

        fv[type1_str] = 1
        fv[type2_str] = 1
        fv[type3_str] = 1
        fv[type4_str] = 1
        fv[type5_str] = 1

        return

    # Here defines some feature type. Used in method get_local_vector
    FIRST_ORDER = 0
    SECOND_ORDER_SIBLING = 1
    SECOND_ORDER_GRANDCHILD = 2
    SECOND_ORDER_SIBLING_ONLY = 3
    SECOND_ORDER_GRANDCHILD_ONLY = 4

    def get_local_vector(self, head_index, dep_index,
                         other_index_list=None,
                         feature_type=0):
        """
        Given an edge, return its local vector

        To support higher order feature, use other_index_list. The content of
        other_index_list is determined by argument feature_type, which specifies
        how the content of other_index_list will be interpreted. See below.

        1st-order features are added no matter which higher-order feature we
        are using. Higher-order features are specified by argument
        feature_type. The values are defined below:

        ----------------------------------------------------------------------------
        | feature_type       Description                   other_index_list        |
        |--------------------------------------------------------------------------|
        |      0        Normal 1st order features       None or [] (Won't be used) |
        |                                                                          |
        |      1        2nd order sibling type with    [0]: Sibling index or None* |
        |               1st order feature                                          |
        |                                                                          |
        |      2       2nd order grand child type        [0]: grand child index    |
        |               with 1st order feature                                     |
        |                                                                          |
        |      3        2nd order sibling type**                  See (1)          |
        |                                                                          |
        |      4      2nd order grand child type**                See (2)          |
        |--------------------------------------------------------------------------|
        | * If [0] == None, then type 1 degrades to type 0                         |
        | ** By default, type 3 and 4 does not include lower order features. This  |
        | two options are useful for some applications of feature vector           |
        ----------------------------------------------------------------------------

        (More on the way...)

        :param head_index: The index of the head node
        :type head_index: integer
        :param dep_index: The index of the dependency node
        :type dep_node: integer
        :param other_index_list: The index of
        """
        # Deal with the case when feature type == 1 (sibling)
        # but the sibling is None. In this case the situation
        # degrades to a normal dependency relation
        if feature_type == self.SECOND_ORDER_SIBLING and \
             other_index_list[0] is None:
            feature_type = self.FIRST_ORDER

        # For these two types there is not need to compute first order
        if feature_type == self.SECOND_ORDER_GRANDCHILD_ONLY or \
            feature_type == self.SECOND_ORDER_SIBLING_ONLY:
                # Empty one. In this case local_fv_1st should not be used
                local_fv_1st = None
        else:
            # Decorated with dist and dir; do not do this again
            local_fv_1st = self.first_order_generator.get_local_vector(head_index, dep_index)

        # Fast path: return directly if only 1st order are evaluated
        if feature_type == self.FIRST_ORDER:
            return local_fv_1st

        # Initialize an empty local vector to hold all 2nd order features (sibling or grandchild)
        local_fv_second_order = feature_vector.FeatureVector()

        if (feature_type == self.SECOND_ORDER_SIBLING or
             feature_type == self.SECOND_ORDER_SIBLING_ONLY):
            sibling_index = other_index_list[0]
            self.get_2nd_sibling_feature(local_fv_second_order,
                                         head_index, dep_index,
                                         sibling_index)
            # From sibling to dependent node (we assume the sibling
            # node is between the head and dependent node)
            self.first_order_generator.add_dir_and_dist(local_fv_second_order,
                                                        sibling_index,
                                                        dep_index)

            if feature_type == self.SECOND_ORDER_SIBLING_ONLY:
                return local_fv_second_order
        elif (feature_type == self.SECOND_ORDER_GRANDCHILD or
              feature_type == self.SECOND_ORDER_GRANDCHILD_ONLY):
            grandchild_index = other_index_list[0]
            self.get_2nd_grandparent_feature(local_fv_second_order,
                                             head_index, dep_index,
                                             grandchild_index)
            # From dependent node to grand child
            self.first_order_generator.add_dir_and_dist(local_fv_second_order,
                                                        dep_index,
                                                        grandchild_index)

            if feature_type == self.SECOND_ORDER_GRANDCHILD_ONLY:
                return local_fv_second_order
        else:
            raise TypeError("Feature type %d not supported yet" %
                            (feature_type, ))

        # Just rename
        local_fv = local_fv_1st
        ##############################################
        # Merge basic 1st order features and higher order features
        # If memory error is reported here (possibly when the set of
        # higher order features are large), then just add one line:
        #    local_fv_higher_order.pop(i)
        for i in local_fv_second_order.keys():
            local_fv[i] = 1
        # We could use this single line instead:
        #   local_fv.aggregate(local_fv_second_order)
        # And actually it is faster than merging manually
        # But it would not run on local machine without hvector installation
        ##############################################


        return local_fv

    def find_sibling_relation(self, edge_list):
        """
        Find all sibling relations:
          |------->>>-----|
        head-->sibling   dep *or*
          |-------<<<-----|
        dep   sibling<--head
        (i.e. we always call the node in the middle as "the sibling")

        :param edge_list: The list of edges represented as tuples

        :return: A list of three-tuples: (head, dep, sibling)
        """
        sibling_list = []
        edge_list_len = len(edge_list)

        for first_edge_index in range(edge_list_len - 1):
            for second_edge_index in range(first_edge_index + 1,
                                           edge_list_len):
                first_edge_tuple = edge_list[first_edge_index]
                second_edge_tuple = edge_list[second_edge_index]
                # If they do not share the same head, continue
                if first_edge_tuple[0] != second_edge_tuple[0]:
                    continue
                head_index = first_edge_tuple[0]
                dep_index = first_edge_tuple[1]
                sib_index = second_edge_tuple[1]

                # May erase this later!
                assert dep_index != sib_index

                if dep_index > head_index and sib_index > head_index:
                    # We always call the node
                    if dep_index > sib_index:
                        sibling_list.append((head_index, # Head
                                             dep_index,  # Dep
                                             sib_index)) # Sibling
                    else:
                        sibling_list.append((head_index, # Head
                                             sib_index,  # Dep (although the var
                                                         # name is sib_index)
                                             dep_index)) # Sibling
                elif dep_index < head_index and sib_index < head_index:
                    if dep_index > sib_index:
                        sibling_list.append((head_index, # Head
                                             sib_index,  # Dep
                                             dep_index)) # Sibling
                    else:
                        sibling_list.append((head_index, # Head
                                             dep_index,  # Dep
                                             sib_index)) # Sibling

        return sibling_list


    def find_grandchild_relation(self, edge_list):
        """
        Find all grandchild relation:

        head-->dep-->grandchild *or*
        grandchild<--dep<--head *or*
             |------<<<-----|
        grandchild  head-->dep  *or*
         |------>>>------|
        dep<--head  grandchild

        i.e. There is no order constraint, as long as
        the head, dep and grandchild node could be chained
        using two edges. (In contrast, in sibling relation
        this is not true. Sibling relation requires dep
         and sibling node on the same side of the head. But
         again direction is not a constraint in either cases)
        """
        grandchild_list = []
        edge_list_len = len(edge_list)

        for first_edge_index in range(edge_list_len - 1):
            for second_edge_index in range(first_edge_index + 1,
                                           edge_list_len):
                first_edge_tuple = edge_list[first_edge_index]
                second_edge_tuple = edge_list[second_edge_index]

                if first_edge_tuple[1] == second_edge_tuple[0]:
                    grandchild_list.append((first_edge_tuple[0],   # Head
                                            first_edge_tuple[1],   # dep
                                            second_edge_tuple[1])) # grand child
                elif first_edge_tuple[0] == second_edge_tuple[1]:
                    grandchild_list.append((second_edge_tuple[0],
                                            second_edge_tuple[1],
                                            first_edge_tuple[1]))
        return grandchild_list


    def recover_feature_from_edges(self, edge_list):
        """
        Recover sibling feature and grandchild feature from a list of edges
        The process consists of two stages:
            * Find sibling and grandchild relation respectively
            * Generate feature for them and aggregate into one feature vector
        """
        sibling_list = self.find_sibling_relation(edge_list)
        grandchild_list = self.find_grandchild_relation(edge_list)

        fv = feature_vector.FeatureVector()

        for head, dep in edge_list:
            local_fv = self.get_local_vector(head, dep)
            fv.aggregate(local_fv)

        for head, dep, sib in sibling_list:
            local_fv = self.get_local_vector(head, dep, [sib],
                                             self.SECOND_ORDER_SIBLING_ONLY)
            fv.aggregate(local_fv)

        for head, dep, gc in grandchild_list:
            local_fv = self.get_local_vector(head, dep, [gc],
                                             self.SECOND_ORDER_GRANDCHILD_ONLY)
            fv.aggregate(local_fv)

        return fv


##################################################################

def test():
    class test_class:  # mocking class that behaves like a tree
        word_list = ['ROOT', 'I', 'am', 'a', 'HAL9000', 'computer']
        pos_list  = ['_ROOT_', 'POS-I', 'POS-am', 'POS-a',
                     'POS-HAL9000', 'POS-computer']
        def get_word_list(self):
            return self.word_list
        def get_pos_list(self):
            return self.pos_list

    sentence = test_class()
    fg = SecondOrderFeatureGenerator(sentence)
    fv = fg.get_second_order_local_vector(1, 5, [3],
                             feature_type=FeatureGenerator.SECOND_ORDER_SIBLING)
    print(fv)

    return

if __name__ == '__main__':
    test()