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
import feature_generator_base
import debug.debug


class FirstOrderFeatureGenerator(feature_generator_base.FeatureGeneratorBase):
    """
    First order feature generator for english
    """

    def __init__(self, sent):
        """
        Delegate initializer to its parent class

        This stub is avoidable, but we choose to keep it here for two reasons. First,
        for those not familiar with Python or OOP, this is a hint that the call to
        initializer goes to the base class. And secondly, if we want to customize
        the initializer this stub saves some typing.
        """
        feature_generator_base.FeatureGeneratorBase.__init__(self, sent)
        return

    def get_unigram_feature(self, fv, head_index, dep_index, direction, dist):
        """
        Add all unigram features into a given feature vector instance.
        There should be no conflict about feature strings, i.e. no feature
        should already exist in the feature vector instance. Unigram features
        are:
            +-----------------+
            | xi-word, xi-pos | type = 0
            | xi-word         | type = 1
            | xi-pos          | type = 2
            | xj-word, xj-pos | type = 3
            | xj-word         | type = 4
            | xj-pos          | type = 5
            +-----------------+

        Basic features are represented using a tuple. The first element is
        integer 0, indicating that it is a unigram feature. The second element
        is also an integer, the value to meaning mapping is listed above:

            (type,xi/xj_[word,pos])

        :param fv: A feature vector instance
        :type fv: FeatureVector
        :param head_index: The index of the head node
        :type head_index: integer
        :paramn dep_index: The index of the dependency node
        :type dep_index: integer
        """
        xi_word = self.word_list[head_index]
        xi_pos = self.pos_list[head_index]
        xj_word = self.word_list[dep_index]
        xj_pos = self.pos_list[dep_index]

        key_gen_func = self.key_gen_func

        # Prepare keys
        type0_str = key_gen_func((0,0,xi_word,xi_pos))
        type1_str = key_gen_func((0,1,xi_word))
        type2_str = key_gen_func((0,2,xi_pos))
        type3_str = key_gen_func((0,3,xj_word,xj_pos))
        type4_str = key_gen_func((0,4,xj_word))
        type5_str = key_gen_func((0,5,xj_pos))

        # Set all unigram features to 1
        #fv[type0_str] = 1
        #fv[type1_str] = 1
        #fv[type2_str] = 1
        #fv[type3_str] = 1
        #fv[type4_str] = 1
        #fv[type5_str] = 1

        fv.append(type0_str)
        fv.append(type1_str)
        fv.append(type2_str)
        fv.append(type3_str)
        fv.append(type4_str)
        fv.append(type5_str)

        fv.append(key_gen_func((type0_str, direction, dist)))
        fv.append(key_gen_func((type1_str, direction, dist)))
        fv.append(key_gen_func((type2_str, direction, dist)))
        fv.append(key_gen_func((type3_str, direction, dist)))
        fv.append(key_gen_func((type4_str, direction, dist)))
        fv.append(key_gen_func((type5_str, direction, dist)))

        # Add five gram features. Detect xi and xj separately

        xi_word_5 = self.five_gram_word_list[head_index]
        xj_word_5 = self.five_gram_word_list[dep_index]

        if xi_word_5 is not None:
            type0_str_5 = key_gen_func((0,0, xi_word_5, xi_pos))
            type1_str_5 = key_gen_func((0,1, xi_word_5))
            fv.append(type0_str_5)
            fv.append(type1_str_5)

            fv.append(key_gen_func((type0_str_5)))
            fv.append(key_gen_func((type1_str_5)))

        if xj_word_5 is not None:
            type3_str_5 = key_gen_func((0,3,xj_word,xj_pos))
            type4_str_5 = key_gen_func((0,4,xj_word))
            fv.append(type3_str_5)
            fv.append(type4_str_5)

            fv.append(key_gen_func((type3_str_5)))
            fv.append(key_gen_func((type4_str_5)))

        return

    def get_bigram_feature(self, fv, head_index, dep_index, direction, dist):
        """
        Add all bigram features into a given feature vector instance.
        There should be no conflict about feature strings, i.e. no feature
        should already exist in the feature vector instance. Unigram features
        are:
            +----------------------------------+
            | xi-word, xi-pos, xj-word, xj-pos | type = 10
            | xi-pos, xj-word, xj-pos          | type = 11
            | xi-word, xj-word, xj-pos         | type = 12
            | xi-word, xi-pos, xj-pos          | type = 13
            | xi-word, xi-pos, xj-word         | type = 14
            | xi-word, xj-word                 | type = 15
            | xi-pos, xj-pos                   | type = 16
            +----------------------------------+

        Basic features are represented using a tuple. The first element is
        integer 1, indicating that it is a bigram feature. The second element
        is also an integer, the value to meaning mapping is listed above:

            (type,xi/xj_[word,pos,word,pos])

        :param fv: A feature vector instance
        :type fv: FeatureVector

        :param head_index: The index of the head node
        :type head_index: integer
        :paramn dep_index: The index of the dependency node
        :type dep_index: integer
        """
        key_gen_func = self.key_gen_func

        xi_word = self.word_list[head_index]
        xi_pos = self.pos_list[head_index]
        xj_word = self.word_list[dep_index]
        xj_pos = self.pos_list[dep_index]
        # Prepare keys
        type0_str = key_gen_func((1,0,xi_word,xi_pos,xj_word,xj_pos))
        type1_str = key_gen_func((1,1,xi_pos,xj_word,xj_pos))
        type2_str = key_gen_func((1,2,xi_word,xj_word,xj_pos))
        type3_str = key_gen_func((1,3,xi_word,xi_pos,xj_pos))
        type4_str = key_gen_func((1,4,xi_word,xi_pos,xj_word))
        type5_str = key_gen_func((1,5,xi_word,xj_word))
        type6_str = key_gen_func((1,6,xi_pos,xj_pos))

        # Set all unigram features to 1
        fv.append(type0_str)
        fv.append(type1_str)
        fv.append(type2_str)
        fv.append(type3_str)
        fv.append(type4_str)
        fv.append(type5_str)
        fv.append(type6_str)

        fv.append(key_gen_func((type0_str, direction, dist)))
        fv.append(key_gen_func((type1_str, direction, dist)))
        fv.append(key_gen_func((type2_str, direction, dist)))
        fv.append(key_gen_func((type3_str, direction, dist)))
        fv.append(key_gen_func((type4_str, direction, dist)))
        fv.append(key_gen_func((type5_str, direction, dist)))
        fv.append(key_gen_func((type6_str, direction, dist)))

        xi_word_5 = self.five_gram_word_list[head_index]
        xj_word_5 = self.five_gram_word_list[dep_index]

        # We guarantee that there are no five gram features will already
        # exist in the fv, so we only pick up those truly changes
        # (i.e. the five gram exists, and the feature itself contains
        # that word)

        if xi_word_5 is not None and xj_word_5 is not None:
            type0_str_5 = key_gen_func((1,0,xi_word_5,xi_pos,xj_word_5,xj_pos))
            type1_str_5 = key_gen_func((1,1,xi_pos,xj_word_5,xj_pos))
            type2_str_5 = key_gen_func((1,2,xi_word_5,xj_word_5,xj_pos))
            type3_str_5 = key_gen_func((1,3,xi_word_5,xi_pos,xj_pos))
            type4_str_5 = key_gen_func((1,4,xi_word_5,xi_pos,xj_word_5))
            type5_str_5 = key_gen_func((1,5,xi_word_5,xj_word_5))
            fv.append(type0_str_5)
            fv.append(type1_str_5)
            fv.append(type2_str_5)
            fv.append(type3_str_5)
            fv.append(type4_str_5)
            fv.append(type5_str_5)

            fv.append(key_gen_func((type0_str_5)))
            fv.append(key_gen_func((type1_str_5)))
            fv.append(key_gen_func((type2_str_5)))
            fv.append(key_gen_func((type3_str_5)))
            fv.append(key_gen_func((type4_str_5)))
            fv.append(key_gen_func((type5_str_5)))

        if xi_word_5 is not None:
            type0_str_5 = key_gen_func((1,0,xi_word_5,xi_pos,xj_word_5,xj_pos))
            type2_str_5 = key_gen_func((1,2,xi_word_5,xj_word_5,xj_pos))
            type3_str_5 = key_gen_func((1,3,xi_word_5,xi_pos,xj_pos))
            type4_str_5 = key_gen_func((1,4,xi_word_5,xi_pos,xj_word_5))
            type5_str_5 = key_gen_func((1,5,xi_word_5,xj_word_5))
            fv.append(type0_str_5)
            fv.append(type2_str_5)
            fv.append(type3_str_5)
            fv.append(type4_str_5)
            fv.append(type5_str_5)

            fv.append(key_gen_func((type0_str_5)))
            fv.append(key_gen_func((type2_str_5)))
            fv.append(key_gen_func((type3_str_5)))
            fv.append(key_gen_func((type4_str_5)))
            fv.append(key_gen_func((type5_str_5)))

        if xj_word_5 is not None:
            type0_str_5 = key_gen_func((1,0,xi_word_5,xi_pos,xj_word_5,xj_pos))
            type1_str_5 = key_gen_func((1,1,xi_pos,xj_word_5,xj_pos))
            type2_str_5 = key_gen_func((1,2,xi_word_5,xj_word_5,xj_pos))
            type4_str_5 = key_gen_func((1,4,xi_word_5,xi_pos,xj_word_5))
            type5_str_5 = key_gen_func((1,5,xi_word_5,xj_word_5))
            fv.append(type0_str_5)
            fv.append(type1_str_5)
            fv.append(type2_str_5)
            fv.append(type4_str_5)
            fv.append(type5_str_5)

            fv.append(key_gen_func((type0_str_5)))
            fv.append(key_gen_func((type1_str_5)))
            fv.append(key_gen_func((type2_str_5)))
            fv.append(key_gen_func((type4_str_5)))
            fv.append(key_gen_func((type5_str_5)))

        return

    def get_in_between_feature(self, fv, head_index, dep_index, direction, dist):
        """
        Add in-between features in to a feature vector instance. These features
        are:

        +------------------------+
        | xi-pos, xb-pos, xj-pos | No type information
        +------------------------+
        (For all xb in the middle of xi and xj)

        (20,xi-pos,xb-pos,xj-pos)

        :param head_index: The index of the head node
        :type head_index: integer
        :param dep_index: The index of the dependency node
        :type dep_node: integer
        """
        # We assume these two will not be the same (maintained by the caller)
        if head_index > dep_index:
            start_index = dep_index
            end_index = head_index
        else:
            start_index = head_index
            end_index = dep_index

        # If these two words are adjacent then we do not need to add anything
        # since there is no in-between features
        if start_index + 1 == end_index:
            return

        # Fetch the two pos tag for xi and xj
        xi_pos = self.pos_list[head_index]
        xj_pos = self.pos_list[dep_index]

        key_gen_func = self.key_gen_func

        # Iterate through [start_index + 1,end_index - 1]
        for between_index in range(start_index + 1, end_index):
            xb_pos = self.pos_list[between_index]
            # Add all words between xi and xj into the feature
            feature_str = key_gen_func((2,xi_pos,xb_pos,xj_pos))
            # Binary function
            fv.append(feature_str)
            fv.append(key_gen_func((feature_str, direction, dist)))

        return

    def get_surrounding_feature(self, fv, head_index, dep_index, direction, dist):
        """
        Add surrounding POS features into the feature vector. These features are

        +------------------------------------+
        | xi_pos, xi+1_pos, xj-1_pos, xj_pos | type = 30
        | xi_pos, xi+1_pos,         , xj_pos | type = 310
        | xi_pos,           xj-1_pos, xj_pos | type = 320
        | xi-1_pos, xi_pos, xj-1_pos, xj_pos | type = 31
        |           xi_pos, xj-1_pos, xj_pos | type = 311
        | xi-1_pos, xi_pos,           xj_pos | type = 321
        | xi_pos, xi+1_pos, xj_pos, xj+1_pos | type = 32
        | xi_pos,           xj_pos, xj+1_pos | type = 312
        | xi_pos, xi+1_pos, xj_pos           | type = 322
        | xi-1_pos, xi_pos, xj_pos, xj+1_pos | type = 33
        |           xi_pos, xj_pos, xj+1_pos | type = 313
        | xi-1_pos, xi_pos, xj_pos           | type = 323
        +------------------------------------+
        If xi or xj is at the boundary (the first word or the last word) then
        there will be out of bound error. In this case we just put a None

        (type,xi_pos,xi[+/-1]_pos,xi[+/-1]_pos,xj[+/-1]_pos,xj[+/-1]_pos)

        :param head_index: The index of the head node
        :type head_index: integer
        :param dep_index: The index of the dependency node
        :type dep_node: integer
        """
        # This is used to detect out of bound case
        len_pos_list = len(self.pos_list)
        xi_pos = self.pos_list[head_index]
        xj_pos = self.pos_list[dep_index]
        # xi+1_pos
        if head_index + 1 == len_pos_list:
            xiplus_pos = None
        else:
            xiplus_pos = self.pos_list[head_index + 1]

        # xi-1_pos
        if head_index == 0:
            ximinus_pos = None
        else:
            ximinus_pos = self.pos_list[head_index - 1]

        # xj+1_pos
        if dep_index + 1 == len_pos_list:
            xjplus_pos = None
        else:
            xjplus_pos = self.pos_list[dep_index + 1]

        # xj-1_pos
        if dep_index == 0:
            xjminus_pos = None
        else:
            xjminus_pos = self.pos_list[dep_index - 1]

        key_gen_func = self.key_gen_func

        type0_str = key_gen_func((3,0,xi_pos,xiplus_pos,xjminus_pos,xj_pos))
        type10_str = key_gen_func((3,10,xi_pos,xjminus_pos,xj_pos))
        type20_str = key_gen_func((3,20,xi_pos,xiplus_pos,xj_pos))

        type1_str = key_gen_func((3,1,ximinus_pos,xi_pos,xjminus_pos,xj_pos))
        type11_str = key_gen_func((3,11,xi_pos,xjminus_pos,xj_pos))
        type21_str = key_gen_func((3,21,ximinus_pos,xi_pos,xj_pos))

        type2_str = key_gen_func((3,2,xi_pos,xiplus_pos,xj_pos,xjplus_pos))
        type12_str = key_gen_func((3,12,xi_pos,xj_pos,xjplus_pos))
        type22_str = key_gen_func((3,22,xi_pos,xiplus_pos,xj_pos))

        type3_str = key_gen_func((3,3,ximinus_pos,xi_pos,xj_pos,xjplus_pos))
        type13_str = key_gen_func((3,13,xi_pos,xj_pos,xjplus_pos))
        type23_str = key_gen_func((3,23,ximinus_pos,xi_pos,xj_pos))

        fv.append(type0_str)
        fv.append(type10_str)
        fv.append(type20_str)
        fv.append(type1_str)
        fv.append(type11_str)
        fv.append(type21_str)
        fv.append(type2_str)
        fv.append(type12_str)
        fv.append(type22_str)
        fv.append(type3_str)
        fv.append(type13_str)
        fv.append(type23_str)
        fv.append(key_gen_func((type0_str, direction, dist)))
        fv.append(key_gen_func((type10_str, direction, dist)))
        fv.append(key_gen_func((type20_str, direction, dist)))
        fv.append(key_gen_func((type1_str, direction, dist)))
        fv.append(key_gen_func((type11_str, direction, dist)))
        fv.append(key_gen_func((type21_str, direction, dist)))
        fv.append(key_gen_func((type2_str, direction, dist)))
        fv.append(key_gen_func((type12_str, direction, dist)))
        fv.append(key_gen_func((type22_str, direction, dist)))
        fv.append(key_gen_func((type3_str, direction, dist)))
        fv.append(key_gen_func((type13_str, direction, dist)))
        fv.append(key_gen_func((type23_str, direction, dist)))

        return

    def get_local_vector(self, head_index, dep_index, other_index_list=None,
                         feature_type=None):
        """
        Return first order local vector, which includes
            * Unigram feature
            * Bigram feature
            * In-between feature
            * Surrounding feature

        Argument other_index_list and feature_type is not used for first order
        features, but we keep them for compatibility purpose.
        """
        local_fv = []
        fv = feature_vector.FeatureVector()

        self.add_local_vector(local_fv, head_index, dep_index)
        for feature in local_fv:
            fv[feature] = 1

        return fv

    def add_local_vector(self, local_fv, head_index, dep_index):
        """
        An alternative and lightweight version of get_local_vector

        It differs from get_local_vector() in two aspects. First, it takes a
        local vector object as argument, which saves time if that fv already has
        some features added (most probably, higher order features). Besides,
        this method only takes head index and dependency index, which is quite convenient
        to use
        """
        # Get dir and dist information prior to any computation
        direction, dist = self.get_dir_and_dist(head_index, dep_index)

        # Get Unigram features
        self.get_unigram_feature(local_fv, head_index, dep_index, direction, dist)
        # Get bigram features
        self.get_bigram_feature(local_fv, head_index, dep_index, direction, dist)
        # Get in-between features
        self.get_in_between_feature(local_fv, head_index, dep_index, direction, dist)
        # Get surrounding feature
        self.get_surrounding_feature(local_fv, head_index, dep_index, direction, dist)

        return

    def recover_feature_from_edges(self, edge_list):
        """
        Return a feature vector instance containing the features
        implied by edge list
        """
        fv = []
        fvdict = feature_vector.FeatureVector()

        for head, dep in edge_list:
            self.add_local_vector(fv, head, dep)
        
        for i in fv:
            fvdict[i] = 1

        return fvdict

