from weight.weight_vector import *
from feature.feature_vector import *

class FeatureGenerator():
    """
    Calculate feature for each sentence
    """
    def __init__(self, sent=None):
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
            self.spine_list = sent.get_spine_list()
            self.label_list = sent.get_label_list()

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

    def get_unigram_spinal_feature(self,fv,head_index,dep_index):
        """
        Add all unigram-spinal features into a given feature vector instance.
            +----------------------------------+
            | xi-spine                         | type = 0
            | xj-spine                         | type = 1
            | xi-word, xi-pos, xi-spine        | type = 2
            | xi-word, xi-spine                | type = 3
            | xi-pos, xi-spine                 | type = 4
            | xj-word, xj-pos, xj-spine        | type = 5
            | xj-word, xj-spine                | type = 6
            | xj-pos, xj-spine                 | type = 7
            +----------------------------------+
        Basic features are represented using a tuple. The first element is
        integer 4, indicating that it is a unigram-spinal feature. The second element
        is also an integer, the value to meaning mapping is listed above:
        
            (4,type,xi/xj_[word,pos,spine,word,pos,spine])

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
        xi_spine = self.spine_list[dep_index]
        xj_spine = self.spine_list[head_index]

        # Prepare keys
        type0_str = str((4,0,xi_spine))
        type1_str = str((4,1,xj_spine))
        type2_str = str((4,2,xi_word,xi_pos,xi_spine))
        type3_str = str((4,3,xi_word,xi_spine))
        type4_str = str((4,4,xi_pos,xi_spine))
        type5_str = str((4,5,xj_word,xj_pos,xj_spine))
        type6_str = str((4,6,xj_word,xj_spine))
        type7_str = str((4,7,xj_pos,xj_spine))

        # Set all unigram-spinal features to 1; same feature count will
        # be aggregated 
        fv[type0_str] = 1
        fv[type1_str] = 1
        fv[type2_str] = 1
        fv[type3_str] = 1
        fv[type4_str] = 1
        fv[type5_str] = 1
        fv[type6_str] = 1
        fv[type7_str] = 1

        return

    def get_bigram_spinal_feature(self,fv,head_index,dep_index):
        """
        Add all bigram-spinal features into a given feature vector instance.
        +-------------------------------------------+
        | xi_word, xi_spine, xj_word                | type = 0
        | xi_word, xi_spine, xj_word, xj_pos        | type = 1
        | xi_word, xi_pos, xi_spine, xj_word        | type = 2
        | xi_word, xi_pos, xi_spine, xj_word,xj_pos | type = 3
        | xi_word, xi_pos, xi_spine, xj_pos         | type = 4
        | xi_pos, xi_spine, xj_pos                  | type = 5
        | xi_pos, xi_spine, xj_word, xj_pos         | type = 6
        | xj_word, xj_spine, xi_word                | type = 7
        | xj_word, xj_spine, xi_word, xi_pos        | type = 8
        | xj_word, xj_pos, xj_spine, xi_word        | type = 9
        | xj_word, xj_pos, xj_spine, xi_word, xi_pos| type = 10
        | xj_word, xj_pos, xj_spine, xi_pos         | type = 11
        | xj_pos, xj_spine, xi_pos))                | type = 12
        | xj_pos, xj_spine, xi_word, xi_pos         | type = 13
        +-------------------------------------------+
        Basic features are represented using a tuple. The first element is
        integer 5, indicating that it is a bigram-spinal feature. The second element
        is also an integer, the value to meaning mapping is listed above:
        
            (5,type,xi/xj_[word,pos,spine,word,pos,spine])

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
        xi_spine = self.spine_list[dep_index]
        xj_spine = self.spine_list[head_index]
        # Prepare keys
        type0_str = str((5,0,xi_word,xi_spine,xj_word))
        type1_str = str((5,1,xi_word,xi_spine,xj_word,xj_pos))
        type2_str = str((5,2,xi_word,xi_pos,xi_spine,xj_word))
        type3_str = str((5,3,xi_word,xi_pos,xi_spine,xj_word,xj_pos))
        type4_str = str((5,4,xi_word,xi_pos,xi_spine,xj_pos))
        type5_str = str((5,5,xi_pos,xi_spine,xj_pos))
        type6_str = str((5,6,xi_pos,xi_spine,xj_word,xj_pos))
        type7_str = str((5,7,xj_word,xj_spine,xi_word))
        type8_str = str((5,8,xj_word,xj_spine,xi_word,xi_pos))
        type9_str = str((5,9,xj_word,xj_pos,xj_spine,xi_word))
        type10_str = str((5,10,xj_word,xj_pos,xj_spine,xi_word,xi_pos))
        type11_str = str((5,11,xj_word,xj_pos,xj_spine,xi_pos))
        type12_str = str((5,12,xj_pos,xj_spine,xi_pos))
        type13_str = str((5,13,xj_pos,xj_spine,xi_word,xi_pos))

        # Set all bigram-spinal features to 1
        fv[type0_str] = 1
        fv[type1_str] = 1
        fv[type2_str] = 1
        fv[type3_str] = 1
        fv[type4_str] = 1
        fv[type5_str] = 1
        fv[type6_str] = 1
        fv[type7_str] = 1
        fv[type8_str] = 1
        fv[type9_str] = 1
        fv[type10_str] = 1
        fv[type11_str] = 1
        fv[type12_str] = 1
        fv[type13_str] = 1

        return

    def get_contextual_spinal_feature(self,fv,head_index,dep_index):
        """
        Add all contextual-spinal features into a given feature vector instance.
        +-------------------------------------------+
        | xi_word, xi_spine, xj_word                | type = 0
        | xi_word, xi_spine, xj_word, xj_pos        | type = 1
        | xi_word, xi_pos, xi_spine, xj_word        | type = 2
        | xi_word, xi_pos, xi_spine, xj_word,xj_pos | type = 3
        | xi_word, xi_pos, xi_spine, xj_pos         | type = 4
        | xi_pos, xi_spine, xj_pos                  | type = 5
        | xi_pos, xi_spine, xj_word, xj_pos         | type = 6
        | xj_word, xj_spine, xi_word                | type = 7
        | xj_word, xj_spine, xi_word, xi_pos        | type = 8
        | xj_word, xj_pos, xj_spine, xi_word        | type = 9
        | xj_word, xj_pos, xj_spine, xi_word, xi_pos| type = 10
        | xj_word, xj_pos, xj_spine, xi_pos         | type = 11
        | xj_pos, xj_spine, xi_pos))                | type = 12
        | xj_pos, xj_spine, xi_word, xi_pos         | type = 13
        +-------------------------------------------+
        Basic features are represented using a tuple. The first element is
        integer 6, indicating that it is a contextual-spinal feature. The second element
        is also an integer, the value to meaning mapping is listed above:
        
            (6,type,xi/xj_[word,pos,spine,word,pos,spine])

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
        xi_spine = self.spine_list[dep_index]
        xj_spine = self.spine_list[head_index]

        # Prepare keys
        type0_str = str((6,0,xi_word,xi_spine,xj_word))
        type1_str = str((6,1,xi_word,xi_spine,xj_word,xj_pos))
        type2_str = str((6,2,xi_word,xi_pos,xi_spine,xj_word))
        type3_str = str((6,3,xi_word,xi_pos,xi_spine,xj_word,xj_pos))
        type4_str = str((6,4,xi_word,xi_pos,xi_spine,xj_pos))
        type5_str = str((6,5,xi_pos,xi_spine,xj_pos))
        type6_str = str((6,6,xi_pos,xi_spine,xj_word,xj_pos))
        type7_str = str((6,7,xj_word,xj_spine,xi_word))
        type8_str = str((6,8,xj_word,xj_spine,xi_word,xi_pos))
        type9_str = str((6,9,xj_word,xj_pos,xj_spine,xi_word))
        type10_str = str((6,10,xj_word,xj_pos,xj_spine,xi_word,xi_pos))
        type11_str = str((6,11,xj_word,xj_pos,xj_spine,xi_pos))
        type12_str = str((6,12,xj_pos,xj_spine,xi_pos))
        type13_str = str((6,13,xj_pos,xj_spine,xi_word,xi_pos))

        # Set all contextual-spinal features to 1
        fv[type0_str] = 1
        fv[type1_str] = 1
        fv[type2_str] = 1
        fv[type3_str] = 1
        fv[type4_str] = 1
        fv[type5_str] = 1
        fv[type6_str] = 1
        fv[type7_str] = 1
        fv[type8_str] = 1
        fv[type9_str] = 1
        fv[type10_str] = 1
        fv[type11_str] = 1
        fv[type12_str] = 1
        fv[type13_str] = 1

        return

    def get_spinal_adjoin_feature(self,fv,head_index,dep_index):  
        """
        Add all spine-adjoin features (GRM) into a given feature vector instance.
        asic features are represented using a tuple. The first element is
        nteger 7, indicating that it is a spinal_adjoin feature. The second element
        is also an integer, the value to meaning mapping is listed above:
        
            (7,type,xi/xj_[word,pos,spine,word,pos,spine])

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
        xi_spine = self.spine_list[dep_index]
        xj_spine = self.spine_list[head_index]
        xj_label = self.label_list[dep_index]
        
        # Map the label to GRM
        print(xi_word, xi_spine)
        print(xj_word, xj_spine, xj_label)
        xi_xj_grm = self.get_grm(xj_spine, xj_label, xi_spine, xi_pos)
        print(xi_xj_grm)

        # Prepare keys
        # note: xj_label[1]=0 means s, =1 means r
        type0_str = str((7,0,xi_word,xj_word,(xi_xj_grm,xj_label[1])))
        type1_str = str((7,1,xi_word,xj_word,xj_pos,(xi_xj_grm,xj_label[1])))
        type2_str = str((7,2,xi_word,xj_word,xi_pos,(xi_xj_grm,xj_label[1])))
        type3_str = str((7,3,xi_word,xj_word,xi_pos,xj_pos,(xi_xj_grm,xj_label[1])))
        type4_str = str((7,4,xi_word,xi_pos,xj_pos,(xi_xj_grm,xj_label[1])))
        type5_str = str((7,5,xi_pos,xj_word,xj_pos,(xi_xj_grm,xj_label[1])))
        type6_str = str((7,6,xi_pos,xj_pos,(xi_xj_grm,xj_label[1])))

        # Set all unigram-spinal features to 1; same feature count will
        # be aggregated 
        fv[type0_str] = 1
        fv[type1_str] = 1
        fv[type2_str] = 1
        fv[type3_str] = 1
        fv[type4_str] = 1
        fv[type5_str] = 1
        fv[type6_str] = 1
        return

    def add_dir_and_dist(self,fv,head_index,dep_index):
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

    def get_local_vector(self,head_index,dep_index,is_uni_spinal=False,is_bi_spinal=False,is_conx_spinal=False,is_spinal_adjoin=True):
        """
        Given an edge, return its local vector

        :param head_index: The index of the head node
        :type head_index: integer
        :param dep_index: The index of the dependency node
        :type dep_node: integer
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

        if is_uni_spinal:
            # Get Unigram-spinal features
            self.get_unigram_spinal_feature(local_fv,head_index,dep_index)

        if is_bi_spinal:
            # Get bigram-spinal features
            self.get_bigram_spinal_feature(local_fv,head_index,dep_index)

        if is_conx_spinal:
            # Get contextual-spinal features
            self.get_contextual_spinal_feature(local_fv,head_index,dep_index)

        # not sure what grm is used for here
        # delete grm because it causes error   
        if is_spinal_adjoin:
            self.get_spinal_adjoin_feature(local_fv,head_index,dep_index)

        # For future improvements please put all other features here
        # ...

        # Add dir and dist information for all features. This can be done
        # uniformly since the edge is the same.
        self.add_dir_and_dist(local_fv,head_index,dep_index)
        
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
    
    # TODO: bugs, refers to conll paper
    def get_grm(self, spine_m, label, spine_h, pos):
        position = label[0]
        r_or_s = label[1]
        # is_prev not used here
        is_prev = label[2]
        
        m_node = spine_m.split("(")[1]
        h_node = spine_h.split("(")[int(position)]

        # If it is a regular adjoin
        if r_or_s:
            return (h_node, h_node, m_node)
        # If it is a sibling adjoin
        else:
            return (h_node, pos, m_node)


