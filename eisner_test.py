
import eisner

test_edge_score = {
    ('ROOT','ecnomic'): 1,
    ('ROOT','news'): 1,
    ('ROOT','had'): 10,
    ('ROOT','little'): 1,
    ('ROOT','effect'): 2,
    ('ROOT','on'): 1,
    ('ROOT','financial'): 3,
    ('ROOT','markets'): 2,
    ('ROOT','news'): 1,

    ('had','news'): 12,
    ('news','ecnomic'): 9,
    ('had','effect'): 11,
    ('effect','little'): 10,
    ('effect','on'): 8,
    ('on','markets'): 8,
    ('markets','financial'): 7,

    ('little','on'): 1,
    ('markets','news'): 4,
    ('had','financial'): 3,
    ('effect','markets'): 1,
    ('ecnomic','had'): 2
}

def test_get_score(parent,child):
    if test_edge_score.has_key((parent,child)):
        return test_edge_score[(parent,child)]
    else:
        return 0

def test_eisner():
    sentence = "ROOT ecnomic news had little effect on financial markets".split()
    print eisner.EisnerParser(sentence).parse(test_get_score)

if __name__ == "__main__":
    test_eisner()
