from data.data_format import DataFormatBase
from data.sentence import Sentence


class DataFormat(DataFormatBase):
    def __init__(self, fgen):
        DataFormatBase.__init__(self, fgen)
        self.format_list = ["FORM",
                            "POSTAG",
                            "CHUNK",
                            "NER"]
        self.comment_sign = ""
        return
