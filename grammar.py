class Grammar:       
    total_count = dict()
    cond_prob = dict()
    val_count = dict()
    rules = [] 
    rhs_to_lhs = dict()
    unique_non_terminals = []
    
    def scan_tree(self, node):    
        if len(node.children) == 0:
            return 0
        else:
            #Nodes with single child
            if len(node.children) == 1:
                self.rules.append(f'{node.label} -> {node.children[0].label}')
                self.scan_tree(node.children[0])

            #Nodes with two children
            elif len(node.children) == 2:
                self.rules.append(f'{node.label} -> {node.children[0].label} {node.children[1].label}')
                self.scan_tree(node.children[0])
                self.scan_tree(node.children[1])
    
    def fill_rules(self, tree_file):                
        f = open(tree_file, "r")
        lines = f.readlines()

        for line in lines:            
            tree = trees.Tree.from_str(line)
            self.scan_tree(tree.root)
            
            for leaf in tree.leaves():
                self.unique_non_terminals.append(leaf.label)
        
        self.unique_non_terminals = list(set(self.unique_non_terminals))
            
        return 1

    def calc_probability(self):
                
        for item in self.rules:
            key = item.split("->")
            if key[0].strip() in self.rhs_to_lhs:
                self.rhs_to_lhs[key[0].strip()].append(key[1].strip())
            else:
                self.rhs_to_lhs[key[0].strip()] = [key[1].strip()]

        for key,value in self.rhs_to_lhs.items():
            self.total_count[key] = len(self.rhs_to_lhs[key])

        for key, value in self.rhs_to_lhs.items():
            for val in value:
                if (key,val) in self.val_count:
                    self.val_count[(key,val)] += 1
                else:
                    self.val_count[(key,val)] = 1
                self.cond_prob[(key,val)] = self.val_count[(key,val)] / self.total_count[key]
                
    def get_top_5(self, non_terminal):
        top_5 = dict()
        top_5_non_terminals = dict()
        
        for key,value in self.cond_prob.items():
            if key[0] == non_terminal:
                top_5[key[1]] = value

        sorted_top_5 = dict(sorted(top_5.items(), key=operator.itemgetter(1),reverse=True))
        count = 0
        
        for key, value in sorted_top_5.items():
            top_5_non_terminals[key] = value
            count += 1
            if count == 5:
                break

        for key,value in top_5_non_terminals.items():
            print(f'{non_terminal} -> {key} : {value}')

        return 0    