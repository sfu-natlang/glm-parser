#!/usr/bin/env python

from _mycollections import mydefaultdict
from mydouble import mydouble, counts

d = mydefaultdict(mydouble)  # always like that

d["a"] = 1                   # no need to say mydouble(1); transparent to the user
print d

print d.addc(d, 0.5)

for i in xrange(500000):
    d[str(i)] = 2

print len(d)

import gc
e = d.copy()
print "before", e["a"], counts()

for i in xrange(20):
#    e = e.deepcopy()
    e.iaddc(d, 0.5)
#    e.addc(d, 0.5)
    print e["a"], counts()
#    gc.collect()
#     del e
# ##    gc.collect()
#     e = f
    
print d["a"]
