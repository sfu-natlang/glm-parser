from data.dependency_tree import *
from backend.data_backend import *
from feature.feature_vector import *
from feature.feature_description import simple_cfg, FeatureDescription
from feature.regular_expression import IndexedStr
from feature.ll_parser import LLParser

class FeatureSet():
    """
    Stores and updates weight vector used in dependency parsing according to
    various features
    """
    def __init__(self,dep_tree,database_filename=None,
                 operating_mode="memory_dict"):
        """
        Initialize the FeatureSet instance, including a file name that might
        be used to store the database on the disk, and a dependency tree
        that provides only word list and pos list (i.e. no edge information)
        to the instance. The dependency tree should not be further modified
        after refistered into the instance, in order to maintain consistency.

        :param dep_tree: The dependency tree that you want to train on
        :type dep_tree: DependencyTree
        :param database_filename: The file name of the database file. If this
        is not provided then a file name is reqiured when you call dump()
        :type database_filename: str
        :param operating_mode: The mode of operation on the database
        :type operating_mode: str
        """
        # A list of FeatureDescription instances
        self.extra_feature_dict = {}
        self.operating_mode = operating_mode
        # If this is None, then we will use the parameter provided in dump()
        self.database_filename = database_filename
        # If you want a disk database with write through, use
        # self.db = DataBackend("shelve_write_through")
        # If you want a disk data base with write back, use
        # self.db = DataBackend("shelve_write_back")
        # If you want a memory database, use
        self.db = DataBackend(operating_mode)
        # We do this during initialization. For later stages if you need to
        # change the tree then just call that method manually
        self.switch_tree(dep_tree)
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
        

    def switch_tree(self,dep_tree):
        """
        After finishing traning on one tree, switch to another new dependency
        tree. This will force the instance ti refresh its word_list and pos_list
        cache.

        :param dep_tree: A dependency tree represenattion tree
        :type dep_tree: DependencyTree 
        """
        # Hook the dependency tree into the instance, so that we need not
        # to provide a parameter about the tree each time
        self.dep_tree = dep_tree
        # We cache these two into the instance to make it faster and prevent
        # fetching them from the dep_tree each time
        # Also do not forget that each time we switch to a new dependency tree
        # we should refresh self.word_list and self.pos_list cache to make
        # it up-to-date.
        self.word_list = dep_tree.get_word_list_ref()
        self.pos_list = dep_tree.get_pos_list_ref()
        # Add five gram word list
        self.compute_five_gram()
        
        return

    def dump(self,filename=None):
        """
        Save the content of the database to a disk file. The file name is given
        in the parameter. For persistent data objects, it will call the sync()
        method. But for memory dict it will call pickle procedure to implement
        the dump operation.

        :param filename: The name of the saved dump file. This will override
        the file name provided in the constructor
        :type filename: str
        """
        if filename == None:
            if self.database_filename == None:
                raise ValueError("""You must provide a file name or use the
                                    default file name.""")
            # If None is passed then use the default file name provided to
            # the constructor
            else:
                filename = self.database_filename
        # This should work for both mem dict and persistent data object
        self.db.dump(filename)
        return

    def load(self,filename=None):
        """
        Load the content of a database from the disk file. For shelve types this
        could be saved, since shelve always works on disk file. However if you
        are using memory dictionary, each time you want to continue your job,
        you need to load the previous dumped one.
        """
        if filename == None:
            if self.database_filename == None:
                raise ValueError("""You must provide a file name or use the
                                    default file name.""")
            else:
                filename = self.database_filename
        self.db.load(filename)
        return
    
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

    def get_local_vector(self,head_index,dep_index):
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

    def get_edge_score(self,head_index,dep_index):
        """
        Given an edge, return its score. The score of an edge is the aggregation
        of its local vector components weighted by the parameters.

        :param head_index: The index of the head node
        :type head_index: integer
        :param dep_index: The index of the dependency node
        :type dep_node: integer
        """
        local_fv = self.get_local_vector(head_index,dep_index)
        score = 0
        # Iterate through each feature that appears with the edge
        for i in local_fv.keys():
            # If there is a parameter record (i.e. not 0) we just use that
            if self.db.has_key(i):
                score += self.db[i]
            else:
                pass
                # If not then we do not add (since it is 0)
                # But we will add the entry into the database
                #self.db[i] = 0
                #####################
                # This will cause us lots of trouble, including making
                # the size of the database bloat to an unacceptable size
                # and introducing a large error in the estimation of the
                # feature number.
                
        return score

    def update_weight_vector(self,fv_delta):
        """
        Update the patameter of features in the database. fv_delta is the delta
        feature vector, which in most cases is the result of applying
        eliminate() on the correct global vector with the global vector

        :param fv_delta: Delta vector
        :type delta: FeatureVector
        """
        for i in fv_delta.keys():
            if self.db.has_key(i):
                self.db[i] = self.db[i] + fv_delta[i]
            else:
                # If it does not exist, then it is considered to be 0
                # So 0 + fv_delta[i] is merely fv_delta[i]
                self.db[i] = fv_delta[i]
        return

    def close(self):
        """
        Close the database. This must be done before program exits, or there is
        probablity that the changes will not be written back. However if you
        have already called dump() to save the content then it is up to you
        whether to close the database. Still, it is good practice to do so
        """
        self.db.close()
        return

    def __getitem__(self,key_str):
        """
        A wrap to the __getitem__ method of the data backend
        """
        return self.db[key_str]

    def __setitem__(self,key_str,value):
        """
        A wrap to the __setitem__ method of the data backend
        """
        self.db[key_str] = value
        return

    def keys(self):
        """
        Return a list of items that is the keys of the underlying dictionary.

        This is only a simple wrap of the underlying database, which may be
        another level of wrapping of the built-in data structure method. However
        you can ignore the difference.

        :return: A list of feature keys
        :rtype: list(str)
        """
        return self.db.keys()

    def has_key(self,key_str):
        """
        Check whether the given key is in the database. A key in this case is a
        string.

        :param key_str: The key string
        :type key_str: str
        :return: True if the key is in the database, False if not
        :rtype: bool
        """
        return self.db.has_key(key_str)

    def pop(self,key):
        self.db.pop(key)
        return

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

    def get_feature_count(self,count_zero=False):
        """
        Return the number of features. Please notice that this is not the number
        of keys in the dictionary, since we may create many unused 0 count
        features in the feature set, so we need to count the feature with
        non-zero count.

        :return: The number of features whose count is not 0
        :rtype: int
        """
        if count_zero == True:
            return len(self.keys())

        count = 0
        
        for i in self.keys():
            if self.db[i] != 0:
                count += 1
        return count

    def add_feature_description(self,name,program):
        """
        Add a new program to generate new features

        :param name: A string name for the feature program
        :type name: str
        :param program: A program to generate the feature
        :type program: IndexedStr
        """
        fd = FeatureDescription(self.dep_tree,simple_cfg,program)
        self.extra_feature_dict[name] = fd
        return

    def get_feature_by_name(self,name,head_index,dep_index):
        """
        Get a feature from self defined feature descriptions
        """
        return self.extra_feature_dict[name].get_feature(head_index,dep_index)

    def parse_description(self,s):
        """
        Parse a string of a feature description

        :param s: A indexed string contains the feature description
        :type s: IndexedStr
        """
        global local_var
        local_var.clear()
        local_var['word_list'] = ('string[]',self.dep_tree.word_list)
        local_var['pos_list'] = ('string[]',self.dep_tree.pos_list)
        local_var['length'] = ('int',len(self.dep_tree.word_list))
        lp = LLParser()
        lp.parse_cfg(simple_cfg)
        t = lp.symbol_table['stmts'].parse(s)
        lp.print_tree(t)
        eva_stmts(t)
        return
    

