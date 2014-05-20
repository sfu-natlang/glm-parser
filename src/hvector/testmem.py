#!/usr/bin/env python

import sys
module = __import__(sys.argv[1])

for i in xrange(5000000):
    str(module.mydouble(i))
