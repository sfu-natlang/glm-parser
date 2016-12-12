from data.data_format import DataFormatBase


class DataFormat(DataFormatBase):
    def __init__(self, fgen):
        DataFormatBase.__init__(self, fgen)
        self.format_list = ["ID",
                            "FORM",
                            "LEMMA",
                            "GPOS",
                            "PPOS",
                            "SPLIT_FORM",
                            "SPLIT_LEMMA",
                            "PPOSS",
                            "HEAD",
                            "DEPREL",
                            "PRED",
                            "ARG"]
        self.comment_sign = ""
        return
