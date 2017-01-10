import feature_vector
import feature_generator_base
import debug.debug
from data.file_io import fileRead, fileWrite
from ner_PER_list import ner_per_list
from ner_LOC_list import ner_loc_list

import string
import copy

__version__ = '1.1'


per_list = ner_per_list
loc_list = ner_loc_list


class FeatureGenerator(feature_generator_base.FeatureGeneratorBase):
    """
    This is the feature generator for the NER Tagger
    """
    name = "NERTaggerFeatureGenerator"

    def __init__(self):
        feature_generator_base.FeatureGeneratorBase.__init__(self)
        self.care_list.append("FORM")
        self.care_list.append("POSTAG")
        self.care_list.append("CHUNK")
        self.care_list.append("NER")
        return

    def load_to_sentence(self, sentence):
        if sentence.fgen is not None:
            sentence.fgen.unload_from_sentence(sentence)

        sentence.column_list["FORM"].insert(0, '_B_-1')
        sentence.column_list["FORM"].insert(0, '_B_-2')  # first two 'words' are B_-2 B_-1
        sentence.column_list["FORM"].append('_B_+1')
        sentence.column_list["FORM"].append('_B_+2')     # last two 'words' are B_+1 B_+2

        sentence.column_list["POSTAG"].insert(0, 'B_-1')
        sentence.column_list["POSTAG"].insert(0, 'B_-2')
        sentence.column_list["POSTAG"].append('B_+1')
        sentence.column_list["POSTAG"].append('B_+2')

        sentence.column_list["CHUNK"].insert(0, 'B_-1')
        sentence.column_list["CHUNK"].insert(0, 'B_-2')
        sentence.column_list["CHUNK"].append('B_+1')
        sentence.column_list["CHUNK"].append('B_+2')

        sentence.column_list["NER"].insert(0, 'B_-1')
        sentence.column_list["NER"].insert(0, 'B_-2')

        gold_global_vector = self.get_feature_vector(sentence)

        sentence.gold_global_vector = gold_global_vector
        sentence.fgen = self
        return

    def unload_from_sentence(self, sentence):
        if sentence.fgen is None:
            return
        if sentence.fgen.name != "NERTaggerFeatureGenerator":
            sentence.fgen.unload_from_sentence(sentence)
            return

        del sentence.column_list["FORM"][0]
        del sentence.column_list["FORM"][0]
        del sentence.column_list["FORM"][len(sentence.column_list["FORM"]) - 1]
        del sentence.column_list["FORM"][len(sentence.column_list["FORM"]) - 1]

        del sentence.column_list["POSTAG"][0]
        del sentence.column_list["POSTAG"][0]
        del sentence.column_list["POSTAG"][len(sentence.column_list["POSTAG"]) - 1]
        del sentence.column_list["POSTAG"][len(sentence.column_list["POSTAG"]) - 1]

        del sentence.column_list["CHUNK"][0]
        del sentence.column_list["CHUNK"][0]
        del sentence.column_list["CHUNK"][len(sentence.column_list["CHUNK"]) - 1]
        del sentence.column_list["CHUNK"][len(sentence.column_list["CHUNK"]) - 1]

        del sentence.column_list["NER"][0]
        del sentence.column_list["NER"][0]

        sentence.fgen = None
        return

    def update_sentence_with_output(self, sentence, output):
        if sentence.fgen != self:
            raise RuntimeError("FGEN [ERROR]: update_sentence_with_output " +
                "can only update sentence  with this fgen as feature generator")
        sentence.column_list["NER"] = copy.deepcopy(output)
        return

    # function to check if the word contains a digit / dollar /exclamatory /hyphen
    def contains_digits(self, s):
        return any(char.isdigit() for char in s)

    def contains_dollar(self, s):
        return any(char == "$" for char in s)

    def contains_exclamatory(self, s):
        return any(char == "!" for char in s)

    def contains_hyphen(self, s):
        return any(char == "-" for char in s)

    # function to check if word contains upper case characters
    def contains_upper(self, s):
        return any(char.isupper() for char in s)

    # function to check if word contains any punctuations
    def contains_punc(self, s):
        return any(char in string.punctuation for char in s)

    # fucntion to check if word starts with capital letter
    def starts_capital(self, s):
        if s[0].isupper():
            return 1
        else:
            return 0

    # function to check if word ends with a period
    def ends_with_period(self, s):
        if s[:-1] == '.':
            return 1
        else:
            return 0

    # function to check is the word is in Upper case
    def all_upper(self, s):
        for k in s:
            if not k.isupper():
                return 0
        return 1

    # function tp check if the word has an internal period/apostrophe/amphasand
    def contains_internal_period(self, s):
        return any(char == '.' for char in s)

    def has_internal_apostrophe(self, s):
        return any(char == "'" for char in s)

    def contains_hyphen(self, s):
        return any(char == "-" for char in s)

    def contains_amphasand(self, s):
        return any(char == "&" for char in s)

    # function to check if word contains both upper and lower characters
    def contains_upper_lower(self, s):
        return (any(char.isupper() for char in s) and any(char.islower() for char in s))

    # function to check if the word is alphanumeric
    def contains_alphanumeric(self, s):
        return any(char.isalnum() for char in s)

    # this function checks is all word contains only digits
    def contains_all_num(self, s):
        for x in s:
            if not x.isdigit():
                return 0
        return 1

    def contains_digits(self, s):
        return any(char.isdigit() for char in s)

    # checking if the word is of the formn .X where x is any alphabet
    def containsPInitial(self, s):
        if len(s) == 2:
            if s[0] == '.' and s[1].isalpha():
                return 1
        return 0

    def contains_hyphen(self, s):
        return any(char == "-" for char in s)

    def contains_all_upper(self, s):
        x = [char for char in s if s.isdigit()]
        return len(x)

    def contains_upper(self, s):
        return any(char.isupper() for char in s)

