import feature_vector
import feature_generator_base
import debug.debug

import string
import copy

__version__ = '1.1'


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

    def load_to_sentence(self, sentence):
        if sentence.fgen is not None:
            sentence.fgen.unload_from_sentence(sentence)

        sentence.column_list["FORM"].insert(0, '_B_-1')
        sentence.column_list["FORM"].insert(0, '_B_-2')  # first two 'words' are B_-2 B_-1
        sentence.column_list["FORM"].append('_B_+1')
        sentence.column_list["FORM"].append('_B_+2')     # last two 'words' are B_+1 B_+2

        sentence.column_list["POSTAG"].insert(0, 'B_-1')
        sentence.column_list["POSTAG"].insert(0, 'B_-2')

        gold_global_vector = self.get_feature_vector(sentence=sentence)

        sentence.gold_global_vector = gold_global_vector
        sentence.fgen = self
        return

    def unload_from_sentence(self, sentence):
        if sentence.fgen is None:
            return
        if sentence.fgen.name != "POSTaggerFeatureGenerator":
            sentence.fgen.unload_from_sentence(sentence)
            return

        del sentence.column_list["FORM"][0]
        del sentence.column_list["FORM"][0]
        del sentence.column_list["FORM"][len(sentence.column_list["FORM"]) - 1]
        del sentence.column_list["FORM"][len(sentence.column_list["FORM"]) - 1]

        del sentence.column_list["POSTAG"][0]
        del sentence.column_list["POSTAG"][0]

        sentence.fgen = None
        return

    def update_sentence_with_output(self, sentence, output):
        if sentence.fgen != self:
            raise RuntimeError("FGEN [ERROR]: update_sentence_with_output " +
                "can only update sentence  with this fgen as feature generator")
        sentence.column_list["POSTAG"] = copy.deepcopy(output)
        return

    def __contains_digits(self, s):
        return any(char.isdigit() for char in s)

    def __contains_hyphen(self, s):
        return any(char == "-" for char in s)

    def __contains_upper(self, s):
        return any(char.isupper() for char in s)

    def __contains_punc(self, s):
        return any(char in string.punctuation for char in s)

    def current_tag_feature(self,
                            sentence,
                            index,
                            prev_tag,
                            prev_backpointer):

        wordlist = sentence.column_list["FORM"]
        pos_list = sentence.column_list["POSTAG"]

        fv = []
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
        return fv

    def get_feature_vector(self, sentence, output=None):  # Computing Sentence Feature
        wordlist = sentence.column_list["FORM"]
        if output is None:
            poslist = sentence.column_list["POSTAG"]
        else:
            poslist = output

        fv = []
        for i in range(3, len(wordlist) - 2):
            word = wordlist[i].lower()
            tag = poslist[i]
            fv.append(str((0, word, tag)))
            fv.append(str((1, wordlist[i - 1].lower(), tag)))
            fv.append(str((2, wordlist[i - 2].lower(), tag)))
            fv.append(str((3, wordlist[i + 1].lower(), tag)))
            fv.append(str((4, wordlist[i + 2].lower(), tag)))
            fv.append(str((5, word[:1], tag)))
            fv.append(str((6, word[-1:], tag)))
            fv.append(str((7, word[:2], tag)))
            fv.append(str((8, word[-2:], tag)))
            fv.append(str((9, word[:3], tag)))
            fv.append(str((10, word[-3:], tag)))
            fv.append(str((11, word[:4], tag)))
            fv.append(str((12, word[-4:], tag)))
            fv.append(str((13, poslist[i - 1], tag)))
            fv.append(str((14, poslist[i - 2], poslist[i - 1], tag)))
            if self.__contains_digits(word):
                fv.append(str((15, "hasNumber", tag)))
            if self.__contains_hyphen(word):
                fv.append(str((16, "hasHyphen", tag)))
            if self.__contains_upper(wordlist[i]):
                fv.append(str((17, "hasUpperCase", tag)))
            fv.append(str((18, poslist[i - 2], tag)))
            fv.append(str((19, wordlist[i - 1].lower()[-3:], tag)))
            fv.append(str((20, wordlist[i + 1].lower()[-3:], tag)))
        return fv
