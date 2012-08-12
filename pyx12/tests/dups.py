#! /usr/bin/env python

import sys

m = {}
for line in sys.stdin.readlines():
    try:
        m[line] += 1
    except:
        m[line] = 1
for key in m.keys():
    if m[key] > 1:
        print key
