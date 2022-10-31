class CKYParser():
    grammar = None
    chart = None
    RHS = dict()
    current_weight = dict()
    
    def __init__(self, grammar):
        self.grammar = grammar  
   
    def create_chart(self, sentence):
        sent_split = sentence.split(' ')
        
        for i in range(len(sent_split)):
            if sent_split[i] not in self.grammar.unique_non_terminals:
                sent_split[i] = '<unk>'
                
        chart_size = len(sent_split)
        
        self.chart = [[defaultdict(lambda : []) for x in range(chart_size)] for y in range(chart_size)]      

        for i in range(len(sent_split)):            
            for rule in self.grammar.cond_prob:
                if rule[1] == sent_split[i]: # matching RHS of rule
                    self.chart[i][i][rule[0]].append([np.log10(self.grammar.cond_prob[rule]), (0,0), (i,i), (i,i), (sent_split[i], sent_split[i])]) # set cell to LHS
                    
        for diagonals in range(1,len(sent_split)):
            
            for i in range(len(sent_split) - diagonals):   
                self.RHS = {}
                for x in range(diagonals):                                        
                    left = (i, i+x)
                    right = (i+1+x, i+diagonals)
                    
                    if len(self.chart[i][i+x]) == 0 or len(self.chart[i+1+x][i+diagonals]) == 0:
                        continue
                        
                    for c_key, c_value in self.chart[i][i+x].items():
                        for d_key, d_value in self.chart[i+1+x][i+diagonals].items():
                            left = (i, i+x)
                            right = (i+1+x, i+diagonals)                                                      
                            self.RHS[c_key + ' ' + d_key] = (c_value[0][0] + d_value[0][0], (c_value[0][0], d_value[0][0]), left, right, (c_key,d_key))
                            
                    for rule in self.grammar.cond_prob:                         
                        for r in self.RHS:    
                            if rule[1] == r:                                                                     
                                self.current_weight[rule[0]] = self.RHS[rule[1]][0] + np.log10(self.grammar.cond_prob[rule])
                                
                                if rule[0] in self.chart[i][i+diagonals]:                              
                                    self.chart[i][i+diagonals][rule[0]].append([self.current_weight[rule[0]]]+ list(self.RHS[rule[1]][1:]) )
                                else:                                    
                                    print
                                    self.chart[i][i+diagonals][rule[0]].append([self.current_weight[rule[0]]]+ list(self.RHS[rule[1]][1:]))
        self.RHS = dict()
        self.current_weight = dict()
        
                
    def max_root_element(self, cell_list):
        max_score = -100000
        
        return_list = None
        for element in cell_list:
            if element[0] > max_score:
                return_list = element
                max_score = element[0]
        return return_list.copy()
    
    def select_approp_child(self, child_tag_list, child_score):     
        for tag_list in child_tag_list:
            if str(tag_list[0]) == str(child_score):                
                return (tag_list[2], tag_list[3]),tag_list[1],(tag_list[-1])
        return ''
                
    def generate_tree_from_cky(self, root, child_coords=None, child_scores=None, child_tags=None):                                          
        if child_coords != None:           
            left_child_coordinates, right_child_coordinates = child_coords
            left_child_score, right_child_score = child_scores 
            left_child_tag, right_child_tag = child_tags        
        
        if 'TOP' == root.label:                        
            element = self.max_root_element(self.chart[0][len(self.chart)-1]['TOP'])
            root_score = element[0]
            left_child_coordinates, right_child_coordinates = element[2], element[3]
            left_child_score, right_child_score = element[1]
            left_child_tag, right_child_tag = element[-1]
                       
        # Base Case
        if left_child_coordinates == right_child_coordinates:
            root.children.append(trees.Node(left_child_tag))
            return
        
        #left child
        left_child = trees.Node(left_child_tag)
        root.children.append(left_child)                
        
        left_results = self.select_approp_child(self.chart[left_child_coordinates[0]][left_child_coordinates[1]][left_child_tag], left_child_score)        
        child_coordinates, child_scores, child_tags = left_results         
               
        self.generate_tree_from_cky(left_child, child_coordinates, child_scores, child_tags)        
        
        #Right child
        right_child = trees.Node(right_child_tag)      
        root.children.append(right_child)
        right_results = self.select_approp_child(self.chart[right_child_coordinates[0]][right_child_coordinates[1]][right_child_tag], right_child_score)
        child_coordinates, child_scores, child_tags = right_results   
        self.generate_tree_from_cky(right_child, child_coordinates, child_scores, child_tags)      