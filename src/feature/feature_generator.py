#
# Global Linear Model Parser
# Simon Fraser University
# NLP Lab
#
# Author: Yulan Huang, Ziqi Wang, Anoop Sarkar
# (Please add on your name if you have authored this file)
#

from weight.weight_vector import *
from feature.feature_vector import *

class FeatureGenerator():
    """
    Calculate feature for each sentence
    """
    def __init__(self, sent):
        """
        Initialize the FeatureSet instance, including a file name that might
        be used to store the database on the disk, and a dependency tree
        that provides only word list and pos list (i.e. no edge information)
        to the instance. The dependency tree should not be further modified
        after refistered into the instance, in order to maintain consistency.

        :param sent: The dependency tree that you want to train on
        :type sent: DependencyTree
        """
        # If you want a disk database with write through, use
        # self.w_vector = DataBackend("shelve_write_through")
        # If you want a disk data base with write back, use
        # self.w_vector = DataBackend("shelve_write_back")
        # If you want a memory database, use
        #self.w_vector = WeightVector()
        # We do this during initialization. For later stages if you need to
        # change the tree then just call that method manually
    
        if not sent == None:
            self.word_list = sent.get_word_list()
	    self.pos_list = sent.get_pos_list()
            # Add five gram word list
            self.compute_five_gram()
			
        return

    def compute_five_gram(self):
        """
        Computes a five gram feature based on the current word_list. The five
        gram is a list having the same length as the word_list, and it will be
        used to construct five gram features.

        Each list entry at position i correponds to the word at the same position
        in word_list, or None if the length of that word is already less than 5.
        This makes it easier to judge whether the length of a word is more than
        five, making it unnecessary to compute the length each time.
        """
        # Flush the old one
        self.five_gram_word_list = []
        # Compute a five_gram for all words. Pleace notice that for
        # those words less than 5 characters, we just push a None into
        # the list, therefore we could judge the length of the word against
        # 5 by reading the corresponding position in five_gram_word_list
        # instead of calculating it each time.
        for word in self.word_list:
            if len(word) > 5:
                self.five_gram_word_list.append(word[0:5])
            else:
                self.five_gram_word_list.append(None)

    #def dump(self,filename=None):
        """
        Save the content of the database to a disk file. The file name is given
        in the parameter. For persistent data objects, it will call the sync()
        method. But for memory dict it will call pickle procedure to implement
        the dump operation.

        :param filename: The name of the saved dump file. This will override
        the file name provided in the constructor
        :type filename: str
        """
    #    if filename == None:
    #        if self.database_filename == None:
    #            raise ValueError("""You must provide a file name or use the
    #                                default file name.""")
            # If None is passed then use the default file name provided to
            # the constructor
    #        else:
    #            filename = self.database_filename
        # This should work for both mem dict and persistent data object
    #    self.w_vector.dump(filename)
    #    return

    #def load(self,filename=None):
        """
        Load the content of a database from the disk file. For shelve types this
        could be saved, since shelve always works on disk file. However if you
        are using memory dictionary, each time you want to continue your job,
        you need to load the previous dumped one.
        """
    #    if filename == None:
    #        if self.database_filename == None:
    #            raise ValueError("""You must provide a file name or use the
    #                                default file name.""")
    #        else:
    #            filename = self.database_filename
    #    self.w_vector.load(filename)
    #    return
    
    def get_unigram_feature(self,fv,head_index,dep_index,five_gram=True):
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
        
            (0,type,xi/xj_[word,pos])

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
        
        # Prepare keys
        type0_str = str((0,0,xi_word,xi_pos))
        type1_str = str((0,1,xi_word))
        type2_str = str((0,2,xi_pos))
        type3_str = str((0,3,xj_word,xj_pos))
        type4_str = str((0,4,xj_word))
        type5_str = str((0,5,xj_pos))
        # Set all unigram features to 1
        fv[type0_str] = 1
        fv[type1_str] = 1
        fv[type2_str] = 1
        fv[type3_str] = 1
        fv[type4_str] = 1
        fv[type5_str] = 1

        # Add five gram features. Detect xi and xj separately
        if five_gram == True:
            xi_word_5 = self.five_gram_word_list[head_index]
            xj_word_5 = self.five_gram_word_list[dep_index]
            
            if xi_word_5 != None:
                type0_str_5 = str((0,0,xi_word_5,xi_pos))
                type1_str_5 = str((0,1,xi_word_5))
                fv[type0_str_5] = 1
                fv[type1_str_5] = 1

            if xj_word_5 != None:
                type3_str_5 = str((0,3,xj_word,xj_pos))
                type4_str_5 = str((0,4,xj_word))
                fv[type3_str_5] = 1
                fv[type4_str_5] = 1
        
        return
    
    def get_bigram_feature(self,fv,head_index,dep_index,five_gram=True):
        """
        Add all bigram features into a given feature vector instance.
        There should be no conflict about feature strings, i.e. no feature
        should already exist in the feature vector instance. Unigram features
        are:
            +----------------------------------+
            | xi-word, xi-pos, xj-word, xj-pos | type = 0
            | xi-pos, xj-word, xj-pos          | type = 1
            | xi-word, xj-word, xj-pos         | type = 2
            | xi-word, xi-pos, xj-pos          | type = 3
            | xi-word, xi-pos, xj-word         | type = 4
            | xi-word, xj-word                 | type = 5
            | xi-pos, xj-pos                   | type = 6
            +----------------------------------+
        Basic features are represented using a tuple. The first element is
        integer 1, indicating that it is a bigram feature. The second element
        is also an integer, the value to meaning mapping is listed above:
        
            (1,type,xi/xj_[word,pos,word,pos])

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
        # Prepare keys
        type0_str = str((1,0,xi_word,xi_pos,xj_word,xj_pos))
        type1_str = str((1,1,xi_pos,xj_word,xj_pos))
        type2_str = str((1,2,xi_word,xj_word,xj_pos))
        type3_str = str((1,3,xi_word,xi_pos,xj_pos))
        type4_str = str((1,4,xi_word,xi_pos,xj_word))
        type5_str = str((1,5,xi_word,xj_word))
        type6_str = str((1,6,xi_pos,xj_pos))
        # Set all unigram features to 1
        fv[type0_str] = 1
        fv[type1_str] = 1
        fv[type2_str] = 1
        fv[type3_str] = 1
        fv[type4_str] = 1
        fv[type5_str] = 1
        fv[type6_str] = 1

        if five_gram == True:
            xi_word_5 = self.five_gram_word_list[head_index]
            xj_word_5 = self.five_gram_word_list[dep_index]

            # We guarantee that there are no five gram features will already
            # exist in the fv, so we only pick up those truly changes
            # (i.e. the five gram exists, and the feature itself contains
            # that word)
            
            if xi_word_5 != None and xj_word_5 != None:
                type0_str_5 = str((1,0,xi_word_5,xi_pos,xj_word_5,xj_pos))
                type1_str_5 = str((1,1,xi_pos,xj_word_5,xj_pos))
                type2_str_5 = str((1,2,xi_word_5,xj_word_5,xj_pos))
                type3_str_5 = str((1,3,xi_word_5,xi_pos,xj_pos))
                type4_str_5 = str((1,4,xi_word_5,xi_pos,xj_word_5))
                type5_str_5 = str((1,5,xi_word_5,xj_word_5))
                fv[type0_str_5] = 1
                fv[type1_str_5] = 1
                fv[type2_str_5] = 1
                fv[type3_str_5] = 1
                fv[type4_str_5] = 1
                fv[type5_str_5] = 1

            if xi_word_5 != None:
                type0_str_5 = str((1,0,xi_word_5,xi_pos,xj_word_5,xj_pos))
                type2_str_5 = str((1,2,xi_word_5,xj_word_5,xj_pos))
                type3_str_5 = str((1,3,xi_word_5,xi_pos,xj_pos))
                type4_str_5 = str((1,4,xi_word_5,xi_pos,xj_word_5))
                type5_str_5 = str((1,5,xi_word_5,xj_word_5))
                fv[type0_str_5] = 1
                fv[type2_str_5] = 1
                fv[type3_str_5] = 1
                fv[type4_str_5] = 1
                fv[type5_str_5] = 1

            if xj_word_5 != None:
                type0_str_5 = str((1,0,xi_word_5,xi_pos,xj_word_5,xj_pos))
                type1_str_5 = str((1,1,xi_pos,xj_word_5,xj_pos))
                type2_str_5 = str((1,2,xi_word_5,xj_word_5,xj_pos))
                type4_str_5 = str((1,4,xi_word_5,xi_pos,xj_word_5))
                type5_str_5 = str((1,5,xi_word_5,xj_word_5))
                fv[type0_str_5] = 1
                fv[type1_str_5] = 1
                fv[type2_str_5] = 1
                fv[type4_str_5] = 1
                fv[type5_str_5] = 1
        
        return

    def get_in_between_feature(self,fv,head_index,dep_index):
        """
        Add in-between features in to a feature vector instance. These features
        are:

        +------------------------+
        | xi-pos, xb-pos, xj-pos | No type information
        +------------------------+
        (For all xb in the middle of xi and xj)

        (2,xi-pos,xb-pos,xj-pos)

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
            
        # If these two words are ajdacent then we do not need to add anything
        # since there is no in-between features
        if start_index + 1 == end_index:
            return fv

        # Fetch the two pos tag for xi and xj
        xi_pos = self.pos_list[head_index]
        xj_pos = self.pos_list[dep_index]
        
        # Iterate through [start_index + 1,end_index - 1]
        for between_index in range(start_index + 1,end_index):
            xb_pos = self.pos_list[between_index]
            # Add all words between xi and xj into the feature
            feature_str = str((2,xi_pos,xb_pos,xj_pos))
            # Binary function
            fv[feature_str] = 1
            
        return

    def get_surrounding_feature(self,fv,head_index,dep_index):
        """
        Add surrounding POS features into the feature vector. These features are

        +------------------------------------+
        | xi_pos, xi+1_pos, xj-1_pos, xj_pos | type = 0
        | xi_pos, xi+1_pos,         , xj_pos | type = 10
        | xi_pos,           xj-1_pos, xj_pos | type = 20
        | xi-1_pos, xi_pos, xj-1_pos, xj_pos | type = 1
        |           xi_pos, xj-1_pos, xj_pos | type = 11
        | xi-1_pos, xi_pos,           xj_pos | type = 21
        | xi_pos, xi+1_pos, xj_pos, xj+1_pos | type = 2
        | xi_pos,           xj_pos, xj+1_pos | type = 12
        | xi_pos, xi+1_pos, xj_pos           | type = 22
        | xi-1_pos, xi_pos, xj_pos, xj+1_pos | type = 3
        |           xi_pos, xj_pos, xj+1_pos | type = 13
        | xi-1_pos, xi_pos, xj_pos           | type = 23
        +------------------------------------+
        If xi or xj is at the boundary (the first word or the last word) then
        there will be out of bound error. In this case we just put a None

        (3,type,xi_pos,xi[+/-1]_pos,xi[+/-1]_pos,xj[+/-1]_pos,xj[+/-1]_pos)

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

        type0_str = str((3,0,xi_pos,xiplus_pos,xjminus_pos,xj_pos))
        type10_str = str((3,10,xi_pos,xjminus_pos,xj_pos))
        type20_str = str((3,20,xi_pos,xiplus_pos,xj_pos))
        
        type1_str = str((3,1,ximinus_pos,xi_pos,xjminus_pos,xj_pos))
        type11_str = str((3,11,xi_pos,xjminus_pos,xj_pos))
        type21_str = str((3,21,ximinus_pos,xi_pos,xj_pos))
        
        type2_str = str((3,2,xi_pos,xiplus_pos,xj_pos,xjplus_pos))
        type12_str = str((3,12,xi_pos,xj_pos,xjplus_pos))
        type22_str = str((3,22,xi_pos,xiplus_pos,xj_pos))
        
        type3_str = str((3,3,ximinus_pos,xi_pos,xj_pos,xjplus_pos))
        type13_str = str((3,13,xi_pos,xj_pos,xjplus_pos))
        type23_str = str((3,23,ximinus_pos,xi_pos,xj_pos))

        fv[type0_str] = 1
        fv[type10_str] = 1
        fv[type20_str] = 1
        
        fv[type1_str] = 1
        fv[type11_str] = 1
        fv[type21_str] = 1
        
        fv[type2_str] = 1
        fv[type12_str] = 1
        fv[type22_str] = 1
        
        fv[type3_str] = 1
        fv[type13_str] = 1
        fv[type23_str] = 1

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

        type1_str = str((4, 1, xi_pos, xk_pos, xj_pos))
        type2_str = str((4, 2, xk_pos, xj_pos))
        type3_str = str((4, 3, xk_word, xj_word))
        type4_str = str((4, 4, xk_word, xj_pos))
        type5_str = str((4, 5, xk_pos, xj_word))

        fv[type1_str] = 1
        fv[type2_str] = 1
        fv[type3_str] = 1
        fv[type4_str] = 1
        fv[type5_str] = 1

        return

    def get_2nd_grandparent_feature(self, fv, head_index, dep_index, gc_index):
        """
        Add geandchild feature into the feature vector

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

        type1_str = str((5, 1, xi_pos, xk_pos, xj_pos))
        type2_str = str((5, 2, xk_pos, xj_pos))
        type3_str = str((5, 3, xk_word, xj_word))
        type4_str = str((5, 4, xk_word, xj_pos))
        type5_str = str((5, 5, xk_pos, xj_word))

        fv[type1_str] = 1
        fv[type2_str] = 1
        fv[type3_str] = 1
        fv[type4_str] = 1
        fv[type5_str] = 1

        return

    def add_dir_and_dist(self, fv, head_index, dep_index):
        """
        Add additional distance and direction information in a given feature
        vector. All existing features will be iterated through, and new
        features will be constructed based on these existing features as well
        as the edge information. All distance are calculated into the bucket
        of 1 2 3 4 5 and 10, i.e. if some dist is more than 5 but less than 10
        then it will be counted as 5. If some dist is more than 10 then it is
        counted as 10.

        The costructed features are also tuples, the first element being the
        original tuple, the second and the third being the dir and dist:

            ([original_feature],dir,dist)

        :param head_index: The index of the head node
        :type head_index: integer
        :param dep_index: The index of the dependency node
        :type dep_node: integer
        """
        if head_index < dep_index:
            #start_index = head_index
            #end_index = dep_index
            dist = dep_index - head_index + 1
            direction = 'R'
        else:
            #start_index = dep_index
            #end_index = head_index
            dist = head_index - dep_index + 1
            direction = 'L'

        if dist > 5:
            if dist < 10:
                dist = 5
            else:
                dist = 10
        
        for feature in fv.keys():
            new_feature_str = str((feature,direction,dist))
            fv[new_feature_str] = 1
            
        return

    # This method could be replaced by get_higher_order_local_vector(),
    # but is defined separately to keep interface unchanged for first
    # order feature parser (which was implemented when we did not consider)
    # higher order features.
    def get_local_vector(self, head_index, dep_index):
        """
        Return first order features (with dist and dir annotation)

        :param head_index: Head index
        :param dep_index: Dependency index
        :return: FeatureVector instance
        """
        local_fv = FeatureVector()

        # Get Unigram features
        self.get_unigram_feature(local_fv,head_index,dep_index)
        # Get bigram features
        self.get_bigram_feature(local_fv,head_index,dep_index)
        # Get in-between features
        self.get_in_between_feature(local_fv,head_index,dep_index)
        # Get sorrounding feature
        self.get_surrounding_feature(local_fv,head_index,dep_index)
        # For future improvements please put all other features here
        # ...

        # Add dir and dist information for all features. This can be done
        # uniformly since the edge is the same.
        self.add_dir_and_dist(local_fv,head_index,dep_index)

        return local_fv


    # Here defines some feature type. Used in method get_local_vector
    FIRST_ORDER = 0
    SECOND_ORDER_SIBLING = 1
    SECOND_ORDER_GRANDCHILD = 2
    SECOND_ORDER_SIBLING_ONLY = 3
    SECOND_ORDER_GRANDCHILD_ONLY = 4

    def get_second_order_local_vector(self, head_index, dep_index,
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
        if (feature_type == self.SECOND_ORDER_SIBLING and
            other_index_list[0] is None):
            feature_type = self.FIRST_ORDER

        # Docorated with dist and dir; do not do this again
        local_fv_1st = self.get_local_vector(head_index, dep_index)
        # Fast path: return directly if only 1st order are evaluated
        if feature_type == self.FIRST_ORDER:
            return local_fv_1st

        local_fv_second_order = FeatureVector()
        if (feature_type == self.SECOND_ORDER_SIBLING or
            feature_type == self.SECOND_ORDER_SIBLING_ONLY):
            sibling_index = other_index_list[0]
            self.get_2nd_sibling_feature(local_fv_second_order,
                                         head_index, dep_index,
                                         sibling_index)
            # From sibling to dependent node (we assume the sibling
            # node is between the head and dependent node)
            self.add_dir_and_dist(local_fv_second_order,
                                  sibling_index, dep_index)

            if feature_type == feature_type == self.SECOND_ORDER_SIBLING_ONLY:
                return local_fv_second_order
        elif (feature_type == self.SECOND_ORDER_GRANDCHILD or
              feature_type == self.SECOND_ORDER_GRANDCHILD_ONLY):
            grandchild_index = other_index_list[0]
            self.get_2nd_grandparent_feature(local_fv_second_order,
                                             head_index, dep_index,
                                             grandchild_index)
            # From dependent node to grand child
            self.add_dir_and_dist(local_fv_second_order,
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
    
    def print_local_vector(self,head_index,dep_index):
        """
        Print out all feature keys in an (actually not) elegant form
        """
        fv = self.get_local_vector(head_index,dep_index)
        for i in fv.keys():
            print i
        return

#TODO move to WeightVector ??
    def merge(self,fs):
        """
        Merge this feature set instance with another instance. The sharing keys
        will be added up together to produce a new parameter value, and the
        unique keys are copied from the sources. This method will change the
        instance it is calling from in-place. If you need a new instance as the
        result of an addition, call the operator overloading __add__

        Please notice that after merge, the second FeatureSet instance will
        be cleared. This is done to prevent memory error.

        :param fs: The feature set instance you want to merge from
        :type fs: FeatureSet instance
        """
        # We only need to check the key
        for fk in fs.keys():
            # If key already exists then merge by addition
            if self.has_key(fk):
                self[fk] += fs[fk]
            # If key does not exist then just add the key
            else:
                self[fk] = fs[fk]
            # We would like to keep the two dictionaries as small as possible
            fs.pop(fk)
        return

#############################################################################
# Unit test code

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
    fg = FeatureGenerator(sentence)
    fv = fg.get_second_order_local_vector(1, 5, [3],
                             feature_type=FeatureGenerator.SECOND_ORDER_SIBLING)
    print(fv)

    return

if __name__ == '__main__':
    test()