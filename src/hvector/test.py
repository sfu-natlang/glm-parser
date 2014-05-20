#!/usr/bin/env python

from _mycollections import mydefaultdict
from mydouble import mydouble, counts

x = mydouble(1)
print x

x += x
print x

x += 5
print x

x += mydouble(2)
print x
print x.__copy__()

x = mydouble()
print x

# x += "1"
# print x

d = mydefaultdict(mydouble)  # always like that

d["a"] = 1                   # no need to say mydouble(1); transparent to the user
print d

d.iadd(d)
print "d=", d

d.iaddc(d, 0.5)
print "d=", d

c = mydefaultdict(mydouble)  # always like that
print c

c += d
#c.__iadd__(d)
print "here", c

e = d # mydefaultdict(mydouble, [("1", 1.)])
# print e
# print type(e.get("1"))  # float

print e["b"]
e["b"] += 1
print e["b"], type(e.get("b"))
e.get("c").incr()
print e["c"], type(e.get("c"))

print "before del e[...]", counts()
del e["c"]
print "after  del e[...]", counts()

for i in xrange(10000):
    continue
    e[str(i)+"a"] = 1#mydouble(1)
    e.get(str(i)).incr()

print counts()
print len(e)
print e.dot(d)

print "making large dict..."
f = mydefaultdict(mydouble, [(x, mydouble(x)) for x in range(1000000)])
print "done"

print len(f)

import time
c = time.time()
f.dot(f)
print time.time() - c

c = time.time()
f.dot(d)
d.dot(f)
print time.time() - c