###############################################################################
#                             The Devil Split Line                            #
###############################################################################

class OldFeatureSet():
    """
    Stores and updates weight vector used in dependency parsing according to
    various features
    """
    def __init__(self,database_filename,dep_tree):
        self.database_filename = database_filename
        # Open the database file
        # self.db = shelve.open(database_filename,writeback=False)
        self.db = DataBackend("shelve_write_through")
        # Store the feature key vector in the instance
        feature_list = self.get_feature_key_list(dep_tree)
        self.feature_key_list = feature_list[0]
        self.feature_str_list = feature_list[1]
        # Callback functions
        self.satisfaction_func = [self.is_satisfied_unigram,
                                  self.is_satisfied_bigram,
                                   ]
        # Save this for later use
        self.dep_tree = dep_tree
        return

    def add_feature_key(self,feature_list,feature_key):
        """
        Add the feature key into feature list. If a key already exists then
        do nothing and return. This is just a shorthand of
            if not feature_key in feature_list:
                feature_list.append(feature_key)
        :param feature_list: A list that holds the feature keys
        :type feature_list: list
        
        :return: True if there are something added to the list, False if not
        :rtype: bool
        """
        if not feature_key in feature_list:
            feature_list.append(feature_key)
            return True
        else:
            return False

    def get_unigram_feature_key_list(self,dep_tree):
        """
        Return a list of features keys, which are basic uni-gram features.
            xi-word, xi-pos
            xi-word
            xi-pos
            xj-word, xj-pos
            xj-word
            xj-pos
        Basic features are represented using a five-tuple:
            (0,xi-word,xi-pos,xj-word,xj-pos)
            
        The starting 0 is used as a type identifier for basic features
        (including both uni-gram and bi-gram).

        If any entry is not used in the feature tuple it is set to empty string

        :param dep_tree: A DependencyTree instance
        :type dep_tree: DependencyTree
        """
        word_list = dep_tree.get_word_list_ref()
        pos_list = dep_tree.get_pos_list_ref()
        # Check whether the dependency tree satisfies the most fundamental
        # requirements of a dependency tree. Especially we are concerning
        # whether the length of pos_list and word_list are the same
        dep_tree.check_valid()
        
        feature_list = []
        # All possible combinations to the possible tags listed above
        for i in range(len(word_list)):
            self.add_feature_key(feature_list,(0,word_list[i],pos_list[i],
                                               None,None))
            self.add_feature_key(feature_list,(0,word_list[i],None,
                                               None,None))
            self.add_feature_key(feature_list,(0,None,pos_list[i],
                                               None,None))

            self.add_feature_key(feature_list,(0,None,None,
                                               word_list[i],pos_list[i]))
            self.add_feature_key(feature_list,(0,None,None,
                                               word_list[i],None))
            self.add_feature_key(feature_list,(0,None,None,
                                               None,pos_list[i]))

        return feature_list

    def get_bigram_feature_key_list(self,dep_tree):
        """
        Return a list of bi-gram basic features, including
            xi-word, xi-pos, xj-word, xj-pos
            xj-pos, xj-word, xj-pos
            xi-word, xj-word, xj-pos
            xi-word, xi-pos, xj-pos
            xi-word, xi-pos, xj-word
            xi-word, xj-word
            xi-pos, xj-pos
            
        :param dep_tree: A DependencyTree instance
        :type dep_tree: DependencyTree        
        """
        word_list = dep_tree.get_word_list_ref()
        pos_list = dep_tree.get_pos_list_ref()

        dep_tree.check_valid()
        feature_list = []

        # Iterate through the head word i and the dependent word j
        for i in range(0,len(word_list)):
            # j starts at 1 since ROOT node cannot be a dependent node
            for j in range(1,len(pos_list)):
                # Cannot depend on itself
                if i == j:
                    continue
                # Now we assume an edge (i,j). It is guaranteed that all pairs
                # will be enumerated in the nested loop
                self.add_feature_key(feature_list,(1,word_list[i],pos_list[i],
                                                   word_list[j],pos_list[j]))
                self.add_feature_key(feature_list,(1,None,pos_list[i],
                                                   word_list[j],pos_list[j]))
                self.add_feature_key(feature_list,(1,word_list[i],None,
                                                   word_list[j],pos_list[j]))
                self.add_feature_key(feature_list,(1,word_list[i],pos_list[i],
                                                   None,pos_list[j]))
                self.add_feature_key(feature_list,(1,word_list[i],pos_list[i],
                                                   word_list[j],None))
                self.add_feature_key(feature_list,(1,word_list[i],None,
                                                   word_list[j],None))
                self.add_feature_key(feature_list,(1,None,pos_list[i],
                                                   None,pos_list[j]))
        return feature_list

    def get_feature_key_list(self,dep_tree):
        feature_key_list = []
        # We are using unigram and bigram features. This is going to be
        # updated in the future
        feature_key_list += self.get_unigram_feature_key_list(dep_tree)
        feature_key_list += self.get_bigram_feature_key_list(dep_tree)

        # Convert these keys to strings. The database can only use string as
        # the index
        feature_str_list = []
        for i in range(0,len(feature_key_list)):
            feature_str_list.append(str(feature_key_list[i]))
        
        return (feature_key_list,feature_str_list)

    def is_satisfied_unigram(self,feature_key,dep_tree,edge_tuple,check=False):
        """
        Calculate whether an edge satisfies the unigram features
        i.e. feature_key[0] == 0
        """
        if check == True and feature_key[0] != 0:
            raise ValueError("Not a unigram feature: %s" % (str(feature_key)))
        word_list = dep_tree.get_word_list_ref()
        pos_list = dep_tree.get_pos_list_ref()

        head_word = word_list[edge_tuple[0]]
        if feature_key[1] != None and feature_key[1] != head_word:
            return False
        head_pos = pos_list[edge_tuple[0]]
        if feature_key[2] != None and feature_key[2] != head_pos:
            return False
        dep_word = word_list[edge_tuple[1]]
        if feature_key[3] != None and feature_key[3] != dep_word:
            return False
        dep_pos = pos_list[edge_tuple[1]]
        if feature_key[4] != None and feature_key[4] != dep_pos:
            return False
        return True

    def is_satisfied_bigram(self,feature_key,dep_tree,edge_tuple,check=False):
        """
        Calculate whether an edge satisfies the unigram features
        i.e. feature_key[0] == 1
        """
        if check == True and feature_key[0] != 1:
            raise ValueError("Not a bigram feature: %s" % (str(feature_key)))
        # Explicitly set check = False to inhibit type checking
        # Or we will get a ValueError
        ret_val = self.is_satisfied_unigram(feature_key,dep_tree,
                                            edge_tuple,False)
        return ret_val

    def is_satisfied(self,feature_key,dep_tree,edge_tuple):
        """
        Calculate whether an edge satisfies a key feature. There are several
        types of key features, so we need to treat them separately.

        :param feature_key: A feature key in feature_key_list
        :type feature_key: tuple
        :param dep_tree: A DependencyTree instance
        :type dep_tree: DependencyTree
        :param edge_tuple: A pair of integers to indicate an edge
        :type edge_tuple: tuple(integer,integer)

        :return: True if the edge satisfies the feature key. False if not
        :rtype: bool
        """
        # Retrieve the callback
        func_index = feature_key[0]
        # Call the function
        ret_val = self.satisfaction_func[func_index](feature_key,
                                                     dep_tree,edge_tuple)
        return ret_val

    def get_local_scalar(self,dep_tree,edge_tuple):
        """
        Return the score of an edge given its edge elements and the context
        """
        param_list = self.get_local_vector(dep_tree,edge_tuple)
        ret_val = 0
        for i in param_list:
            ret_val += i
        return ret_val

    def get_edge_score(self,edge_tuple):
        """
        Almost identical to get_local_scalar, except that it does not need
        a DependencyTree instance. This is usually used to score an edge
        during parsing, where the overall structure is not known yet, and
        we only have to score edges
        """
        local_vector = self.get_local_vector(self.dep_tree,edge_tuple)
        param_list = self.get_param_list(self.dep_tree,edge_tuple)
        if len(local_vector) != len(param_list):
            raise ValueError("Local vector and parameter list do not accord")
        edge_score = 0
        for i in range(0,len(local_vector)):
            if local_vector[i] == 1:
                edge_score += param_list[i]
        return edge_score

    def get_param_list(self,dep_tree,edge_tuple):
        """
        Return the parameter list of current feature key list
        """
        feature_list_length = len(self.feature_str_list)
        param_list = [0] * feature_list_length
        # Find all parameter, i is a feature key, i[0] is the feature type
        # feature_str_list is the string key for using in the database
        # feature_key_list is the tuple for using by the program code
        for i in range(0,feature_list_length):
            # If the value already in the data base
            if self.db.has_key(self.feature_str_list[i]):
                # Check whether it satisfies the feature key
                if self.is_satisfied(self.feature_key_list[i],
                                     dep_tree,edge_tuple):
                    param_list[i] = self.db[self.feature_str_list[i]]
            else:
                # Create new key-value pair, if it does not exist
                self.db[self.feature_str_list[i]] = 0
                
        return param_list

    def get_local_vector(self,dep_tree,edge_tuple):
        local_vector = []
        for i in range(0,len(self.feature_str_list)):
            if self.is_satisfied(self.feature_key_list[i],dep_tree,edge_tuple):
                local_vector.append(1)
            else:
                local_vector.append(0)
        return local_vector

    def update_weight_vector(self,delta_list):
        """
        Update the weight vector, given a list of deltas that will be added
        up to the current weight vector
        """
        # We do not need to check whether the feature exists or not, since we
        # have initialized the database earlier
        for i in range(0,len(self.feature_key_list)):
            temp = self.db[self.feature_str_list[i]]
            temp += delta_list[i]
            self.db[self.feature_str_list[i]] = temp
        return

    def close(self):
        """
        Routine that must be called before exit
        """
        # Write back all pages into database
        self.db.close()
        return

