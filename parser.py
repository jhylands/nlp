from lark import Lark
from lark.lexer import Token
from wordlexer import WordLexer


def plot(t):
    if isinstance(t, Token):
        return str(t)
    elif t.data=="_ambig":
        return "({self}\n{children})".format(self=t.data, children="\n".join([plot(c) for c in t.children]))
    else:
        return "({self} {children})".format(self=t.data, children=" ".join([plot(c) for c in t.children]))


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
p = Lark(collision_grammar, parser='earley', ambiguity="explicit", lexer=WordLexer, import_paths=["."], debug=True)
