from lark import Lark
from lark.lexer import Token
from wordlexer import WordLexer


def plot(t):
    if t is None:
        return
    if isinstance(t, str):
        return t
    elif isinstance(t, Token):
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
sbar: conjunction sentence
np: terminalnounphrase | np pp | np sbar | QUOTE WORD* QUOTE
terminalnounphrase: determiner? adjp? noun
vp: terminalvp | terminalvp np | vp pp | linkingverb adjp
terminalvp: advp? verb+ advp?
adjp: adjective+
advp: adverb+
imperative_sentence: vp np
interrogative_sentence: qvp? np QUESTIONMARK
qvp: advp? verb? adjp| verb vp
QUESTIONMARK: "?"
QUOTE: "`"
WORD: /[a-z]+/
%ignore " "
%import .ambiguous_word (determiner, noun, linkingverb, verb, pronoun, conjunction, adjective, adverb, preposition)
'''
p = Lark(collision_grammar, parser='earley', ambiguity="explicit", lexer=WordLexer, import_paths=["."], debug=True)

simple_grammar = '''
start: sentence
sentence: np vp obj
pp: preposition np
np: determiner? adjp? noun
vp: verb+
obj: np | advp? verb | pp
adjp: adjective+
advp: adverb+
%ignore " "
%import .ambiguous_word (determiner, noun, verb, pronoun, conjunction, adjective, adverb, preposition)
'''
simple_p = Lark(simple_grammar, parser='earley', ambiguity="explicit", lexer=WordLexer, import_paths=["."], debug=True)