# function to replace all digits in a word with 'D'

    def lexical_f(self, s):
        for i in s:
            if i.isdigit():
                s = s.replace(i, "D")
        return s

    def list_PER_isPresent(self, s):
        y = '\'s'
        if s != y:
            if s in per_list:
                return 1
        return 0

    # function to generate ortho features

    def ortho_feature_alphanumeric(self, s):
        for i in s:
            if i.isdigit():
                s = s.replace(i, "D")
            elif i.isalpha():
                s = s.replace(i, "A")
        return s

    # function to check is all charcters are in lower case
    def all_lower(self, s):
        for i in s:
            if not i.islower():
                return 0
        return 1

    def possesive_feature(self, s):
        y = '\'s'
        if s == y:
            # print y
            return 1
        return 0

    # function to perform binary search in a gazatteer
    def binarySearch(self, item, alist):
        first = 0
        last = len(alist)-1
        found = False

        while first <= last and not found:
            midpoint = (first + last)//2
            if alist[midpoint] == item:
                found = True
            else:
                if item < alist[midpoint]:
                    last = midpoint-1
                else:
                    first = midpoint+1

        return found

    def loading_list(self, list_file):
        c = open(list_file, 'r')
        alist = []
        for line in c:
                x = line.split()
                alist.append(x[1])
        c.close()
        return alist

    # Function to get the ner feature of a word
    def current_tag_feature(self,
                            sentence,
                            index,
                            prev_tag,
                            prev_backpointer):

        wordlist = sentence.column_list["FORM"]
        ner_list = sentence.column_list["NER"]
        pos_list = sentence.column_list["POSTAG"]
        chunk_list = sentence.column_list["CHUNK"]

        fv = []
        word = wordlist[index].lower()
        i = index
        if self.all_upper(word):
            fv.append((1, 'cur_upper'))
        if self.all_upper(wordlist[i-1]):
            fv.append((2, 'prev_upper'))
        if self.all_upper(wordlist[i-2]):
            fv.append((3, 'prev_prev_upper'))
        if self.all_upper(wordlist[i+1]):
            fv.append((4, 'after_upper'))
        if self.all_upper(wordlist[i+2]):
            fv.append((5, 'after_after_upper'))
        fv.append((6, 'previous_2_tag', prev_tag, prev_backpointer))
        fv.append((7, 'previous+cur', prev_tag, prev_backpointer, word))
        fv.append((8, 'cur', word))
        fv.append((9, 'prev', wordlist[i-1]))
        fv.append((10, 'prev_prev', wordlist[i-2]))
        fv.append((11, 'after', wordlist[i+1]))
        fv.append((12, 'after_after', wordlist[i+2]))
        fv.append((13, wordlist[i-2], wordlist[i-1], word, wordlist[i+1], wordlist[i+2]))
        if self.starts_capital(word):
            fv.append((14, 'cur_cap'))
        if self.starts_capital(wordlist[i-1]):
            fv.append((15, 'prev_cap'))
        if self.starts_capital(wordlist[i-2]):
            fv.append((16, 'prev_prev_cap'))
        if self.starts_capital(wordlist[i+1]):
            fv.append((17, 'after_cap'))
        if self.starts_capital(wordlist[i+2]):
            fv.append((18, 'after_after_cap'))

        fv.append((19, word[:1]))
        fv.append((20, word[-1:]))
        fv.append((21, word[:2]))
        fv.append((22, word[-2:]))
        fv.append((23, word[:3]))
        fv.append((24, word[-3:]))
        fv.append((25, word[:4]))
        fv.append((26, word[-4:]))
        fv.append((29, len(word)))
        fv.append((30, i))
        if self.possesive_feature(word):
            fv.append((36, prev_tag))
            fv.append((37, pos_list[i-1]))

        fv.append((27, pos_list[i]))
        fv.append((28, chunk_list[i]))

        if self.contains_all_num(word):
            fv.append((29, 'all_digits'))
        if self.contains_digits(word):
            if self.contains_hyphen(word):
                fv.append((30, 'digits_punc'))
            elif self.contains_internal_period(word):
                fv.append((31, 'digits_punc'))
            elif self.has_internal_apostrophe(word):
                fv.append((32, 'digits_punc'))
            elif self.contains_internal_period(word):
                fv.append((33, 'digits_punc'))
            elif self.contains_amphasand(word):
                fv.append((34, 'digits_punc'))
        if self.contains_alphanumeric(word) and self.contains_hyphen(word):
            fv.append((35, 'alphanum_hyphen'))
        if self.binarySearch(word, per_list):
            fv.append((38, 'PER_list'))
        if self.binarySearch(word, loc_list):
            fv.append((39, 'LOC_list'))
        fv.append((40, wordlist[i-1], word))
        fv.append((41, word, wordlist[i+1]))
        if self.all_lower(word):
            fv.append((42, 'islower'))
        if self.contains_hyphen(word):
            fv.append((43, 'hyphen'))

        return fv

    # Function to get sentence feature
    def get_feature_vector(self, sentence, output=None):
        wordlist = sentence.column_list["FORM"]
        pos_list = sentence.column_list["POSTAG"]
        chunk_list = sentence.column_list["CHUNK"]

        if output is None:
            ner_list = sentence.column_list["NER"]
        else:
            ner_list = output

        fv = []
        for i in range(3, len(wordlist) - 2):
            word = wordlist[i]
            tag = ner_list[i]
            if self.all_upper(word):
                fv.append(str((1, 'cur_upper', tag)))
            if self.all_upper(wordlist[i-1]):
                fv.append(str((2, 'prev_upper', tag)))
            if self.all_upper(wordlist[i-2]):
                fv.append(str((3, 'prev_prev_upper', tag)))
            if self.all_upper(wordlist[i+1]):
                fv.append(str((4, 'after_upper', tag)))
            if self.all_upper(wordlist[i+2]):
                fv.append(str((5, 'after_after_upper', tag)))
            fv.append(str((6, 'previous_2_tag', ner_list[i-1], ner_list[i-2], tag)))
            fv.append(str((7, 'previous+cur', ner_list[i-1], ner_list[i-2], word, tag)))
            fv.append(str((8, 'cur', word, tag)))
            fv.append(str((9, 'prev', wordlist[i-1], tag)))
            fv.append(str((10, 'prev_prev', wordlist[i-2], tag)))
            fv.append(str((11, 'after', wordlist[i+1], tag)))
            fv.append(str((12, 'after_after', wordlist[i+2], tag)))
            fv.append(str((13, wordlist[i-2], wordlist[i-1], word, wordlist[i+1], wordlist[i+2], tag)))
            if self.starts_capital(word):
                fv.append(str((14, 'cur_cap', tag)))
            if self.starts_capital(wordlist[i-1]):
                fv.append(str((15, 'prev_cap', tag)))
            if self.starts_capital(wordlist[i-2]):
                fv.append(str((16, 'prev_prev_cap', tag)))
            if self.starts_capital(wordlist[i+1]):
                fv.append(str((17, 'after_cap', tag)))
            if self.starts_capital(wordlist[i+2]):
                fv.append(str((18, 'after_after_cap', tag)))

            fv.append(str((19, word[:1], tag)))
            fv.append(str((20, word[-1:], tag)))
            fv.append(str((21, word[:2], tag)))
            fv.append(str((22, word[-2:], tag)))
            fv.append(str((23, word[:3], tag)))
            fv.append(str((24, word[-3:], tag)))
            fv.append(str((25, word[:4], tag)))
            fv.append(str((26, word[-4:], tag)))
            fv.append(str((29, len(word), tag)))
            fv.append(str((30, i, tag)))
            if self.possesive_feature(word):
                fv.append(str((36, ner_list[i-1], tag)))
                fv.append(str((37, pos_list[i-1], tag)))

            fv.append(str((27, pos_list[i], tag)))
            fv.append(str((28, chunk_list[i], tag)))

            if self.contains_all_num(word):
                fv.append(str((29, 'all_digits', tag)))
            if self.contains_digits(word):
                if self.contains_hyphen(word):
                    fv.append(str((30, 'digits_punc', tag)))
                elif self.contains_internal_period(word):
                    fv.append(str((31, 'digits_punc', tag)))
                elif self.has_internal_apostrophe(word):
                    fv.append(str((32, 'digits_punc', tag)))
                elif self.contains_internal_period(word):
                    fv.append(str((33, 'digits_punc', tag)))
                elif self.contains_amphasand(word):
                    fv.append(str((34, 'digits_punc', tag)))
            if self.contains_alphanumeric(word) and self.contains_hyphen(word):
                fv.append(str((35, 'alphanum_hyphen', tag)))
            if self.binarySearch(word, per_list):
                fv.append(str((38, 'PER_list', tag)))
            if self.binarySearch(word, loc_list):
                fv.append(str((39, 'LOC_list', tag)))
            fv.append(str((40, wordlist[i-1], word, tag)))
            fv.append(str((41, word, wordlist[i+1], tag)))
            if self.all_lower(word):
                fv.append(str((42, 'islower', tag)))
            if self.contains_hyphen(word):
                fv.append(str((43, 'hyphen', tag)))
        return fv
