#!/usr/bin/env python

import sys, fileinput
import collections
import trees

count = collections.defaultdict(int)

ts = []
for line in fileinput.input():
    t = trees.Tree.from_str(line)
    for leaf in t.leaves():
        count[leaf.label] += 1
    ts.append(t)

for t in ts:
    for leaf in t.leaves():
        if count[leaf.label] < 2:
            leaf.label = "<unk>"
    sys.stdout.write("{0}\n".format(t))
