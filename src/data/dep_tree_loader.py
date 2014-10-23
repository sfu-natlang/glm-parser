class DepTreeLoader():
    def __init__(self):
        return

    def load_dep_tree(self, filename):
        data = open(filename)

        sent_list = []
        sent = []
        for line in data:
            line = line[:-1]

            if not line == "":
                line = line.split()
                line[2] = int(line[2])
                sent.append(line)
            else:
                if not sent == []:
                    sent_list.append(sent)
                    sent = []

        print "load dep tree finished"
        return sent_list