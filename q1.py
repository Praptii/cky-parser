from collections import Counter

def question_no_1(grammar):
    
    uniq_keys = []
    freq_keys = []

    uniq = Counter(grammar.rules)
    uniq_keys_count = len(set(uniq))
        
    print(f'Unique rules count: {uniq_keys_count} \n' )
    
    for freq in uniq.most_common(5):
        print(f'Most frequent rules: {freq} \n' )