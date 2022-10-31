#!/usr/bin/env python

import sys, fileinput
import trees

for li, line in enumerate(fileinput.input()):
    t = trees.Tree.from_str(line)

    # Binarize, inserting 'X*' nodes.
    t.binarize()

    # Remove unary nodes
    t.remove_unit()

    # The tree is now strictly binary branching, so that the CFG is in Chomsky normal form.

    # Make sure that all the roots still have the same label.
    assert t.root.label == 'TOP', f'line {li}: {t.root.label}'

    print(t)
    
    
