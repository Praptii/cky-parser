class ParseUtils:  
    def __init__(self, grammar):
        self.grammar = grammar
        
    def get_n_parses(self, file_name, n = 58):
        f = open(file_name, "r")
        lines = f.readlines()
        output_lines = []
        
        for line in lines[:n]:
            line = line.replace('\n', '')
            line_split = line.split(' ')
            score = 0
            
            for i in range(len(line_split)):
                if line_split[i] not in self.grammar.unique_non_terminals:
                    line_split[i] = '<unk>'
                        
            sentence = ' '.join(line_split)
            print(sentence)
                        
            
            cky = CKYParser(self.grammar)            
            cky.create_chart(sentence)
            sa_tree = trees.Tree(trees.Node('TOP'))                        
            
            if 'TOP' in cky.chart[0][len(line_split)-1]:
                cky.generate_tree_from_cky(sa_tree.root)
                score = cky.max_root_element(cky.chart[0][len(line_split)-1]['TOP'])                                             
                print(f'{sa_tree} --> {score[0]} \n')
                
                sa_tree.restore_unit()
                sa_tree.unbinarize()
                
                output_lines.append(str(sa_tree))
            else:
                output_lines.append('\n')
            
        return output_lines
    
    def generate_output_file(self, input_file, output_file):
        output_pcfg = self.get_n_parses(input_file)
                
        with open(output_file, 'w') as temp_file:
            for item in output_pcfg:    
                
                if item == '\n':
                    temp_file.write('\n')
                    continue
                    
                temp_file.write(f'{item}\n')