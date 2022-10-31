import collections
import trees
import pickle

with open('sample.vars','rb') as f:
    # These sample variables are the result of treating the first 3 sentences as our entire training data
    sample_vars = pickle.load(f)

def read_trees(fname):
    """Read in all trees from a given file
    input: filename
    outputs: rule lookup dictionary, count of each rule seen"""
    # Replace this with your code, for now I put a placeholder in
    rules_lookup = sample_vars[0]
    rule_counts = sample_vars[1]
    return rules_lookup, rule_counts

fname = 'train.trees.pre.unk'
rules_lookup, rule_counts = read_trees(fname)
''' Format of rules_lookup provided is:
    key = RHS of rule
    value = set of valid LHS of rules
    For example:
    rules_lookup['the'] = {'DT'} corresponds to rule DT -> the
    rules_lookup['stop'] = {'VBP','NN'} corresponds to rules stop -> VBP and stop -> NN'''


''' Format of rule_counts provided is:
    key = rule as tuple of (LHS, RHS)
    value = how many times that rule was seen in the data
    For example:
    rule_counts[('PP', ('IN', 'NP_NNP'))] = 4
    rule_counts[('DT', 'this')] = 1'''

def get_probs(rules_lookup, rule_counts):
    """Given the rules_lookup dictionary and the total count of rules
    return a dictionary with keys as rules and values as probabilities"""
    grammar = sample_vars[2]
    return grammar

grammar = get_probs(rules_lookup, rule_counts)
''' Format of grammar provided is:
    key = rule as tuple of (LHS, RHS)
    value = conditional probability of RHS given LHS
    For example:
    grammar[('PP', ('IN', 'NP_NNP'))] = 0.66666666
    grammar[('DT', 'this')] = 0.25'''



def CKY(sent, grammar):
    """Given a space separated sentence and your grammar,
    run CKY to fill the chart with the highest probability partial parses.
    Return the filled in chart from CKY"""
    chart = sample_vars[3]
    return chart

sent = sample_vars[4]
chart = CKY(sent, grammar)
''' Format of chart provided is:
    chart[row][column] = dictionary with:
        key = parse for that span (LHS of rule applied)
        value = [weight, RHS of rule applied, index of first word  of span (i), split index (x), diagonal # (diagonals)]
    For example:
    chart[0][0]['VBZ'] = [1.0, 'Does', 0, None, None]
    weight is 1.0, RHS of rule is Does, comes from word 0, there is no split, there is no diagonal #
    
    chart[0][-1]['TOP'] = [0.000992063492063492, ('SQ', 'PUNC'), 0, 4, 5]
    weight is 0.00099, RHS of rule is ('SQ', 'PUNC'), starts at word 0, splits after word index 4, 5th diagonal processed
    '''

def parse(chart, s='TOP', row=0, col=-1):
    """Given the following:
    chart - filled in chart from CKY
    s - used for recursion, starts with 'TOP'
    row - the index of the row that i appears in
    col - the index of the column that s appears in
    This will be recursive, with s row and col changing"""
    parse_string = sample_vars[5]
    return parse_string

parse_string = parse(chart)
''' Format of parse_string matches train.trees'''
