
import eisner
import ceisner
test_edge_score = {
    ('0','1'): 1,
    ('0','2'): 1,
    ('0','3'): 10,
    ('0','4'): 1,
    ('0','5'): 2,
    ('0','6'): 1,
    ('0','7'): 3,
    ('0','8'): 2,
    ('0','2'): 1,

    ('3','2'): 12,
    ('2','1'): 9,
    ('3','5'): 11,
    ('5','4'): 10,
    ('5','6'): 8,
    ('6','8'): 8,
    ('8','7'): 7,

    ('4','6'): 1,
    ('8','2'): 4,
    ('3','7'): 3,
    ('5','8'): 1,
    ('1','3'): 2
}

def test_get_score(a,b):
    if test_edge_score.has_key((a,b)):
        return test_edge_score[(a,b)]
    else:
        return 0

def test_eisner():
    sentence = "0 1 2 3 4 5 6 7 8".split()
    print sentence
    a = ceisner.EisnerParser()
    b = a.parse(9, test_get_score)
    print b

if __name__ == "__main__":
    test_eisner()
    #ce = ceisner.EisnerParser(5)
    #print ce.get_i(4, 4,1,1)
    
