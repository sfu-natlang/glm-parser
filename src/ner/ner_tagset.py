
import os,sys,inspect

# read the valid output tags for the NER tagging from the file
def read_ner_tagset():
    file_path = "ner_tagset.txt"
    ner_tagset = []
    with open(file_path,"r") as in_file:
        for line in in_file:
            line = line.strip()
            ner_tagset.append(line)
    return ner_tagset
