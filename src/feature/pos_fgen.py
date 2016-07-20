import feature_vector
import feature_generator_base
import debug.debug

import string
import copy
from collections import defaultdict


class FeatureGenerator(feature_generator_base.FeatureGeneratorBase):
    """
    This is the feature generator for the Part Of Speech Tagger
    """
    name = "POSTaggerFeatureGenerator"

    def __init__(self):
        feature_generator_base.FeatureGeneratorBase.__init__(self)
        self.care_list.append("FORM")
        self.care_list.append("POSTAG")
        return

    def __contains_digits(self, s):
        return any(char.isdigit() for char in s)

    def __contains_hyphen(self, s):
        return any(char == "-" for char in s)

    def __contains_upper(self, s):
        return any(char.isupper() for char in s)

    def __contains_punc(self, s):
        return any(char in string.punctuation for char in s)

    def get_local_vector(self, wordlist, index, prev_tag, prev_backpointer):
        fv = defaultdict(int)
        word = wordlist[index].lower()
        fv.append((0, word))
        fv.append((1, wordlist[index - 1].lower()))
        fv.append((2, wordlist[index - 2].lower()))
        fv.append((3, wordlist[index + 1].lower()))
        fv.append((4, wordlist[index + 2].lower()))
        fv.append((5, word[:1]))
        fv.append((6, word[-1:]))
        fv.append((7, word[:2]))
        fv.append((8, word[-2:]))
        fv.append((9, word[:3]))
        fv.append((10, word[-3:]))
        fv.append((11, word[:4]))
        fv.append((12, word[-4:]))
        fv.append((13, prev_tag))
        fv.append((14, prev_backpointer, prev_tag))
        if self.__contains_digits(word):
            fv.append((15, "hasNumber"))
        if self.__contains_hyphen(word):
            fv.append((16, "hasHyphen"))
        if self.__contains_upper(wordlist[index]):
            fv.append((17, "hasUpperCase"))
        fv.append((18, prev_backpointer))
        fv.append((19, wordlist[index - 1].lower()[-3:]))
        fv.append((20, wordlist[index + 1].lower()[-3:]))

    def get_global_vector(self, wordlist, poslist):  # Computing Sentence Feature
        fv = defaultdict(int)
        for i in range(3, len(wordlist) - 2):
            word = wordlist[i].lower()
            tag = poslist[i]
            fv[(0, word), tag] += 1
            fv[(1, wordlist[i - 1].lower()), tag] += 1
            fv[(2, wordlist[i - 2].lower()), tag] += 1
            fv[(3, wordlist[i + 1].lower()), tag] += 1
            fv[(4, wordlist[i + 2].lower()), tag] += 1
            fv[(5, word[:1]), tag] += 1
            fv[(6, word[-1:]), tag] += 1
            fv[(7, word[:2]), tag] += 1
            fv[(8, word[-2:]), tag] += 1
            fv[(9, word[:3]), tag] += 1
            fv[(10, word[-3:]), tag] += 1
            fv[(11, word[:4]), tag] += 1
            fv[(12, word[-4:]), tag] += 1
            fv[(13, poslist[i - 1], tag)] += 1
            fv[(14, poslist[i - 2], poslist[i - 1]), tag] += 1
            if self.__contains_digits(word):
                fv[(15, "hasNumber"), tag] += 1
            if self.__contains_hyphen(word):
                fv[(16, "hasHyphen"), tag] += 1
            if self.__contains_upper(wordlist[i]):
                fv[(17, "hasUpperCase"), tag] += 1
            fv[(18, poslist[i - 2]), tag] += 1
            fv[(19, wordlist[i - 1].lower()[-3:]), tag] += 1
            fv[(20, wordlist[i + 1].lower()[-3:]), tag] += 1
