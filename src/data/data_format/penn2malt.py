from data.data_format import DataFormatBase


class DataFormat(DataFormatBase):
    def __init__(self, fgen):
        DataFormatBase.__init__(self, fgen)
        self.format_list = ["FORM",
                            "POSTAG",
                            "HEAD",
                            "DEPREL"]
        self.comment_sign = ""
        return
