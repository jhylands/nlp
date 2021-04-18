from itertools import combinations, product
def is_unique_list(the_list):
    return len(set(the_list))==len(the_list)

class Node:
    def __init__(self, children=None):
        children = children or []
        self.children = children

    def append(self, child):
        self.children.append(child)

    def _find_sub_from_children(self, root_search):
        possible_pairing_of_children = combinations(
            product(
                self.children,
                root_search.children),
            2)

        valid_pairings = (pairing for pairing in possible_pairing_of_children 
            if all(map(is_unique_list, zip(*pairing)))) 


         matching_pairings = (pairing for pairing in valid_pairings 
            if all(b.pairing(a) for a, b in pairing))
        for matching_pairing in matching_pairings:
            for a, b in matching_pairing:
                found = a.find(b) 
                if found:
                    return found
        return False
        
    def find(self, root_search):
        # only interested in the first one we find
        if root_search.match(self):
            found = self._find_sub_from_children(root_search)
            if found:
                return found
        # this can't be an else clause!
        for c in self.children:
            found = c.find(root_search) 
            if found:
                return found
        return False

class A(Node):
    pass        
class B(Node):
    pass        
class C(Node):
    pass        

"""
So the idea that I am going for here is that
the replacement nodes are specific kinds that contain
lambdas which tell if a node matches the replacement rule
I think that is better than trying to make the replacement
of the original type.
"""
class SearchNode(Node):
    def __init__(self, property_lambda=lambda: True, children=None):
        self.property_lambda = property_lambda
        super().__init__(children)

    def match(self, node):
        return len(node.children) >= len(self.children) and\
            self.property_lambda(node)

class ReplacementNode(Node):
    def __init__(self, matched_node, children=None):
        self.matched_node = matched_node 
        super().__init__(children)
