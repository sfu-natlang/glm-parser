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

    def get_unigram_feature(self, head_index, dep_index, direction, dist):
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

        local_fv = []

        # Prepare keys
        local_fv.append( (0,0,xi_word,xi_pos) )
        local_fv.append( (0,1,xi_word) )
        local_fv.append( (0,2,xi_pos) )
        local_fv.append( (0,3,xj_word,xj_pos) )
        local_fv.append( (0,4,xj_word) )
        local_fv.append( (0,5,xj_pos) )

        # Add five gram features. Detect xi and xj separately

        if len(xi_word) > 5:
            xi_word_5 = self.five_gram_word_list[head_index]
            local_fv.append( (0,6, xi_word_5, xi_pos) )
            local_fv.append( (0,7, xi_word_5) )

        if len(xj_word) > 5:
            xj_word_5 = self.five_gram_word_list[dep_index]
            local_fv.append( (0,8,xj_word,xj_pos) )
            local_fv.append( (0,9,xj_word) )

        dir_dist_fv = self.get_dir_dist_feature(local_fv, direction, dist)
        return local_fv + dir_dist_fv

    def get_bigram_feature(self, head_index, dep_index, direction, dist):
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
        local_fv = []

        xi_word = self.word_list[head_index]
        xi_pos = self.pos_list[head_index]
        xj_word = self.word_list[dep_index]
        xj_pos = self.pos_list[dep_index]
        # Prepare keys
        local_fv.append( (1,0,xi_word,xi_pos,xj_word,xj_pos) )
        local_fv.append( (1,1,xi_pos,xj_word,xj_pos) )
        local_fv.append( (1,2,xi_word,xj_word,xj_pos) )
        local_fv.append( (1,3,xi_word,xi_pos,xj_pos) )
        local_fv.append( (1,4,xi_word,xi_pos,xj_word) )
        local_fv.append( (1,5,xi_word,xj_word) )
        local_fv.append( (1,6,xi_pos,xj_pos) )

        xi_word_5 = self.five_gram_word_list[head_index]
        xj_word_5 = self.five_gram_word_list[dep_index]

        # We guarantee that there are no five gram features will already
        # exist in the fv, so we only pick up those truly changes
        # (i.e. the five gram exists, and the feature itself contains
        # that word)
        if len(xi_word) > 5 or len(xj_word) > 5:
            local_fv.append( (1,7,xi_word_5,xi_pos,xj_word_5,xj_pos) )
            local_fv.append( (1,8,xi_pos,xj_word_5,xj_pos) )
            local_fv.append( (1,9,xi_word_5,xj_word_5,xj_pos) )
            local_fv.append( (1,10,xi_word_5,xi_pos,xj_pos) )
            local_fv.append( (1,11,xi_word_5,xi_pos,xj_word_5) )
            local_fv.append( (1,12,xi_word_5,xj_word_5) )

        dir_dist_fv = self.get_dir_dist_feature(local_fv, direction, dist)
        return local_fv + dir_dist_fv

    def get_in_between_feature(self, head_index, dep_index, direction, dist):
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
            return []

        # Fetch the two pos tag for xi and xj
        xi_pos = self.pos_list[head_index]
        xj_pos = self.pos_list[dep_index]

        local_fv = set()

        # Iterate through [start_index + 1,end_index - 1]
        for between_index in range(start_index + 1, end_index):
            xb_pos = self.pos_list[between_index]
            # Add all words between xi and xj into the feature
            local_fv.add( (2,0,xi_pos,xb_pos,xj_pos) )

        fv = list(local_fv)
        dir_dist_fv = self.get_dir_dist_feature(fv, direction, dist)
        return fv + dir_dist_fv

    def get_surrounding_feature(self, head_index, dep_index, direction, dist):
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

        local_fv = []

        local_fv.append( (3,0,xi_pos,xiplus_pos,xjminus_pos,xj_pos) )
        local_fv.append( (3,10,xi_pos,xjminus_pos,xj_pos) )
        local_fv.append( (3,20,xi_pos,xiplus_pos,xj_pos) )

        local_fv.append( (3,1,ximinus_pos,xi_pos,xjminus_pos,xj_pos) )
        local_fv.append( (3,11,xi_pos,xjminus_pos,xj_pos) )
        local_fv.append( (3,21,ximinus_pos,xi_pos,xj_pos) )

        local_fv.append( (3,2,xi_pos,xiplus_pos,xj_pos,xjplus_pos) )
        local_fv.append( (3,12,xi_pos,xj_pos,xjplus_pos) )
        local_fv.append( (3,22,xi_pos,xiplus_pos,xj_pos) )

        local_fv.append( (3,3,ximinus_pos,xi_pos,xj_pos,xjplus_pos) )
        local_fv.append( (3,13,xi_pos,xj_pos,xjplus_pos) )
        local_fv.append( (3,23,ximinus_pos,xi_pos,xj_pos) )

        dir_dist_fv = self.get_dir_dist_feature(local_fv, direction, dist)
        return local_fv + dir_dist_fv

    def get_dir_dist_feature(self, local_fv, direction, dist):
        """ 
        Add direction and dist attachment to all the features
        in the local_fv. Notice: local_fv shouldn't already have
        features with dist and direction attachment
        """
        dir_dist_fv = []
        for feature in local_fv:
            new_prefix = (feature[0], feature[1]*10+9)
            new_suffix = (direction, dist)
            dir_dist_fv.append( new_prefix + feature[2:] + new_suffix )
        return dir_dist_fv

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
        # Get dir and dist information prior to any computation
        direction, dist = self.get_dir_and_dist(head_index, dep_index)

        fv = []
        # Get Unigram features
        fv += self.get_unigram_feature(head_index, dep_index, direction, dist)
        # Get bigram features
        fv += self.get_bigram_feature(head_index, dep_index, direction, dist)
        # Get in-between features
        fv += self.get_in_between_feature(head_index, dep_index, direction, dist)
        # Get surrounding feature
        fv += self.get_surrounding_feature(head_index, dep_index, direction, dist)

        setfv = set(fv)
        duplicates = [ x for x in fv if fv.count(x) > 1 ]
        if len(duplicates) > 0:
            raise ValueError("fv has duplicates: %s" % (duplicates))

        return map(str, fv)

    def recover_feature_from_edges(self, edge_list):
        """
        Return a feature vector instance containing the features
        implied by edge list
        """
        fv = []

        for head, dep in edge_list:
            fv += self.get_local_vector(head, dep)
        
        return fv

