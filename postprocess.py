#!/usr/bin/env python

import sys, fileinput
import trees

for line in fileinput.input():
    try:
        t = trees.Tree.from_str(line)

        t.restore_unit()
        t.unbinarize()

        print(t)
    except:
        print("")
    
    
