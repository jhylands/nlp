from tree import A, B, C, SearchNode, ReplacementNode

def name(instance):
    return instance.__class__.__name__

def test_cut():
    root = A([B([C()])])
    # lhs is the search rule giving the structure
    # we are going to replace
    a_search = SearchNode(lambda x:name(x)=="A")
    b_search = SearchNode(lambda x:name(x)=="B")
    c_search = SearchNode(lambda x:name(x)=="C")
    a_search.children=[b_search]
    b_search.children=[c_search]

    lhs = a_search
    rhs = ReplacementNode(
        a_search,
        children=[c_search])
    assert root.children == [leaf]

