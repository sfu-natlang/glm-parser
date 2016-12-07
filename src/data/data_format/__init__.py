from data.file_io import fileRead, fileWrite
from data.sentence import Sentence


class DataFormatBase():
    def __init__(self, fgen):
        self.fgen = fgen
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