#############################################################################
# If you see this line and you are modiyfing the code exactly above, then you
# are accessing the wrong part of the code.
#############################################################################

if __name__ == "__main__":
    dt = DependencyTree()
    dt.word_list = "John smashed the ball with the bat".split()
    dt.pos_list = "N V D N P D N".split()
    #fs = FeatureSet(dt,"test_load.db",operating_mode='memory_dict')
    #fs.load('sec_14_14_iter_0.db')
    #print "fs load successfully"
    #fs2 = FeatureSet(dt,"test_load.db",operating_mode='memory_dict')
    #fs2.load('sec_15_15_iter_0.db')
    #print "fs2 load successfully"
    #fs2.merge(fs)
    #fs2.dump('test_merge.db')
    s = IndexedStr("""
                    string result[5];
                    result[0] = word_list[head_index];
                    result[1] = pos_list[head_index];
                    result[2] = word_list[dep_index];
                    result[3] = pos_list[dep_index];
                    if(dep_index == (length - 1))
                    {
                        result[4] = "end_node";
                    }
                    else
                    {
                        result[4] = "not_end";
                    };
                   """)
    fs = FeatureSet(dt)
    print len(fs.get_local_vector(1,4).keys())
    fs.print_local_vector(1,4)
    #fs2.add_feature_description('my_feature',s)
    #print fs2.get_feature_by_name('my_feature',1,2)
    
