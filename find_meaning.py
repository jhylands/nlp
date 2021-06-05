from lark import Tree
from lark.visitors import CollapseAmbiguities
import sys
from wordlexer import WordLexer, Token
from parser import plot, p
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

def replace_node_verb(t):
    if isinstance(t, Token):
        return
    for index, child in enumerate(t.children):
        if isinstance(child, Token):
            return
        if child.data=="vp" and len(child.children)==1 and child.children[0].data=="verb":
            # so here it would be nice to replace t with t.children[0] but to do that we need a reference to t.
            t.children[index] = child.children[0]
        if child.data=="vp" and len(child.children)==1 and child.children[0].data=="terminalverbphrase":
            # so here it would be nice to replace t with t.children[0] but to do that we need a reference to t.
            t.children[index] = child.children[0]
        if child.data=="np" and len(child.children)==1 and child.children[0].data=="noun":
            # so here it would be nice to replace t with t.children[0] but to do that we need a reference to t.
            t.children[index] = child.children[0]
        if child.data=="np" and len(child.children)==1 and child.children[0].data=="terminalnounphrase":
            # so here it would be nice to replace t with t.children[0] but to do that we need a reference to t.
            t.children[index] = child.children[0]
        if child.data=="noun" and len(child.children)==1 and isinstance(child.children[0], Tree) and child.children[0].data=="pronoun":
            # so here it would be nice to replace t with t.children[0] but to do that we need a reference to t.
            t.children[index] = child.children[0]
        if child.data=="advp" and len(child.children)==1 and isinstance(child.children[0], Tree) and child.children[0].data=="adverb":
            # so here it would be nice to replace t with t.children[0] but to do that we need a reference to t.
            t.children[index] = child.children[0]
        else:
            [replace_node_verb(child) for child in t.children]
    

def find_meaning(t: Tree):
    if isinstance(t, Token):
        return
    if t.data in ["start", "sentence"]:
        return find_meaning(t.children[0])

    if t.data=="declarative_sentence":
        np, vp = t.children
        if is_(vp, "vp terminalvp np"):
            # That is saying that the terminal vp is being applied to
            # t.children[0] and vp.children[1]
            return "( ({n1})->(PERFORMING)->({v}) )-(happening_to)->({n2})"
        elif is_(vp, "vp terminalvp"):
            # The noun is perform(ing)(obs tense) the verb
            return "({n1})->(PERFORMING)->({v})"
        elif is_(vp, "vp linkingverb adjp"):
            # That means this adjective is being linked to the noun through the linking verb
            return "({n1})->(linkingverb)->({adj})"
        elif is_(vp, "vp vp pp"):
            return "({vp})->({prepositional})->({preposition})"
            # the pp is describing the vp
            pass
    elif t.data == "vp":
        pass
    elif t.data == "np":
        np = t
        if is_(np, "np np pp"):
            # this is also adding extra information about the noun
            return "({np})->({prepositional})->({preposition})"
        elif is_(np, "np np sbar"):
            # this is adding extra information about the noun
            pass
        elif is_(np, "np terminalnounphrase"):
            return "(noun) where noun -> adjective"
            pass
        else:
            # assuming the quote isn't implemented
            raise Exception("NP meaning confused")
    elif t.data == "terminalnounphrase":
        # the meaning of this is pretty simple.
        pass


def main(phrase):
    try:
        parsed_phrase = p.parse(phrase)
        replace_node_verb(parsed_phrase)
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
    #print(plot(parsed_phrase))
    for x in CollapseAmbiguities().transform(parsed_phrase):
        print(x.pretty())
        input()

if __name__=="__main__":
    phrase = sys.argv[1]
    main(phrase)
