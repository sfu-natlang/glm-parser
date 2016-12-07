from data.data_format import DataFormatBase


class DataFormat(DataFormatBase):
    def __init__(self, fgen):
        DataFormatBase.__init__(self, fgen)
        self.format_list = ["ID",
                            "FORM",
                            "LEMMA",
                            "CPOSTAG",
                            "POSTAG",
                            "FEATS",
                            "HEAD",
                            "DEPREL",
                            "PHEAD",
                            "PDEPREL"]
        self.comment_sign = ""
        return
