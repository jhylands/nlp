from lark import Tree
import sys
from wordlexer import WordLexer, Token
from parser import plot, simple_p
from typing import Tuple, List
from itertools import zip_longest


collision_grammar = '''
start: sentence
sentence: declarative_sentence | interrogative_sentence | imperative_sentence
declarative_sentence: np vp
pp: preposition+ np
sbar: sentence | conjunction sentence
np: determiner? adjp? noun | np pp | np sbar
vp: vp np | vp pp | advp? vp advp?| verb+
adjp: adjective+
advp: adverb+
imperative_sentence: vp np
interrogative_sentence: qvp? np QUESTIONMARK
qvp: advp? verb? adjp| verb vp
QUESTIONMARK: "?"
%ignore " "
%import .ambiguous_word (determiner, noun, verb, pronoun, conjunction, adjective, adverb, preposition)
'''
class AThing:
    def __init__(self, det, noun):
        self.det = det
        self.noun = noun
    def __str__(self):
        return "({} {})".format(self.det, self.noun)

class Meaning:
    def __init__(self, subject, verb, object=None):
        self.subject = subject
        self.verb = verb
        self.object = object

        self.compliment = None
        self.adverbial = None

    def __str__(self):
        if isinstance(self.verb, list):
            verb = "_".join(map(plot, self.verb))
        else:
            verb = self.verb
        if self.object is not None:
            return "({} {} {})".format(*map(plot, [verb, self.subject, self.object]))
        else:
            return "({} {})".format(*map(plot, [verb, self.subject]))

    def __repr__(self):
        return str(self)
            

def EQ(x):
    a, b = x
    return a==b
def is_(tree, rule):
    if "(" in rule:
        raise Exception("Can't handle that yet")
    data = tree.data
    children = tree.children
    units = rule.split(" ")
    types = [data] + [child.data for child in children]
    return all(map(EQ, zip_longest(types, units)))


def extract_nested_verbs(vp: Tree)->Tuple[List[Token], Tree]:
    # The idea is that this is a function which can round up the verbs
    if is_(vp, "vp vp np"):
        verbs, _ = extract_nested_verbs(vp.children[0])
        return verbs, vp.children[1]
    elif is_(vp, "vp verb vp"):
        verbs, np = extract_nested_verbs(vp.children[1])
        return [vp.children[0]] + verbs, np
    elif is_(vp, "vp verb np"):
        return [vp.children[0]], np
    elif is_(vp, "vp verb"):
        return [vp.children[0]], None
    else:
        return [], vp

def find_meaning(t: Tree):
    if t.data in ["start", "sentence"]:
        return find_meaning(t.children[0])
    if t.data=="_ambig":
        return filter(lambda x:x is not None, [find_meaning(child) for child in t.children])

    if t.data=="declarative_sentence":
        np1, vp = t.children
        verbs, np2 = extract_nested_verbs(vp)
        if verbs!=[]:
            if np2 is None:
                return Meaning(verb=verbs, subject = np1)
            else:
                return Meaning(verb=verbs, subject= np1, object=np2)
        else:
            print(plot(np1), plot(vp))
            
    elif is_(t, "np determiner noun"):
        return AThing(*t.children)
    else:
        print(t.data)
"""
        
        # vp decomposition
            vp, np = vp.children
            vp, pp = vp.children
            advp, vp, advp = vp.children
            verbs = vp.children
        # np decomposition
            determiner, adjp, noun
            np pp
            np sbar
"""

def main(phrase):
    try:
        parsed_phrase = simple_p.parse(phrase)
    except Exception as e:
        print(e)
        print(list(WordLexer().lex(phrase)))
        return
#    try:
#        meaning = find_meaning(parsed_phrase)
#    except Exception as e:
#        print(e)
    meaning = False
    if meaning:
        print("\n\n--------------------------------MEANING----------\n\n")
        print(list(meaning))
        print("End of meaning")
    print("plot: ")
    print(plot(parsed_phrase))

if __name__=="__main__":
    phrase = sys.argv[1]
    main(phrase)
