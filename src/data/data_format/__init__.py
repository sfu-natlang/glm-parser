from data.file_io import fileRead, fileWrite
from data.sentence import Sentence
from copy import deepcopy


class DataFormatBase():
    def __init__(self, fgen):
        self.fgen = fgen
        self.format_list = []
        self.comment_sign = ""
        return

    def load_from_content(self, content):
        data_list = []
        column_list = {}
        for field in self.format_list:
            if not(field.isdigit()):
                column_list[field] = []

        length = len(self.format_list)

        for line in content:
            entity = line.split()
            if len(entity) == length and entity[0] != self.comment_sign:
                for i in range(length):
                    if not(self.format_list[i].isdigit()):
                        column_list[self.format_list[i]].append(str(entity[i].encode('utf-8')))
            else:
                if not(self.format_list[0].isdigit()) and column_list[self.format_list[0]] != []:
                    sent = Sentence(column_list, self.format_list, self.fgen)
                    data_list.append(sent)

                column_list = {}

                for field in self.format_list:
                    if not (field.isdigit()):
                        column_list[field] = []

        return data_list

    def load_stringtext(self, textString):
        content = textString.splitlines()

        return self.load_from_content(content)

    def get_data_from_file(self, file_path):
        content = fileRead("file://" + file_path)

        return self.load_from_content(content)

    def export_to_file(self, dataPool, fileURI, sparkContext=None):
        content = []
        dataPool.reset_index()
        while dataPool.has_next_data():
            sentence = dataPool.get_next_data()
            sentence = deepcopy(sentence)
            sentence.unload_fgen()

            length = len(sentence.column_list["FORM"])

            for index in range(length):
                line = ""
                for item in self.format_list:
                    if item not in sentence.column_list:
                        line = line + "O"
                    else:
                        line = line + sentence.column_list[item][index]
                    line = line + " "

                content.append(line)
            content.append("")

        dataPool.reset_index()
        fileWrite(fileURI=fileURI,
                  contents=content,
                  sparkContext=sparkContext)
        return
